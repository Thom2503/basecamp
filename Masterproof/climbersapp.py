import sqlite3

import tvlib as tv

# as is erbij om circular definitions te vermijden
from climber import Climber as Climber
from mountain import Mountain as Mountain
from expedition import Expedition as Expedition

FILE_NAME = "expeditions.json"


def is_empty_db(cur: object) -> bool:
    """
    Functie om te checken of de database tabellen leeg zijn.
    Als die leeg zijn moeten die opgevuld worden met de mountains,
    climbers en expeditions.

    :return bool, of het leeg is of niet (true = leeg, false = niet leeg)
    """
    # query om alle namen van de tables te krijgen om te zoeken of ze leeg zijn
    result = cur.execute("SELECT `name` FROM `sqlite_master` WHERE `type` = 'table'").fetchall()
    tables = [x[0] for x in result]

    for table in tables:
        # query om te tellen hoeveel rows er zijn
        result = cur.execute(f"SELECT COUNT(*) FROM `{table}`").fetchone()
        # als de count 0 is is de table leeg
        if result[0] == 0:
            return True
    return False


def add_mountains(cur: object):
    """
    Voeg de bergen uit de json file toe aan de database

    :param file_name: str, de naam van het bestand
    """
    data = tv.json_to_list(FILE_NAME)

    sq_add_mountain = """
        INSERT OR REPLACE INTO `mountains`
        (`name`, `country`, `rank`, `height`, `prominence`, `range`)
        VALUES (:name, :country, :rank, :height, :prominence, :range)
    """
    mountains = []  # lijst met toegevoegde bergen om duplicates te vermijden
    for expedition in data:
        mountain_data = expedition['mountain']

        name = mountain_data['name']
        country = mountain_data['countries'][0]
        rank = mountain_data['rank']
        height = int(mountain_data['height'])
        prominence = int(mountain_data['prominence'])
        range = mountain_data['range']

        # als de naam in de lijst gevonden is is het hoogstwaarschijnlijk
        # een duplicate en kan je het toevoegen overslaan
        if name in mountains:
            continue

        sq_data = {'name': name,
                   'country': country,
                   'rank': rank,
                   'height': height,
                   'prominence': prominence,
                   'range': range}
        cur.execute(sq_add_mountain, sq_data)
        mountains.append(name)


def add_expeditions(con: object):
    """
    Voeg de expeditions en de climbers toe aan de database.
    """
    cur = con.cursor()
    data = tv.json_to_list(FILE_NAME)

    sq_add_climber = """
        INSERT OR REPLACE INTO `climbers`
        (`id`, `first_name`, `last_name`, `nationality`, `date_of_birth`)
        VALUES (:cid, :first, :last, :nationality, :birthday)
    """

    climber_ids = []  # lijst met toegevoegde climbers zodat er geen duplicates in zitten

    sq_add_expedition = """
        INSERT OR REPLACE INTO `expeditions`
        (`id`, `name`, `mountain_id`, `start_location`, `date`, `country`, `duration`, `success`)
        VALUES (:eid, :name, :mid, :start, :date, :country, :duration, :success)
    """
    for expediton in data:
        id = int(expediton['id'])
        name = expediton['name']
        mountain_name = expediton['mountain']['name']

        # query om de berg te zoeken voor de id in het object en database
        sq_select_mountain = "SELECT `id` FROM `mountains` WHERE `name` = :mName LIMIT 1"
        result = cur.execute(sq_select_mountain, {'mName': mountain_name}).fetchone()
        mountain_id = int(result[0])

        date = tv.str_to_time(expediton['date'], "%Y-%m-%d")
        country = expediton['country']
        start = expediton['start']
        minutes_duration = int(expediton['duration'].split("H")[0]) * 60
        duration = int(expediton['duration'].split("H")[1]) + minutes_duration
        success = bool(expediton['success'])

        sq_data = {'eid': id, 'name': name,
                   'mid': mountain_id, 'date': date,
                   'country': country, 'start': start,
                   'duration': duration, 'success': success}

        cur.execute(sq_add_expedition, sq_data)
        con.commit()
        # maak een Expedition opbject aan om de climber te kunnen verbinden in expedition_climbers table
        cur_expedition = Expedition(id, name, mountain_id, start, date, country, duration, success)

        for climber in expediton['climbers']:
            climber_id = climber['id']
            first_name = climber['first_name']
            last_name = climber['last_name']
            nationality = climber['nationality']
            birthday = tv.str_to_time(climber['date_of_birth'], "%d-%m-%Y")

            # maak een climber object aan om die te kunnen verbinden
            cur_climber = Climber(climber_id, first_name, last_name, nationality, birthday)
            cur_expedition.add_climber(cur_climber)  # verbind de climber aan de huidige expedition

            # als de climber al is toegevoegd hoeft dat niet meer aan de database
            # en kan de loop overgeslagen worden
            if climber_id in climber_ids:
                continue

            cur.execute(sq_add_climber, {'cid': climber_id,
                                         'first': first_name,
                                         'last': last_name,
                                         'nationality': nationality,
                                         'birthday': birthday})
            con.commit()
            climber_ids.append(climber_id)


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


if __name__ == "__main__":
    main()
