import csv

CSV_FILE = "bannedvideogames.csv"
GAMES = []


def csv_to_games(file_path: str) -> list:
    """
    Stop de content van een csv file in een lijstje

    :param file_path: str, pad naar het csv bestand

    :return file_content: list, lijst met alle games
    """
    file_content = []
    with open(file_path, "r") as file:
        file_content = list(csv.DictReader(file))

    return file_content


def games_to_csv(file_path: str, content: list):
    """
    Stop de content van een python lijstje in de csv file

    :param file_path: str, pad naar csv bestand
    :param content: list, de content van in een python list
    """
    # headers die csv nodig heeft
    headers = content[0].keys()
    with open(file_path, "w") as out_file:
        writer = csv.DictWriter(out_file, headers)
        writer.writeheader()
        writer.writerows(content)


def filter_by_type(games: list, filter_type: str, filter_str: str) -> list:
    """
    Filter de games op basis van de country.

    :param games: list, de lijst met games
    :param filter_type: str, waar je op wilt filteren
    :param filter_str: waar je op wilt filteren

    :return list, gefilterde lijst
    """
    return list(filter(lambda game: game[filter_type] == filter_str, games))


def add_game(games: list, new_content: dict) -> None:
    """
    Functie om een game toe te voegen op basis van een list.

    :param games: list, lijst met de games om aan toe te voegen
    :param new_content: dict, nieuwe content die toegevoegd kan worden
    """
    global GAMES

    # gebruik de header keys en de values van het nieuwe content
    # om het een goede dictionary te maken voor in de csv
    header_keys = list(games[0].keys())
    new_values = list(new_content.values())

    new_content = {k: v for k, v in zip(header_keys, new_values)}

    games.append(new_content)

    games_to_csv(CSV_FILE, games)
    GAMES = csv_to_games(CSV_FILE)


def get_game_index(games: list, filtered_games: list) -> list:
    """
    Maak een lijst met alle indexes van de gefilterde lijst in de
    originele lijst

    :param games: list, lijst met de games
    :param filtered_games: list, lijst met de gefilterde games om de indexes van te zoeken

    :return list, lijst met de indexes van de gefilterde games
    """
    return [games.index(game) for game in filtered_games]


def get_countries(games: list) -> set:
    """
    Functie om alle landen uit het bestand te krijgen.

    :param games: list, lijst met de games

    :return countries: set, alle landen
    """
    countries = []
    for game in games:
        for key, value in game.items():
            if key == "Country":
                countries.append(value)

    countries = set(countries)
    return countries


def update_records(games: list, change_type: str, from_str: str, to_str: str) -> list:
    """
    Functie om een specifieke waarde te veranderen van een record om die vervolgens te kunnen updaten

    :param games: list, lijst met de games
    :param change_type: str, welk type je wilt veranderen
    :param from_str: str, wat de oude waarde is
    :param to_str: str, wat de nieuwe waarde moet zijn.

    :return updated_records: list, lijst met de nieuwe records
    """
    updated_records = []
    found_records = filter_by_type(games, change_type, from_str)

    for record in found_records:
        if record[change_type] == from_str:
            record[change_type] = to_str
        updated_records.append(record)

    return updated_records


def update_games(games: list, new_content: list) -> None:
    """
    Update the info van een game door de content te veranderen op die index.

    :param gemes: list, lijst met de games
    :param new_content: list, de nieuwe content voor op die plek
    """
    global GAMES
    updated_games = []

    found_indexes = get_game_index(games, new_content)

    i = 0
    for idx in range(len(games)):
        if idx in found_indexes:
            games[idx] = new_content[i]
            i += 1
        updated_games.append(games[idx])

    games_to_csv(CSV_FILE, updated_games)
    GAMES = csv_to_games(CSV_FILE)


def remove_records(games: list, filter_type: str, filter_str: str) -> None:
    """
    Verwijder de records uit games met die overeenkomen met filter type/str.

    :param games: list, lijst met de games
    :param filter_type: str, op welk type je wilt filteren (om te verwijderen
    :param filter_str: str, op welke waarde je wilt filteren
    """
    global GAMES

    found_records = filter_by_type(games, filter_type, filter_str)
    found_indexes = get_game_index(games, found_records)

    updated_games = [game for idx, game in enumerate(games) if idx not in found_indexes]

    games_to_csv(CSV_FILE, updated_games)
    GAMES = csv_to_games(CSV_FILE)


def add_game_prompt(games: list) -> None:
    """
    Functie om de vragen te stellen over de nieuwe game.

    :param games: list, lijst met de games
    """
    answers = {
        'id': '',
        'name': '',
        'series': '',
        'country': '',
        'details': '',
        'category': '',
        'status': '',
        'wikipedia': '',
        'image': '',
        'summmary': '',
        'developer': '',
        'publisher': '',
        'genre': '',
        'homepage': ''
    }

    for question, value in answers.items():
        user_answer = input(f"{question}> ")
        answers[question] = user_answer

    add_game(games, answers)


def print_overview(country_data: list, country: str, name_details: bool = False) -> None:
    """
    Print een overview met het land, hoeveel gebannede games
    en welke games dat zijn.

    :param country_data: list, lijst met de games per land
    :param country: str, de naam van het land
    :param name_details: bool, of het de detail en naam moet tonen
    """
    if name_details is False:
        amount_banned = len(country_data)

        text = f"{country} - {amount_banned}\n"

        for game in country_data:
            text += f"- {game['Game']}\n"
    else:
        text = ""
        for game in country_data:
            text += f"{game['Game']} - {game['Details']}\n"

    print(text)


def print_each_country(games: list) -> None:
    """
    Haal alle informatie op van elk land in het bestand

    :param games: list, lijst met de games
    """
    countries = get_countries(games)

    for country in countries:
        country_data = filter_by_type(games, "Country", country)
        print_overview(country_data, country)


def menu_item_i(games: list) -> None:
    """
    Print de assignment dingen

    :param games: list, lijst met de games
    """
    print(len(filter_by_type(games, "Country", "Israel")))

    countries = get_countries(games)
    max_amount = 0
    max_country = ""
    for country in countries:
        country_data = filter_by_type(games, "Country", country)
        amount = len(country_data)
        if amount > max_amount:
            max_amount = amount
            max_country = country

    print(max_country)

    ac_games = filter_by_type(games, "Series", "Assassin's Creed")
    print(len(filter_by_type(ac_games, "Ban Status", "Active")))

    germany_data = filter_by_type(games, "Country", "Germany")
    print_overview(germany_data, "Germany", True)

    red_dead_games = filter_by_type(games, "Series", "Red Dead Redemption")
    text = ""
    for game in red_dead_games:
        text += f"{game['Country']} - {game['Details']}\n"
    print(text)


def menu_item_m(games: list) -> None:
    """
    Doe de veranderingen als de assignment wilt

    :param games: list, lijst met de games
    """
    remove_records(games, "Country", "Germany")
    games = GAMES  # update de locale games list met de globale games list

    updated_records = update_records(games, "Game", "Silent Hill VI: Homecoming", "Silent Hill Remastered")
    update_games(games, updated_records)

    brazil_games = filter_by_type(games, "Country", "Brazil")
    bully_games = filter_by_type(brazil_games, "Game", "Bully")
    updated_records = update_records(bully_games, "Ban Status", "Active", "Ban Lifted")
    update_games(games, updated_records)

    manhunt_games = filter_by_type(games, "Series", "Manhunt")
    updated_records = update_records(manhunt_games, "Genre", "Stealth", "Action")
    update_games(games, updated_records)

    manhunt_games = filter_by_type(games, "Series", "Manhunt")
    to_str = "Action|Psychological Horror"
    updated_records = update_records(manhunt_games, "Genre", "Stealth|Psychological horror", to_str)
    update_games(games, updated_records)


def main(filename: str) -> None:
    global GAMES

    print("[I] Print request info from assignment")
    print("[M] Make modification based on assignment")
    print("[A] Add new game to list")
    print("[O] Overview of banned games per country")
    print("[S] Search the dataset by country")
    print("[Q] Quit program")

    quit_program = False

    GAMES = csv_to_games(filename)

    while quit_program is False:
        command = input("> ").lower()
        if command in ('q', 'quit'):
            quit_program = True
        elif command in ('i', 'info'):
            menu_item_i(GAMES)
        elif command in ('m', 'modify'):
            menu_item_m(GAMES)
        elif command in ('a', 'add'):
            add_game_prompt(GAMES)
        elif command in ('o', 'overview'):
            print_each_country(GAMES)
        elif command in ('s', 'search'):
            country_name = input("s> ").capitalize()
            country_data = filter_by_type(GAMES, "Country", country_name)
            print_overview(country_data, country_name, True)


if __name__ == "__main__":
    main(CSV_FILE)
