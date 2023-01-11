from __future__ import annotations
from datetime import datetime, date
import sqlite3


class Climber:

    def __init__(self, id, first_name, last_name, nationality, date_of_birth) -> None:
        self.id: int = id
        self.first_name: str = first_name
        self.last_name: str = last_name
        self.nationality: str = nationality
        self.date_of_birth: datetime = date_of_birth

        self.db_conn = sqlite3.connect("climbersapp.db")

    def get_age(self) -> int:
        """
        Bereken de leeftijd van een climber

        :return age: int, leeftijd van de climber
        """
        today = date.today()
        age = today.year - self.date_of_birth.year
        # voor correctie als het vandaag onder de geboorte dag is
        # als vandaag de maand en dag kleiner zijn dan de geboorte maand en dag
        # krijg je true en dan word er 1 van de jaren afgehaald
        age -= ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        return age

    def get_expeditions(self) -> list[Expedition]:
        """
        Maak een lijst met expedition objects van deze climber

        :return expeditions: list, lijst met de expeditons van de climber
        """
        from expedition import Expedition
        cur = self.db_conn.cursor()

        expeditions = []
        sq_get_expeditions = """
            SELECT `expeditions`.* FROM `expeditions`
              LEFT JOIN `expedition_climbers`
              ON `expedition_climbers`.`expedition_id` = `expeditions`.`id`
              WHERE `expedition_climbers`.`climber_id` = :cid
        """
        output = cur.execute(sq_get_expeditions, {'cid': self.id})
        result = output.fetchall()

        for row in result:
            # Maak een dictionary van de row om het makkelijker en duidelijk te kunnen gebruiken
            dict_row = {output.description[i][0]: row[i] for i in range(len(row))}
            expedition = Expedition(dict_row['id'],
                                    dict_row['name'],
                                    dict_row['mountain_id'],
                                    dict_row['start_location'],
                                    dict_row['date'],
                                    dict_row['country'],
                                    dict_row['duration'],
                                    dict_row['success'])
            expeditions.append(expedition)
        return expeditions

    # Representation method
    # This will format the output in the correct order
    # Format is @dataclass-style: Classname(attr=value, attr2=value2, ...)
    def __repr__(self) -> str:
        return "{}({})".format(type(self).__name__, ", ".join([f"{key}={value!r}" for key, value in self.__dict__.items()]))