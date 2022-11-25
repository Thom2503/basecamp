from datetime import datetime, timedelta
import json
import os

# ParkedCar class to store information of parked cars.


class DateTimeHelper:
    """
    Class voor dingen die te maken hebben met datetime
    """

    @staticmethod
    def round_up(time: datetime) -> datetime:
        """
        Rond het uur naar boven af.
        """
        return time.replace(second=0, microsecond=0, minute=0, hour=time.hour+1)

    @staticmethod
    def get_now() -> datetime:
        """
        Static method om de huidige datetime te krijgen.
        Mainly gemaakt om makkelijk te testen.
        """
        return datetime.now()

    @staticmethod
    def time_to_str(time: datetime, format: str = "%d-%m-%Y %H:%M:%S") -> str:
        """
        Verander de datetime naar een leesbare string
        gebaseerd op de meegegeven format
        """
        return time.strftime(format)

    @staticmethod
    def str_to_time(date_str: str, format: str = "%d-%m-%Y %H:%M:%S") -> datetime:
        """
        Maak een datetime object van een gegeven date_str en format.
        """
        return datetime.strptime(date_str, format)

    @staticmethod
    def is_correct_format(date_str: str, format: str = "%d-%m-%Y") -> bool:
        """
        Check of het gegeven date string correct is op basis van de format
        """
        return bool(datetime.strptime(date_str, format))


class CarParkingLogger:
    """
    Logger class om bij te houden welke autos in welke garage zijn
    ingecheckt en uitgecheckt.
    """
    def __init__(self, id=""):
        self.id: str = id

    def log_action(self, license_plate: str, action: str, time: datetime, fee: float = 0.0):
        """
        Voeg een actie toe aan een log bestand.
        """
        action_text = "check-in"
        if action == "check-out":
            action_text = f"check-out;parking_fee={fee}"

        utc_date = DateTimeHelper.time_to_str(time)

        log_text = \
            f"{utc_date};cpm_name={self.id};license_plate={license_plate};action={action_text}\n"

        with open("carparklog.txt", "a") as log_file:
            log_file.write(log_text)

    def get_checked_in_cars(self, name: str, action: str = "check-in", all_cpm: bool = False) -> dict:
        """
        Zoek alle autos die ingecheckt zijn in deze garage.
        """
        parked_cars = {}
        with open("carparklog.txt", "r") as file:
            log_lines = file.readlines()
            car_no = 0  # om bij te houden welk nummer in de log line het is voor het uitlezen

            # loop door alle lines in de logfile om per line de verschillende data in een dictionary
            # te stoppen zodat die gebruikt kan worden om parked_cars te vullen
            for line in log_lines:
                line_data = {}

                # lees de verschillende data en stop die in een dictionary voor deze specifieke lijn
                for data in line.split(";"):
                    try:
                        data_name, data_value = data.split("=")
                        line_data.update({data_name: data_value.replace("\n", "")})
                    except ValueError:
                        line_data.update({"time": data})

                # check of de naam klopt uit de data en de functie parameter dan kan je door
                # behalve als je alle meters wilt uitlezen bij bijvoorbeeld get_total_car_fee()
                if line_data['cpm_name'] == name or all_cpm is True:

                    # als de actie niet check in is wil ik de data krijgen van de auto
                    # en dan specifiek de tijd en de parking fee om die te gebruiken in andere methods
                    if action != "check-in":
                        try:
                            check_out_data = [line_data['time'], line_data['parking_fee']]
                            # de key van de license_plate is met een # en een nummer toegevoegd
                            # omdat een auto in meerdere keren uitgecheckt kan zijn en die moet je dan
                            # niet de hele tijd overschrijven
                            parked_cars.update({line_data['license_plate'] + "#" + str(car_no): check_out_data})
                        except KeyError:
                            continue
                    else:
                        # als de auto in de data al is een keertje is gevonden en dit keer checkt die uit
                        # mag je hem uit de uiteindelijke parked cars dictionary halen want die data
                        # is niet meer nodig
                        if line_data['license_plate'] in parked_cars.keys() and line_data['action'] == "check-out":
                            parked_cars.pop(line_data['license_plate'])
                        else:
                            license = line_data['license_plate']
                            date_time = DateTimeHelper.str_to_time(line_data['time'])

                            # maak gelijk ook een object van de auto zodat het gelijk in CarParkingMachine
                            # te gebruiken is
                            parked_cars.update({line_data['license_plate']: ParkedCar(license, date_time)})
                car_no += 1

        return parked_cars

    def get_machine_fee_by_day(self, name: str, date: str) -> float:
        """
        Geef het totaal aantal aan parking fees terug als float op
        basis van de naam en gegeven datum
        """
        sum_fee = 0.0
        # check of de datum correct is die is meegegeven
        if DateTimeHelper.is_correct_format(date) is False:
            return 0.0

        checked_out_cars = self.get_checked_in_cars(name, "check-out")

        for license, data in checked_out_cars.items():
            # check of de data een list is zodat je die kan gebruiken
            if isinstance(data, list):
                # zorg dat de datum in de data veranderd word zodat het
                # vergeleken kan worden met de parameter
                str_to_date = DateTimeHelper.str_to_time(data[0])
                correct_date = DateTimeHelper.time_to_str(str_to_date, "%d-%m-%Y")
                if correct_date == date:
                    sum_fee += float(data[1])

        return round(sum_fee, 2)

    def get_total_car_fee(self, license_plate: str) -> float:
        """
        Bereken het totaal aantal fee van een geparkeerde auto
        """
        sum_fee = 0.0
        checked_out_cars = self.get_checked_in_cars(self.id, "check-out", True)

        for license, data in checked_out_cars.items():
            # split op de # en haal het eerste uit de lijst want dat
            # is de data die we moeten gebruiken om te kunnen filteren
            license = license.split("#")[0]
            if isinstance(data, list) and license == license_plate:
                sum_fee += float(data[1])

        return round(sum_fee, 2)


class ParkedCar:
    """
    Class voor een geparkeerde auto met een tijd van inchecken en kenteken.
    """

    def __init__(self, license, check_in):
        self.license: str = license
        self.check_in: datetime = check_in


class CarParkingMachine:
    """
    Class waar bijgehouden wordt welke auto's er ingecheckt zijn, je kan inchecken,
    uitchecken en dan krijg je een prijs terug.
    """

    def __init__(self, capacity=10, hourly_rate=2.50, parked_cars={}, id=""):
        self.capacity: int = capacity
        self.hourly_rate: float = hourly_rate
        self.id: str = id

        self.file_path: str = f"{self.id}_state.json"

        self.logger = CarParkingLogger(self.id)

        self.parked_cars = self.read_json(self.file_path)

    @staticmethod
    def read_json(file_path: str) -> dict:
        """
        Method om de json te lezen voor een specifiek machine

        :param file_path: str, pad naar het bestand

        :return cars: dict, alle auto's in de json file
        """
        file_content = []
        cars = {}

        try:
            with open(file_path, "rb") as file:
                file_content = json.load(file)

            # maak de list met dictionaries een dictionary zoals
            # het in self.parked_cars moet komen te staan
            for item in file_content:
                check_in = DateTimeHelper.str_to_time(item['check_in'])
                license_plate = item['license_plate']
                cars.update({license_plate: ParkedCar(license_plate, check_in)})

            return cars
        except FileNotFoundError:
            return {}

    def write_json(self) -> None:
        """
        Schrijf de parked cars naar de json file
        """
        cars = []

        # maak van de dictionary een lijst met dictionaries
        # zodat het in json gedumped kan worden
        for license_plate, car_obj in self.parked_cars.items():
            check_in = DateTimeHelper.time_to_str(car_obj.check_in)
            cars.append({"license_plate": license_plate, "check_in": check_in})

        json_data = json.dumps(cars, indent=4)
        with open(self.file_path, "w") as out_file:
            out_file.write(json_data)

    def get_other_parked_cars(self) -> dict:
        """
        Method om alle andere geparkeerde auto's die geparkeerd staan in
        de andere parkeer garages

        :return other_cars: dict, alle andere auto's
        """
        other_cars = {}

        # haal alle bestand namen op die met json eindigen om daar
        # de geparkeerde auto's uit te kunnen halen
        all_files = [file for file in os.listdir() if os.path.splitext(file)[1] == ".json"]

        # loop door die bestanden heen en voeg die aan de dictionary toe
        # behalve als dat hetzelfde bestand is als de huidige machine.
        for file in all_files:
            if file != self.file_path:
                cars = CarParkingMachine.read_json(file)
                other_cars.update(cars)

        return other_cars

    def get_parking_fee(self, license_plate: str) -> float:
        """
        Functie om het tarief te berekenen op basis hoe lang de
        auto geparkeerd is.
        """
        # zoek de object op in de parked_cars dictionary om
        # het tarief te kunnen berekenen.
        parked_car_obj = self.parked_cars[license_plate]
        if parked_car_obj is None:
            return 0.0

        # haal de huidige datetime en die van de auto op
        # zodat je het tarief kan berekenen. Rond de uren van nu ook naar boven af.
        current_hour = DateTimeHelper.round_up(DateTimeHelper.get_now())
        parked_car_time = parked_car_obj.check_in

        # bereken hoeveel uur de auto geparkeerd is.
        parked_diff = current_hour - parked_car_time
        hours_parked = parked_diff.total_seconds() / 3600
        # rond de hours_parked naar boven af om een heel uur te maken voor de minuten enz.
        # dit kan met bijvoorbeeld -(-2//3) zonder de math module (dit zou ik nooit zo doen...)
        hours_parked = -(-hours_parked//1)

        # als de dag anders is maar de uren hetzelfde of meer is het hoogstwaarschijnlijk >24 uur
        if hours_parked >= 24:
            fee = self.hourly_rate * 24
        # als het resultaat 0 is moet je nog wel een tarief betalen
        elif hours_parked == 0:
            fee = self.hourly_rate
        else:
            fee = hours_parked * self.hourly_rate

        return fee

    def check_in(self, license_plate: str, check_in: datetime = DateTimeHelper.get_now()) -> bool:
        # haal alle autos op die in andere garages staan om mee te checken
        other_cars = self.get_other_parked_cars()

        # check of het al vol is
        if len(self.parked_cars) == self.capacity:
            return False

        if license_plate in other_cars.keys():
            return False

        if license_plate in self.parked_cars.keys():
            return False

        # maak een nieuw geparkeerde auto object aan.
        parked_car = ParkedCar(license_plate, check_in)
        # voeg de nieuwe auto toe aan de parked_cars dictionary
        self.parked_cars.update({license_plate: parked_car})

        # log het inchecken met de CarParkingLogger object
        self.logger.log_action(license_plate, "check-in", check_in)

        # update het json bestand
        self.write_json()

        return True

    def check_out(self, license_plate: str) -> float:
        if license_plate in self.parked_cars.keys():
            parking_fee = self.get_parking_fee(license_plate)
            self.parked_cars.pop(license_plate)
            # log het uitchecken met de CarParkingLogger object
            self.logger.log_action(license_plate, "check-out", DateTimeHelper.get_now(), parking_fee)

            # update het json bestand
            self.write_json()
            return parking_fee
        else:
            return 0


def main():
    parking_machine = CarParkingMachine(id="West")
    print("""Welcome to the parking garage!
[I] Check-in car by license plate
[O] Check-out car by license plate
[Q] Quit program""")
    # om bij te houden of je het programma kan afsluiten
    quit_program = False
    while quit_program is False:
        command = input("> ").lower()
        if command in ('q', 'quit'):
            quit_program = True
        elif command in ('i'):
            user_license = input("Give a license to check in:\n> ")
            if user_license != "":
                new_parked = parking_machine.check_in(user_license, DateTimeHelper.get_now())
            if new_parked is not False:
                print("License registered")
            else:
                print("Capacity reached!")
        elif command in ('o'):
            user_license = input("Give a license to check out:\n> ")
            if user_license != "":
                check_out = parking_machine.check_out(user_license)

            # toon het tarief als het hoger dan nul is anders is
            # er geen geparkeerde auto gevonden.
            if check_out > 0:
                print(f"Parking fee: {check_out:.2f} EUR")
            else:
                print(f"{user_license} not found")
        else:
            print("Invalid command!")


if __name__ == "__main__":
    main()
