from climbersapp import is_empty_db, add_expeditions, add_mountains
import tvlib as tv

import sqlite3

"""
Dit is mijn uitbreiding op de masterproof wat een simpele crud app is
waar je expeditions, climbers en mountains kan toevoegen, verwijderen en bekijken.
"""


def is_correct_date(date: str) -> bool:
    """
    Functie om te checken of de gegeven string
    correcte datum is op basis van %Y-%m-%d

    :param date: str, string om te checken
    """
    # bool om te checken of de datum een correcte datum is
    is_correct_date = False
    try:
        is_correct_date = bool(tv.str_to_time(date, "%Y-%m-%d"))
    except ValueError:
        is_correct_date = False

    return is_correct_date


def add_climber(cur: object, climber_data: list) -> None:
    """
    Functie om een climber toe te voegen aan de database

    :param cur: object, cursor object van de database
    :param climber_data: list, data wat in de database moet komen
    """
    sq_climber_data = {}
    sq_climber_data['first_name'] = climber_data[0].capitalize()
    sq_climber_data['last_name'] = climber_data[1].capitalize()
    sq_climber_data['nationality'] = climber_data[2]

    # check of de datum correct is als Y-m-d
    if is_correct_date(climber_data[3]) is False:
        print("Climber: incorrect date given, needs to be year-month-day!")
        return

    sq_climber_data['date_of_birth'] = climber_data[3]

    sq_add_climber = """
        INSERT INTO `climbers`
        (`first_name`, `last_name`, `nationality`, `date_of_birth`)
        VALUES (:first_name, :last_name, :nationality, :date_of_birth)
    """

    cur.execute(sq_add_climber, sq_climber_data)


def add_mountain(cur: object, mountain_data: list) -> None:
    """
    Functie om een mountain toe te voegen aan de database

    :param cur: object, cursor object van de database
    :param mountain_data: list, data wat in de database moet komen
    """
    sq_mountain_data = {}
    sq_mountain_data['name'] = mountain_data[0].capitalize()
    sq_mountain_data['country'] = mountain_data[1].capitalize()

    if mountain_data[2].isnumeric() is False:
        print("Mountain: rank needs to be numeric!")
        return

    sq_mountain_data['rank'] = int(mountain_data[2])

    if mountain_data[3].isnumeric() is False:
        print("Mountain: height needs to be numeric!")
        return

    sq_mountain_data['height'] = int(mountain_data[3])

    if mountain_data[4].isnumeric is False:
        print("Mountain: prominence needs to be numeric!")
        return

    sq_mountain_data['prominence'] = int(mountain_data[4])
    sq_mountain_data['range'] = mountain_data[5].capitalize()

    sq_add_mountain = """
        INSERT INTO `mountains`
        (`name`, `country`, `rank`, `height`, `prominence`, `range`)
        VALUES (:name, :country, :rank, :height, :prominence, :range)
    """

    cur.execute(sq_add_mountain, sq_mountain_data)


def add_expedition(cur: object, expedition_data: list) -> None:
    """
    Functie om een expedition toe te voegen aan de database

    :param cur: object, cursor object van de database
    :param expedition_data: list, data wat in de database moet komen
    """
    sq_expedition_data = {}
    sq_expedition_data['name'] = expedition_data[0].capitalize()

    # zoeken naar de berg want er mag geen id ingevuld worden
    # van een berg die niet bestaat.
    sq_select_mountain = """
        SELECT * FROM `mountains` WHERE `id` = :mid
    """
    mountain = cur.execute(sq_select_mountain, {'mid': expedition_data[1]}).fetchone()
    if mountain is None:
        print("Expedition: mountain is not found with this id!")
        return

    sq_expedition_data['mid'] = expedition_data[1]
    sq_expedition_data['start'] = expedition_data[2]

    if is_correct_date(expedition_data[3]) is False:
        print("Expedition: incorrect date given!")
        return

    sq_expedition_data['date'] = expedition_data[3]
    sq_expedition_data['country'] = expedition_data[4].capitalize()

    if expedition_data[5].isnumeric() is False:
        print("Expedition: duration is not numeric needs to be minutes")
        return

    sq_expedition_data['duration'] = expedition_data[5]

    if expedition_data[6].lower() not in ('1', '0', 'true', 'false'):
        print("Expedition: success needs to be a boolean (1, 0, True, False)")
        return

    sq_expedition_data['success'] = expedition_data[6]

    sq_add_expedition = """
        INSERT INTO `expeditions`
        (`name`, `mountain_id`, `start_location`, `date`, `country`, `duration`, `success`)
        VALUES (:name, :mid, :start, :date, :country, :duration, :success)
    """

    cur.execute(sq_add_expedition, sq_expedition_data)


def print_data(cur: object, search_table: str, search_term: str) -> str:
    """
    Functie om in de database te zoeken naar een meegegeven term
    in een meegegeven database.

    :param cur: object, database cursor
    :param search_table: str, table om in te zoeken
    :param search_term: str, term om op te zoeken
    """
    # een niet heel veilige manier om de db table te kiezen
    # maar dit wilde ik zo veel mogelijk dynamisch maken.
    sq_get_data = f"""
        SELECT *
        FROM `{search_table}`
    """
    # alle opties voor het opzoeken van de data in de database
    # bij elke statement staat er data wat gezocht moet worden
    # met een where clause
    if search_table == "climbers":
        sq_get_data += """
        WHERE `id` = :id
           OR `first_name` = :first
           OR `last_name` = :last
           OR `nationality` = :nationality
           OR `date_of_birth` = :date_of_birth
        """
        sq_term_data = {
            'id': search_term,
            'first': search_term.capitalize(),
            'last': search_term.capitalize(),
            'nationality': search_term.capitalize(),
            'date_of_birth': search_term
        }
    elif search_table == "mountains":
        sq_get_data += """
        WHERE `id` = :id
           OR `name` = :name
           OR `country` = :country
           OR `rank` = :rank
           OR `range` = :range
        """
        sq_term_data = {
            'id': search_term,
            'name': search_term.capitalize(),
            'country': search_term.capitalize(),
            'rank': search_term,
            'range': search_term.capitalize()
        }
    elif search_table == "expeditions":
        sq_get_data += """
        WHERE `id` = :id
           OR `name` = :name
           OR `start_location` = :start
           OR `country` = :country
           OR `date` = :date
        """
        sq_term_data = {
            'id': search_term,
            'name': search_term.capitalize(),
            'start': search_term.capitalize(),
            'country': search_term.capitalize(),
            'date': search_term
        }
    else:
        print("Wrong table given!")
        return

    result = cur.execute(sq_get_data, sq_term_data).fetchall()
    for row in result:
        print(" - ".join([str(x) for x in row]))


def delete_data(cur: object, delete_table: str, id_to_delete: int) -> None:
    """
    Verwijder iets uit de database op basis van de delete_table en id_to_delete

    :param cur: object, cursor voor de database
    :param delete_table: str, table om uit te deleten
    :param id_to_delete: int, id voor de where clause
    """
    # weer een beetje onveilige query om dynamisch
    # de table te kiezen
    sq_delete_data = f"""
        DELETE FROM `{delete_table}`
        WHERE `id` = :id
    """
    if isinstance(id_to_delete, int) is False:
        print("Delete: id is not an integer")
        return

    cur.execute(sq_delete_data, {'id': id_to_delete})


def main():
    con = sqlite3.connect("climbersapp.db")
    cur = con.cursor()

    is_empty = is_empty_db(cur)
    if is_empty is True:
        # zorg eerst dat de bergen zijn toegevoegd omdat expeditions die
        # gebruikt
        add_mountains(cur)

        # voeg expeditions toe aan de database tegelijkertijd ook met
        # de climbers van die expedition om de connectie te maken
        add_expeditions(con)

    quit_program = False

    print("""WELCOME TO THE EXPEDITIONS TRACKER
    -----------------------
[C] add a climber
[M] add a mountain
[E] add a expedition
    -----------------------
[P] print data
    -----------------------
[D] delete data
    """)

    while quit_program is False:
        command = input("> ").lower()
        if command in ('q', 'quit'):
            quit_program = True
        elif command in ('c', 'climber'):
            print("Add climber data seperated by comma's:")
            print("Data to add: first name, last name, nationality, date of birth (Year-month-day)")
            climber_data = input("add climber > ")
            climber_data_parts = climber_data.split(",")

            if len(climber_data_parts) != 4:
                print("Incorrect number of data!")

            add_climber(cur, climber_data_parts)
            con.commit()
        elif command in ('m', 'mountain'):
            print("Add mountain data seperated by comma's:")
            print("Data to add: name, country, rank, height, prominence, range")
            mountain_data = input("add mountain > ")
            mountain_data_parts = mountain_data.split(",")

            if len(mountain_data_parts) != 6:
                print("Incorrect number of data!")

            add_mountain(cur, mountain_data_parts)
            con.commit()
        elif command in ('e', 'expedition'):
            print("Add expedition data seperated by comma's:")
            print("Data to add: name, mountain_id, start location, date, country, duration (minutes), success")
            expedition_data = input("add expedition > ")
            expedition_data_parts = expedition_data.split(",")

            if len(expedition_data_parts) != 7:
                print("Incorrect number of data!")

            add_expedition(cur, expedition_data_parts)
            con.commit()
        elif command in ('p', 'print'):
            option_info = {
                'climbers': 'Give an id, first name, last name, nationality or date of birth to search for',
                'mountains': 'Give an id, name, country, rank or range to search for',
                'expeditions': 'Give an id, name, start, country or date to search for'
            }

            print("Choose what to print: climbers, mountains, expeditions")
            table_option = input("print data > ").lower()

            if table_option not in ('climbers', 'mountains', 'expeditions'):
                print("Incorrect option given!")

            print(option_info[table_option])
            search_option = input("search term > ")

            print_data(cur, table_option, search_option)
        elif command in ('d', 'delete'):
            print("Choose what to delete: climbers, mountains, expeditions")
            table_option = input("delete data > ").lower()

            if table_option not in ('climbers', 'mountains', 'expeditions'):
                print("Incorrect option given!")

            print("Give an id to delete")
            id_to_delete = int(input("id to delete > "))

            delete_data(cur, table_option, id_to_delete)
            con.commit()
        else:
            print("Wrong command!")

    con.close()


if __name__ == "__main__":
    main()
