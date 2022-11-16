from datetime import datetime

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
        self.id = id

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

    def get_checked_in_cars(self, name: str, action: str = "check-in") -> dict:
        """
        Zoek alle autos die ingecheckt zijn in deze garage.
        """
        parked_cars = {}
        with open("carparklog.txt", "r") as file:
            log_lines = file.readlines()
            for line in log_lines:
                line_data = {}
                for data in line.split(";"):
                    try:
                        data_name, data_value = data.split("=")
                        line_data.update({data_name: data_value.replace("\n", "")})
                    except ValueError:
                        line_data.update({"time": data})

                if line_data['cpm_name'] == name and line_data['action'] == action:
                    parked_cars.update({line_data['license_plate']: line_data['time']})

        return parked_cars

    def get_machine_fee_by_day(self, name: str, date: str) -> float:
        """
        Geef het totaal aantal aan parking fees terug als float op
        basis van de naam en gegeven datum
        """
        # check of de datum correct is die is meegegeven
        if DateTimeHelper.is_correct_format(date) is False:
            return 0.0

        checked_out_cars = self.get_checked_in_cars(name, "check-out")
        checked_in_cars = self.get_checked_in_cars(name)


class ParkedCar:
    """
    Class voor een geparkeerde auto met een tijd van inchecken en kenteken.
    """

    def __init__(self, license, checked_in):
        self.license: str = license
        self.checked_in: datetime = checked_in


class CarParkingMachine:
    """
    Class waar bijgehouden wordt welke auto's er ingecheckt zijn, je kan inchecken,
    uitchecken en dan krijg je een prijs terug.
    """

    def __init__(self, capacity=10, hourly_rate=2.50, parked_cars={}, id=""):
        self.capacity: int = capacity
        self.hourly_rate: float = hourly_rate
        self.parked_cars: dict = parked_cars
        self.id: str = id

        self.logger = CarParkingLogger(self.id)

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
        current_hour = DateTimeHelper.round_up(DateTimeHelper.get_now()).hour
        current_day = DateTimeHelper.round_up(DateTimeHelper.get_now()).day

        parked_car_hour = parked_car_obj.checked_in.hour
        parked_car_day = parked_car_obj.checked_in.day

        # bereken hoeveel uur de auto geparkeerd is.
        hours_parked = current_hour - parked_car_hour

        # als de dag anders is maar de uren hetzelfde of meer is het hoogstwaarschijnlijk >24 uur
        if current_day != parked_car_day and current_hour >= parked_car_hour:
            fee = self.hourly_rate * 24
        # als het resultaat 0 is moet je nog wel een tarief betalen
        elif hours_parked == 0:
            fee = self.hourly_rate
        else:
            fee = hours_parked * self.hourly_rate

        return fee

    def check_in(self, license_plate: str, check_in: datetime = DateTimeHelper.get_now()) -> bool:
        # check of het al vol is
        if len(self.parked_cars) == self.capacity:
            return False

        # check of de auto niet al is geparkeerd
        if license_plate in self.parked_cars.keys():
            return False

        # maak een nieuw geparkeerde auto object aan.
        parked_car = ParkedCar(license_plate, check_in)
        # voeg de nieuwe auto toe aan de parked_cars dictionary
        self.parked_cars.update({license_plate: parked_car})

        # log het inchecken met de CarParkingLogger object
        self.logger.log_action(license_plate, "check-in", check_in)

        return True

    def check_out(self, license_plate: str) -> float:
        if license_plate in self.parked_cars.keys():
            parking_fee = self.get_parking_fee(license_plate)
            self.parked_cars.pop(license_plate)
            # log het uitchecken met de CarParkingLogger object
            self.logger.log_action(license_plate, "check-out", DateTimeHelper.get_now(), parking_fee)
            return parking_fee
        else:
            return 0

    def update_parked_cars(self):
        """
        Update de dictionary met de autos die in de log staan
        """
        logged_cars = self.logger.get_checked_in_cars(self.id)

        for license_plate, time in logged_cars.items():
            time = DateTimeHelper.str_to_time(time)
            new_parked = ParkedCar(license_plate, time)

            self.parked_cars.update({license_plate: new_parked})


def main():
    # build menu structure as following
    # the input can be case-insensitive (so E and e are valid inputs)
    # [I] Check-in car by license plate
    # [O] Check-out car by license plate
    # [Q] Quit program
    parking_machine = CarParkingMachine(id="West")
    parking_machine.update_parked_cars()
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
