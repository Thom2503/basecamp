from __future__ import annotations
from datetime import datetime, timedelta
import tvlib as tv
import sqlite3


class Expedition:

    def __init__(self, id, name, mountain_id, start, date, country, duration, success) -> None:
        self.id: int = id
        self.name: str = name
        self.mountain_id: int = mountain_id
        self.start: str = start
        self.date: datetime = date
        self.country: str = country
        self.duration: int = duration  # in minuten
        self.success: bool = success

        self.db_conn = sqlite3.connect("climbersapp.db")

    def add_climber(self, climber: Climber) -> None:
        """
        Voeg een climber toe aan de expedition door het id
        van de meegegeven climber object te gebruiken

        :param climber: Climber, de climber die je wilt toevoegen
        """
        cur = self.db_conn.cursor()
        sq_add_climber = """
            INSERT OR REPLACE INTO `expedition_climbers`
            (`climber_id`, `expedition_id`)
            VALUES (:cid, :eid)
        """
        cur.execute(sq_add_climber, {'cid': climber.id, 'eid': self.id})
        self.db_conn.commit()

    def get_climbers(self) -> list[Climber]:
        """
        Maak een list van de climbers die mee hebben
        gedaan aan deze expedition

        :return climbers: list, lijst van climbers die mee hebben gedaan
        """
        from climber import Climber

        climbers = []

        cur = self.db_conn.cursor()
        sq_select_climbers = """
            SELECT `climbers`.*
              FROM `climbers`
              LEFT JOIN `expedition_climbers`
              ON `expedition_climbers`.`climber_id` = `climbers`.`id`
              WHERE `expedition_climbers`.`expedition_id` = :eid
        """
        output = cur.execute(sq_select_climbers, {'eid': self.id})
        result = output.fetchall()

        for row in result:
            # Maak een dictionary van de row om het makkelijker en duidelijk te kunnen gebruiken
            dict_row = {output.description[i][0]: row[i] for i in range(len(row))}
            climber = Climber(dict_row['id'],
                              dict_row['first_name'],
                              dict_row['last_name'],
                              dict_row['nationality'],
                              dict_row['date_of_birth'])
            climbers.append(climber)

        return climbers

    def get_mountain(self) -> Mountain:
        """
        Krijg de berg van de de expedition

        :return mountain: Mountain, de berg van de expedition
        """
        from mountain import Mountain

        cur = self.db_conn.cursor()
        sq_select_mountain = """
            SELECT `mountains`.*
              FROM `mountains`
              LEFT JOIN `expeditions`
              ON `mountains`.`id` = `expeditions`.`mountain_id`
              WHERE `expeditions`.`id` = :eid
        """
        output = cur.execute(sq_select_mountain, {'eid': self.id})
        result = output.fetchone()
        dict_row = {output.description[i][0]: result[i] for i in range(len(result))}

        mountain = Mountain(dict_row['id'],
                            dict_row['name'],
                            dict_row['country'],
                            dict_row['rank'],
                            dict_row['height'],
                            dict_row['prominence'],
                            dict_row['range'])

        return mountain

    def convert_date(self, to_format: str) -> str:
        """
        Verander de date van de expedition naar een string
        gebaseerd op de meegegeven format.

        :param to_format: str, de format waarnaar het veranderd moet worden

        :return converted: str, de veranderde date string
        """
        return tv.time_to_str(self.date, to_format)

    def convert_duration(self, to_format: str) -> str:
        """
        Verander duration van minuten naar een string
        gebaseerd op de meegegeven format.

        :param to_format: str, format om naar te veranderen

        :return converted: str, de veranderde duration string
        """
        # maak een timedelta object zodat we er berekeningen mee kunnen doen
        td = timedelta(minutes=self.duration)
        # haal de dagen uit de secondes
        days, seconds = divmod(td.total_seconds(), 86400)  # 86400 is het aantal secondes in een dag
        hours, rem = divmod(seconds, 3600)  # haal het aantal uur uit de secondes
        minutes, seconds = divmod(rem, 60)  # haal het aantal minuten uit de secondes

        # maak er een datetime object van zodat we het kunnen formaten
        # jaar, maand en dag op begin van unix tijd maar maakt niks uit
        # wat daar komt
        dt = datetime(1970, 1, 1, int(hours), int(minutes), int(seconds))
        return tv.time_to_str(dt, to_format)

    # Representation method
    # This will format the output in the correct order
    # Format is @dataclass-style: Classname(attr=value, attr2=value2, ...)
    def __repr__(self) -> str:
        return "{}({})".format(type(self).__name__, ", ".join([f"{key}={value!r}" for key, value in self.__dict__.items()]))