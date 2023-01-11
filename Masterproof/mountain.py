from __future__ import annotations
import sqlite3


class Mountain:

    def __init__(self, id, name, country, rank, height, prominence, range) -> None:
        self.id: int = id
        self.name: str = name
        self.country: str = country
        self.rank: int = rank
        self.height: int = height
        self.prominence: int = prominence
        self.range: str = range

        self.db_conn = sqlite3.connect("climbersapp.db")

    def height_difference(self) -> int:
        """
        Bereken het verschil tussen de prominence en de height
        """
        return self.height - self.prominence

    def get_expeditions(self) -> list[Expedition]:
        """
        Zoek alle expeditons die op deze berg gedaan zijn.

        :return expeditons: list, lijst met de expeditons
        """
        from expedition import Expedition

        expeditions = []

        cur = self.db_conn.cursor()
        sq_get_expeditions = """
            SELECT * FROM `expeditions`
              WHERE `mountain_id` = :mid
        """
        output = cur.execute(sq_get_expeditions, {'mid': self.id})
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