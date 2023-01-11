from climber import Climber as Climber
from mountain import Mountain as Mountain
from expedition import Expedition as Expedition
from datetime import datetime
from dataclasses import dataclass
import sqlite3
import tvlib as tv


@dataclass
class Reporter:
    db_conn: object = sqlite3.connect("climbersapp.db")
    cur: object = db_conn.cursor()

    # How many climbers are there? -> int
    def total_amount_of_climbers(self) -> int:
        """
        Zoek het aantal climbers in de datbase

        :return result: int, aantal climbers
        """
        result = self.cur.execute("SELECT COUNT(*) FROM `climbers`").fetchone()
        return int(result[0])

    # What is the highest mountain? -> Mountain
    def highest_mountain(self) -> Mountain:
        """
        Zoek de hoogste berg in de database en geef die terug

        :return highest_mountain: Mountain, de hoogste berg
        """
        sq_select_mountain = """
            SELECT * FROM `mountains`
              GROUP BY `name`
              ORDER BY `height` DESC
              LIMIT 1
        """
        output = self.cur.execute(sq_select_mountain).fetchone()
        result = output.fetchone()
        dict_row = {output.description[i][0]: result[i] for i in range(len(result))}

        highest_mountain = Mountain(dict_row['id'],
                                    dict_row['name'],
                                    dict_row['country'],
                                    dict_row['rank'],
                                    dict_row['height'],
                                    dict_row['prominence'],
                                    dict_row['range'])

        return highest_mountain

    # What is the longest and shortest expedition? -> tuple[Expedition, Expedition]
    def longest_and_shortest_expedition(self) -> tuple[Expedition, Expedition]:
        """
        Zoek de langste en kortste expedition in de databse

        :return expeditions: tuple, tuple met de langste en kortste expeditions
        """
        sq_select_expeditions = """
            SELECT * FROM `expeditions`
              WHERE `duration` = (SELECT MAX(`duration`) FROM `expeditions`)
                 OR `duration` = (SELECT MIN(`duration`) FROM `expeditions`)
        """
        output = self.cur.execute(sq_select_expeditions)
        result = output.fetchall()

        expeditions = []

        for row in result:
            dict_row = {output.description[i][0]: result[i] for i in range(len(row))}
            expedition = Expedition(dict_row['id'],
                                    dict_row['name'],
                                    dict_row['mountain_id'],
                                    dict_row['start_location'],
                                    dict_row['date'],
                                    dict_row['country'],
                                    dict_row['duration'],
                                    dict_row['success'])
            expeditions.append(expedition)

        return tuple(expeditions)

    # Which expeditons have the most climbers -> tuple[Expedition, ...]
    def expedition_with_most_climbers(self) -> tuple[Expedition, ...]:
        """
        Zoek de expedition met de meeste climbers uit de database

        :return expeditions: tuple, lijst met de expeditions die de meeste climbers hebben
        """
        sq_select_expeditions = """
            SELECT * FROM `expeditions`
              WHERE `id` =
                (SELECT `expedition_id`
                   FROM `expedition_climbers`
                   GROUP BY `expedition_id`
                   ORDER BY COUNT(*) DESC
                )
        """
        output = self.cur.execute(sq_select_expeditions)
        result = output.fetchall()

        expeditions = []

        for row in result:
            dict_row = {output.description[i][0]: result[i] for i in range(len(row))}
            expedition = Expedition(dict_row['id'],
                                    dict_row['name'],
                                    dict_row['mountain_id'],
                                    dict_row['start_location'],
                                    dict_row['date'],
                                    dict_row['country'],
                                    dict_row['duration'],
                                    dict_row['success'])
            expeditions.append(expedition)

        return tuple(expeditions)

    # Which climbers have made the most expeditions -> tuple[Climber, ...]
    # Which climbers have made the most succesful expeditions -> tuple[Climber, ...]
    def climbers_with_most_expeditions(self, only_succesful: bool = False) -> tuple[Climber, ...]:
        climbers = []

        sq_select_climbers = """
            WITH `max_subquery` AS (
              SELECT COUNT(`expedition_id`) as `c`
              FROM `expedition_climbers`
              GROUP BY `climber_id`
              ORDER BY `c` DESC
            )
            SELECT `climbers`.*
              FROM `climbers`
                LEFT JOIN `expedition_climbers`
                ON `expedition_climbers`.`climber_id` = `climbers`.`id`
                LEFT JOIN `expeditions`
                ON `expedition_climbers`.`expedition_id` = `expeditions`.`id`
        """

        if only_succesful is True:
            sq_select_climbers += """
              WHERE `expeditions`.`success` = 1
        """

        sq_select_climbers += """
              GROUP BY `expedition_climbers`.`climber_id`
              ORDER BY COUNT(`expedition_climbers`.`expedition_id`) DESC
              LIMIT (SELECT MAX(`c`) FROM `max_subquery`);
        """

        output = self.cur.execute(sq_select_climbers)
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

        return tuple(climbers)

    # Which mountain has the most expeditions -> Mountain
    def mountains_with_most_expeditions(self) -> tuple[Mountain, ...]:
        mountains = []

        sq_select_mountain = """
            WITH `max_subquery` AS (
              SELECT COUNT(`mountain_id`) as `c`
              FROM `expeditions`
              GROUP BY `mountain_id`
              ORDER BY `c` DESC
            )
            SELECT * FROM `mountains`
              WHERE `id` = (
                SELECT `mountain_id`
                FROM `expeditions`
                GROUP BY `mountain_id`
                LIMIT (SELECT MAX(`c`) FROM `max_subquery`)
              );
        """
        output = self.cur.execute(sq_select_mountain)
        result = output.fetchall()
        for row in result:
            # Maak een dictionary van de row om het makkelijker en duidelijk te kunnen gebruiken
            dict_row = {output.description[i][0]: row[i] for i in range(len(row))}
            mountain = Mountain(dict_row['id'],
                                dict_row['name'],
                                dict_row['country'],
                                dict_row['rank'],
                                dict_row['height'],
                                dict_row['prominence'],
                                dict_row['range'])
            mountains.append(mountain)

        return tuple(mountains)

    # Which expedition was the first expedition? -> Expedition
    # Which expedition was the first successful expedition? -> Expedition
    def get_first_expedition(self, only_succesful: bool = False) -> Expedition:
        sq_select_expedition = """
            SELECT * FROM `expeditions`
        """
        if only_succesful is True:
            sq_select_expedition += """
              WHERE `success` = 1
        """

        sq_select_expedition += """
            ORDER BY `date` ASC
            LIMIT 1;
        """
        output = self.cur.execute(sq_select_expedition).fetchone()
        result = output.fetchone()
        dict_row = {output.description[i][0]: result[i] for i in range(len(result))}

        first_expedition = Expedition(dict_row['id'],
                                      dict_row['name'],
                                      dict_row['mountain_id'],
                                      dict_row['start_location'],
                                      dict_row['date'],
                                      dict_row['country'],
                                      dict_row['duration'],
                                      dict_row['success'])
        return first_expedition

    # Which expedition is the latest? -> Expedition
    # Which succesful expedition is the latetst? -> Expedition
    def get_latest_expedition(self, only_succesful: bool = False) -> Expedition:
        sq_select_expedition = """
            SELECT * FROM `expeditions`
        """
        if only_succesful is True:
            sq_select_expedition += """
              WHERE `success` = 1
        """

        sq_select_expedition += """
            ORDER BY `date` DESC
            LIMIT 1;
        """
        output = self.cur.execute(sq_select_expedition).fetchone()
        result = output.fetchone()
        dict_row = {output.description[i][0]: result[i] for i in range(len(result))}

        latest_expedition = Expedition(dict_row['id'],
                                       dict_row['name'],
                                       dict_row['mountain_id'],
                                       dict_row['start_location'],
                                       dict_row['date'],
                                       dict_row['country'],
                                       dict_row['duration'],
                                       dict_row['success'])
        return latest_expedition

    # Which climbers have climbed mountain Z between period X and Y? -> tuple[Climber, ...]
    # Based on given parameter `to_csv = True` should generate CSV file as  `Climbers Mountain Z between X and Y.csv`
    # otherwise it should just return the value as tuple(Climber, ...)
    # CSV example:
    #   Id, first_name, last_name, nationality, date_of_birth
    def get_climbers_that_climbed_mountain_between(self, mountain: Mountain, start: datetime, end: datetime, to_csv: bool = False) -> tuple[Climber, ...]:
        climbers = []

        sq_select_climbers = """
            SELECT `climbers`.*
              FROM `climbers`
                LEFT JOIN `expedition_climbers`
                ON `expedition_climbers`.`climber_id` = `climbers`.`id`
                LEFT JOIN `expeditions`
                ON `expedition_climbers`.`expedition_id` = `expeditions`.`id`
              WHERE `expeditions`.`mountain_id` = :mid
                AND (`expeditions`.`date` BETWEEN :start AND :end)
        """
        output = self.cur.execute(sq_select_climbers, {'mid': mountain.id, 'start': start, 'end': end})
        result = output.fetchall()
        for row in result:
            # Maak een dictionary van de row om het makkelijker en duidelijk te kunnen gebruiken
            dict_row = {output.description[i][0]: row[i] for i in range(len(row))}
            if to_csv is True:
                climbers.append(dict_row)
            else:
                climber = Climber(dict_row['id'],
                                  dict_row['first_name'],
                                  dict_row['last_name'],
                                  dict_row['nationality'],
                                  dict_row['date_of_birth'])
                climbers.append(climber)

        if to_csv is True:
            tv.list_to_csv(f"climbers_between_on_{mountain.name}.csv", climbers)
        else:
            return tuple(climbers)

    # Which mountains are located in country X? ->tuple[Mountain, ...]
    # Based on given parameter `to_csv = True` should generate CSV file as  `Mountains in country X.csv`
    # otherwise it should just return the value as tuple(Mountain, ...)
    # CSV example:
    #   Id, name, country, rank, height, prominence, range
    def get_mountains_in_country(self, country: str, to_csv: bool = False) -> tuple[Mountain, ...]:
        pass

    # Which climbers are from country X? -> tuple[Climber, ...]
    # Based on given parameter `to_csv = True` should generate CSV file as  `Climbers in country X.csv`
    # otherwise it should just return the value as tuple(Climber, ...)
    # CSV example:
    #   Id, first_name, last_name, nationality, date_of_birth
    def get_climbers_from_country(self, country: str, to_csv: bool = False) -> tuple[Climber, ...]:
        pass


if __name__ == "__main__":
    reporter = Reporter()
    Putha = Mountain(73, "Putha Hiunchuli", "Nepal", 94, 7246, 1151, "Dhaulagiri Himalaya")
    print(reporter.get_climbers_that_climbed_mountain_between(Putha,
                                                              datetime(1966, 1, 1),
                                                              datetime(1968, 1, 1), 
                                                              True))