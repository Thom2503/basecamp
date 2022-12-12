from datetime import datetime, timedelta
import json
import os
import sqlite3
import sys

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


class ParkedCar:
    """
    Class voor een geparkeerde auto met een tijd van inchecken en kenteken.
    """

    def __init__(self, id: int, license_plate: str, check_in: datetime, check_out: datetime, parking_fee: float):
        self.id: int = id
        self.license_plate: str = license_plate
        self.check_in: datetime = check_in
        self.check_out: datetime = check_out
        self.parking_fee: float = parking_fee


class CarParkingMachine:
    """
    Class waar bijgehouden wordt welke auto's er ingecheckt zijn, je kan inchecken,
    uitchecken en dan krijg je een prijs terug.
    """

    def __init__(self, capacity=10, hourly_rate=2.50, parked_cars={}, id=""):
        self.capacity: int = capacity
        self.hourly_rate: float = hourly_rate
        self.id: str = id

        self.db_conn = sqlite3.connect(os.path.join(sys.path[0], 'carparkingmachine.db'))
        self.db_conn.execute(
            '''CREATE TABLE IF NOT EXISTS parkings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                car_parking_machine TEXT NOT NULL,
                license_plate TEXT NOT NULL,
                check_in TEXT NOT NULL,
                check_out TEXT DEFAULT NULL,
                parking_fee NUMERIC DEFAULT 0
            );'''
        )

        def get_all_cars() -> dict:
            """
            Haal alle ingecheckde autos op die in de database staan zodat die
            gelijk aan parked_cars toegevoegd kunnen worden.

            :return parked_cars: dict, dictionary met de ingecheckde autos
            """
            parked_cars = {}

            sq_query = "SELECT * FROM `parkings` WHERE `car_parking_machine` = :cpm AND `check_out` IS NULL"
            output = self.db_conn.execute(sq_query, {'cpm': self.id})
            result = output.fetchall()
            # als het leeg is return een lege dictionary
            if len(result) == 0:
                return parked_cars

            for row in result:
                # Maak een dictionary van de row om het makkelijker en duidelijk te kunnen gebruiken
                dict_row = {output.description[i][0]: row[i] for i in range(len(row))}
                id = dict_row['id']
                license_plate = dict_row['license_plate']
                check_in = DateTimeHelper.str_to_time(dict_row['check_in'], "%Y-%m-%d %H:%M:%S.%f")

                parked_cars.update({license_plate: ParkedCar(id, license_plate, check_in, None, 0)})

            return parked_cars

        self.parked_cars: dict = get_all_cars()

    def find_by_id(self, id: int) -> ParkedCar:
        """
        Zoek naar het id in de table en geef een ParkedCar
        object terug met de goede data.

        :param self, huidige object
        :param id: int, id waar het object van gemaakt moet worden

        :return ParkedCar, object met de goede data
        """
        sq_find_car = \
            "SELECT * FROM `parkings` WHERE `id` = :id and `car_parking_machine` = :cpm"
        result = self.db_conn.execute(sq_find_car, {'id': id, 'cpm': self.id}).fetchone()

        license_plate = result[2]
        check_in = DateTimeHelper.str_to_time(result[3], "%Y-%m-%d %H:%M:%S.%f")
        check_out = DateTimeHelper.str_to_time(result[4], "%Y-%m-%d %H:%M:%S.%f") if result[4] is not None else None
        parking_fee = result[5]

        return ParkedCar(id, license_plate, check_in, check_out, parking_fee)

    def find_last_checkin(self, license_plate: str) -> int:
        """
        Zoek de laatste row van een auto met license_plate die niet uitgecheckt is.

        :param self, huidige object
        :param license_plate: str, kentekenplaat waar je op moet zoeken.

        :return id: int, id van de gevonden auto
        """
        sq_find_car = """
            SELECT `id` FROM `parkings`
            WHERE `license_plate` = :license
                AND `car_parking_machine` = :cpm
                AND `check_out` IS NULL
            LIMIT 1;
        """
        result = self.db_conn.execute(sq_find_car, {'license': license_plate, 'cpm': self.id}).fetchone()

        return int(result[0])

    def insert(self, parked_car: ParkedCar) -> ParkedCar:
        """
        Voeg de ParkedCar object toe aan de database zodat je het goede id kan krijgen

        :param self, huidige object
        :param parked_car: ParkedCar, auto object om toe te voegen

        :return ParkedCar, nieuwe object met goede id
        """
        sq_insert_car = """
            INSERT INTO `parkings`
            (`car_parking_machine`, `license_plate`, `check_in`, `check_out`, `parking_fee`)
            VALUES
            (:cpm, :license_plate, :check_in, :check_out, :parking_fee)
        """
        sq_data = {**{'cpm': self.id}, **parked_car.__dict__}
        self.db_conn.execute(sq_insert_car, sq_data)
        self.db_conn.commit()

        last_car = self.find_last_checkin(sq_data['license_plate'])
        last_car_obj = self.find_by_id(last_car)

        return last_car_obj

    def update(self, parked_car: ParkedCar) -> None:
        """
        Update de database row op basis van de ParkedCar object
        de id in de row is ParkedCar.id.

        :param self, huidige object
        :param parked_car: ParkedCar, object vanwaar die geupdatet moet worden
        """
        sq_update_car = """
            UPDATE `parkings` SET
                `car_parking_machine` = :cpm,
                `license_plate` = :license_plate,
                `check_in` = :check_in,
                `check_out` = :check_out,
                `parking_fee` = :parking_fee
            WHERE `id` = :id
        """
        sq_data = {**{'cpm': self.id}, **parked_car.__dict__}
        self.db_conn.execute(sq_update_car, sq_data)
        self.db_conn.commit()

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
        # check of het al vol is
        if len(self.parked_cars) == self.capacity:
            return False

        if license_plate in self.parked_cars.keys():
            return False

        # maak een nieuw geparkeerde auto object aan.
        # parked_car = ParkedCar(0, license_plate, check_in, None, None)
        parked_car = self.insert(ParkedCar(0, license_plate, check_in, None, 0))
        # voeg de nieuwe auto toe aan de parked_cars dictionary
        self.parked_cars.update({license_plate: parked_car})

        return True

    def check_out(self, license_plate: str) -> float:
        if license_plate in self.parked_cars.keys():
            parking_fee = self.get_parking_fee(license_plate)

            car_obj = self.find_by_id(self.find_last_checkin(license_plate))
            car_obj.check_out = datetime.now()
            car_obj.parking_fee = parking_fee
            self.update(car_obj)

            self.parked_cars.pop(license_plate)

            return parking_fee
        else:
            return 0


def main():
    parking_machine = CarParkingMachine(id="North")
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
    parking_machine.close()


if __name__ == "__main__":
    main()
