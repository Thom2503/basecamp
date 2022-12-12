from datetime import datetime
import csv
import sqlite3


def create_csv(data: list, file_name: str) -> None:
    """
    Converteer de data naar een csv bestand

    :param data: list, de data die in csv moet komen
    :param file_name: str, de naam van het csv bestand
    """
    # headers die csv nodig heeft
    headers = data[0].keys()

    with open(file_name, "w") as out_file:
        writer = csv.DictWriter(out_file, headers, delimiter=';')
        writer.writeheader()
        writer.writerows(data)


def get_specific_period(cur: object, machine: str, from_date: str, to_date: str) -> None:
    """
    Filter alle data op basis van de machine en de from_date en to_date, daar zou
    dan een lijst met dictionaries uit komen met alle data van een bepaalde datum
    tot een bepaalde datum.

    :param cur: object, cursor voor de sql queries
    :param machine: str, op welke machine gefilterd moet worden
    :param from_date: str, vanaf welke datum
    :param to_date: str, tot welke datum
    """
    update_cars = []
    sq_query = """
        SELECT `license_plate`,
               `check_in` as `checked_in`,
               `check_out` as `checked_out`,
               `parking_fee`
         FROM `parkings`
         WHERE `car_parking_machine` = :cpm
          AND (`check_in` BETWEEN :from AND :to)
          AND (`check_out` BETWEEN :from AND :to);
    """
    output = cur.execute(sq_query, {'cpm': machine, 'to': to_date, 'from': from_date})
    result = output.fetchall()
    for row in result:
        row_dict = {output.description[i][0]: row[i] for i in range(len(row))}
        update_cars.append(row_dict)

    update_cars = sorted(update_cars, key=lambda x: x['checked_out'])

    create_csv(update_cars[::-1], f"parkedcars_{machine}_from_{from_date}_to_{to_date}.csv")


def get_all_fees(cur: object, from_date: str, to_date: str) -> None:
    """
    Bereken alle fees die betaald zijn van alle machines

    :param cur: object, cursor voor de sql queries
    :param from_date: str, vanaf welke datum berekent moet worden
    :param to_date: str, tot welke datum berekent moet worden
    """
    fees = []
    sq_query = """
        SELECT `car_parking_machine`, SUM(`parking_fee`) as `total_parking_fee`
         FROM `parkings`
         WHERE (`check_in` BETWEEN :from AND :to)
          AND (`check_out` BETWEEN :from AND :to)
         GROUP BY `car_parking_machine`;
    """
    output = cur.execute(sq_query, {'from': from_date, 'to': to_date})
    result = output.fetchall()
    for row in result:
        row_dict = row_dict = {output.description[i][0]: row[i] for i in range(len(row))}
        fees.append(row_dict)

    create_csv(fees, f"totalfee_from_{from_date}_to_{to_date}.csv")


def get_specific_car(cur: object, license_plate: str) -> None:
    """
    Maak een csv bestand van data uit de database van de
    meegegeven license_plate.

    :param cur: object, cursor voor de sql queries
    :param license_plate: str, license plate waar je op wilt zoeken
    """
    car_checks = []

    sq_query = """
        SELECT `car_parking_machine`,
               `check_in`,
               `check_out`,
               `parking_fee`
         FROM `parkings`
         WHERE `license_plate` = :license_plate;
    """
    output = cur.execute(sq_query, {'license_plate': license_plate})
    result = output.fetchall()
    for row in result:
        row_dict = row_dict = {output.description[i][0]: row[i] for i in range(len(row))}
        car_checks.append(row_dict)

    create_csv(car_checks[::-1], f"all_parkings_for_{license_plate}.csv")


def main() -> None:
    """
    Functie die het hele programma bij elkaar haalt.
    """

    print("""[P] Report all parked cars during a parking period for a specific parking machine
[F] Report total collected parking fee during a parking period for all parking machines
[C] Report all complete parkings over all parking machines for a specific car
[Q] Quit program""")
    con = sqlite3.connect("carparkingmachine.db")
    cur = con.cursor()

    quit_program = False
    while quit_program is False:
        command = input("> ").lower()
        if command in ('q', 'quit'):
            quit_program = True
        elif command in ('p', 'period'):
            user_input = input("period > ")
            if "," not in user_input:
                continue
            else:
                machine, from_date, to_date = user_input.split(",")
                get_specific_period(cur, machine, from_date, to_date)
        elif command in ('f', 'fee'):
            user_input = input("fee > ")
            if "," not in user_input:
                continue
            else:
                from_date, to_date = user_input.split(",")
                get_all_fees(cur, from_date, to_date)
        elif command in ('c', 'complete'):
            user_input = input("license plate > ")
            get_specific_car(cur, user_input)


if __name__ == "__main__":
    main()
