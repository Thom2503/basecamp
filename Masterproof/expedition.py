from datetime import datetime
import tvlib as tv
import sqlite3

db_conn = sqlite3.connect("climbersapp.db")


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

    def add_climber(self, climber: object) -> None:
        """
        Voeg een climber toe aan de expedition door het id
        van de meegegeven climber object te gebruiken

        :param climber: Climber, de climber die je wilt toevoegen
        """
        cur = db_conn.cursor()
        sq_add_climber = """
            INSERT OR REPLACE INTO `expedition_climbers`
            (`climber_id`, `expedition_id`)
            VALUES (:cid, :eid)
        """
        cur.execute(sq_add_climber, {'cid': climber.id, 'eid': self.id})
        db_conn.commit()

    def get_climbers(self) -> list:
        """
        Maak een list van de climbers die mee hebben
        gedaan aan deze expedition

        :return climbers: list, lijst van climbers die mee hebben gedaan
        """
        from climber import Climber

        climbers = []

        cur = db_conn.cursor()
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

    def get_mountain(self) -> object:
        """
        Krijg de berg van de de expedition

        :return mountain: Mountain, de berg van de expedition
        """
        from mountain import Mountain

        cur = db_conn.cursor()
        sq_select_mountain = """
            SELECT DISTINCT `mountains`.*
              FROM `mountains`
              LEFT JOIN `expeditions`
              ON `mountains`.`id` = `expeditions`.`mountain_id`
              WHERE `mountains`.`id` = :mid
        """
        output = cur.execute(sq_select_mountain, {'mid': self.mountain_id})
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
        # als de date in het object een string is
        # moet het eerst naar een datetime object veranderd worden
        if isinstance(self.date, str):
            self.date = tv.str_to_time(self.date, "%Y-%m-%d")

        return tv.time_to_str(self.date, to_format)

    def convert_duration(self, to_format: str) -> str:
        """
        Verander duration van minuten naar een string
        gebaseerd op de meegegeven format.

        :param to_format: str, format om naar te veranderen

        :return converted: str, de veranderde duration string
        """
        # haal de dagen en wat over is uit de duration
        # zodat daar verder mee gerekent kan worden
        days, minutes = divmod(self.duration, 1440)
        if to_format == "%H:%M":
            # bereken het uur en de overgebleven minuten uit de overgebleven
            # minuten van de dag
            hours, minutes = divmod(minutes % 1440, 60)  # haal het aantal uur uit de minuten
            hours += (days * 24)  # stop het aantal uur van een dag weer in het uur

            # verplaats alle format string met de uur en minuten
            return to_format.replace("%H", f"{hours:02d}").replace("%M", f"{minutes:02d}")
        else:
            hours, minutes = divmod(minutes, 60)  # haal het aantal uur uit de minuten
            return to_format.replace("%D", f"{days:02d}").replace("%H", f"{hours:02d}").replace("%M", f"{minutes:02d}")

    # Representation method
    # This will format the output in the correct order
    # Format is @dataclass-style: Classname(attr=value, attr2=value2, ...)
    def __repr__(self) -> str:
        return "{}({})".format(type(self).__name__, ", ".join([f"{key}={value!r}" for key, value in self.__dict__.items()]))