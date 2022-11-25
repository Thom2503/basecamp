from datetime import datetime
import csv


def read_logfile(file_path: str) -> list:
    """
    Lees de logfile en maak daar een list of dictionaries
    van met alle data die nodig is.

    :param file_path: str, pad naar de logfile
    """
    cars = []

    with open(file_path, "r") as file:
        log_lines = file.readlines()
        for line in log_lines:
            line_data = {
                'license_plate': '',
                'checked_in': '',
                'checked_out': '',
                'parking_fee': '',
                'cpm_name': ''
            }

            data = line.split(";")
            time = data[0]
            cpm_name = data[1].split("=")[1]
            license = data[2].split("=")[1]
            action = data[3].split("=")[1].replace("\n", "")

            try:
                parking_fee = data[4].split("=")[1].replace("\n", "")
            except IndexError:
                parking_fee = 0

            line_data['license_plate'] = license
            line_data['cpm_name'] = cpm_name

            if action == "check-in":
                line_data['checked_in'] = time
                line_data['checked_out'] = "None"

            if parking_fee == 0:
                line_data['parking_fee'] = parking_fee
            else:
                found_cars = list(filter(lambda x: x['license_plate'] == license, cars))
                found_car = list(filter(lambda x: x['parking_fee'] == 0, found_cars))

                if found_car == []:
                    idx = cars.index(found_cars[-1:][0])
                    found_data = cars[idx]
                    line_data['checked_in'] = found_data['checked_in']
                    line_data['checked_out'] = time
                    line_data['parking_fee'] = parking_fee
                else:
                    idx = cars.index(found_car[0])

                    line_data = cars[idx]
                    line_data['checked_out'] = time
                    line_data['parking_fee'] = parking_fee

            cars.append(line_data)

    # verwijder de duplicate dictionaries uit de lijst
    cars = [i for n, i in enumerate(cars) if i not in cars[n + 1:]]
    print(cars)
    return cars


def create_csv(data: list, cpm_name: str, from_date: str, to_date: str) -> None:
    """
    Converteer de data naar een csv bestand

    :param data: list, de data die in csv moet komen
    :param cpm_name: str, de id van de machine
    :param from_date: str, vanaf welke datum de report gemaakt wordt
    :param to_date: str, tot welke datum de report gemaakt wordt
    """
    # headers die csv nodig heeft
    headers = data[0].keys()

    with open(f"{cpm_name}_from_{from_date}_to_{to_date}.csv", "w") as out_file:
        writer = csv.DictWriter(out_file, headers, delimiter=';')
        writer.writeheader()
        writer.writerows(data)


def get_cars_in_period(log_data: list, from_date: str, to_date: str) -> list:
    """
    Zoek alle auto's tussen een specifieke datum.

    :param log_data: list, data met alle auto's
    :param from_date: str, vanaf welke datum gezocht moet worden
    :param to_date: str, tot welke datum gezocht moet worden

    :return list, lijst met de data van alle data in een periode
    """
    format = "%d-%m-%Y %H:%M:%S"
    from_datetime = datetime.strptime(from_date, format.split(" ")[0])
    to_datetime = datetime.strptime(to_date, format.split(" ")[0])

    def check_in_between(car: dict) -> bool:
        """
        Functie om te checken of de data tussen 2 data valt.

        :param car: dict, data van een auto

        :return bool, of het tussen de 2 data valt
        """
        return from_datetime <= datetime.strptime(car['checked_in'], format) <= to_datetime

    def check_after_to_date(car: dict) -> bool:
        """
        Functie om te checken of de checked_out tijd na de to date is

        :param car: dict, data van een auto

        :return bool
        """
        if car['checked_out'] == "None":
            return True
        return datetime.strptime(car['checked_out'], format) <= to_datetime

    filtered_list = list(filter(check_in_between, log_data))
    return list(filter(check_after_to_date, filtered_list))


def get_specific_period(log_data: list, machine: str, from_date: str, to_date: str) -> None:
    """
    Filter alle data op basis van de machine en de from_date en to_date, daar zou
    dan een lijst met dictionaries uit komen met alle data van een bepaalde datum
    tot een bepaalde datum.

    :param log_data: list, lijst met de auto data uit de logfile
    :param machine: str, op welke machine gefilterd moet worden
    :param from_date: str, vanaf welke datum
    :param to_date: str, tot welke datum
    """
    all_machine_cars = list(filter(lambda car: car['cpm_name'] == machine, log_data))
    cars_in_period = get_cars_in_period(all_machine_cars, from_date, to_date)

    update_cars = []
    for car in cars_in_period:
        try:
            del car['cpm_name']
            update_cars.append(car)
        except KeyError:
            update_cars.append(car)

    update_cars = sorted(update_cars, key=lambda x: x['license_plate'])

    create_csv(update_cars, f"parkedcars_{machine}", from_date, to_date)


def get_all_fees(log_data: list, from_date: str, to_date: str) -> None:
    """
    Bereken alle fees die betaald zijn van alle machines

    :param log_data: list, lijst met de data
    :param from_date: str, vanaf welke datum berekent moet worden
    :param to_date: str, tot welke datum berekent moet worden
    """
    cars_in_period = get_cars_in_period(log_data, from_date, to_date)

    fees = []
    for car in cars_in_period:
        names = [machine['car_parking_machine'] for machine in fees]
        if car['cpm_name'] not in names:
            fees.append({"car_parking_machine": car['cpm_name'], "total_parking_fee": float(car['parking_fee'])})
        else:
            machine = list(filter(lambda fee: fee['car_parking_machine'] == car['cpm_name'], fees))[0]
            idx = fees.index(machine)
            fees[idx]['total_parking_fee'] += float(car['parking_fee'])

    create_csv(fees, "totalfee", from_date, to_date)


def main() -> None:
    """
    Functie die het hele programma bij elkaar haalt.
    """

    print("""[P] Report all parked cars during a parking period for a specific parking machine
[F] Report total collected parking fee during a parking period for all parking machines
[Q] Quit program""")

    log_cars = read_logfile("carparklog.txt")

    quit_program = False
    while quit_program is False:
        command = input("> ").lower()
        if command in ('q', 'quit'):
            quit_program = True
        elif command in ('p', 'period'):
            user_input = input("> ")
            if "," not in user_input:
                continue
            else:
                machine, from_date, to_date = user_input.split(",")
                get_specific_period(log_cars, machine, from_date, to_date)
        elif command in ('f', 'fee'):
            user_input = input("> ")
            if "," not in user_input:
                continue
            else:
                from_date, to_date = user_input.split(",")
                get_all_fees(log_cars, from_date, to_date)


if __name__ == "__main__":
    main()
