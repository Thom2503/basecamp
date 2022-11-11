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

    def __init__(self, capacity=10, hourly_rate=2.50, parked_cars={}):
        self.capacity: int = capacity
        self.hourly_rate: float = hourly_rate
        self.parked_cars: dict = parked_cars

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
            return self.hourly_rate * 24
        # als het resultaat 0 is moet je nog wel een tarief betalen
        elif hours_parked == 0:
            return self.hourly_rate

        return hours_parked * self.hourly_rate

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
        return True

    def check_out(self, license_plate: str) -> float:
        if license_plate in self.parked_cars.keys():
            parking_fee = self.get_parking_fee(license_plate)
            self.parked_cars.pop(license_plate)
            return parking_fee
        else:
            return 0


def main():
    # build menu structure as following
    # the input can be case-insensitive (so E and e are valid inputs)
    # [I] Check-in car by license plate
    # [O] Check-out car by license plate
    # [Q] Quit program
    parking_machine = CarParkingMachine()
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
