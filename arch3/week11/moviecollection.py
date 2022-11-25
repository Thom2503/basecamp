import json


JSON_FILE = "movies.json"
MOVIES = []


def json_to_movies(file_path: str) -> list:
    """
    Lees de json en maak daar een list met dictionaries van films van

    :param file_path: str, pad naar het json bestand

    :return movies: list, lijst met dictionaries van films
    or
    :return str, foutmelding als json niet is meegegeven
    """
    movies = []

    with open(file_path, "r") as json_file:
        try:
            movies = json.load(json_file)
        except (TypeError, ValueError):
            return "No valid json"

    return movies


def movies_to_json(file_path: str, movies: list):
    """
    Maak van de lijst met films weer een json bestand

    :param file_path: str, pad naar het bestand
    :param movies: list, lijst met de films
    """
    json_movies = json.dumps(movies, indent=4)

    with open(file_path, "w") as file:
        file.write(json_movies)


def capitalize_str(string: str) -> str:
    """
    Functie om alle woorden in een string te capitalizen.

    :param string: str, string waar alle delen hoofdletters krijgen

    :return capitalized_str: str, spreekt voor zich
    """
    parts = string.split(" ")
    capitalized_parts = [p.capitalize() for p in parts]
    capitalized_str = " ".join(capitalized_parts)

    return capitalized_str


def filter_movies(movies: list, filter_type: str, filter_str: str) -> list:
    """
    Zoek in de lijst naar films met de gegeven filter
    en stop dit dan in een lijst met de gefilterde films

    :param movies: list, de lijst met films
    :param filter_type: str, het type waar je op filtert
    :param filter_str: str, hetgene van de type waar je op filtered.

    :return filtered_movies: list, lijst met gefilterde films
    """
    filtered_movies = []

    # zorg dat de string hoofdletters heeft bij elk woord
    filter_str = capitalize_str(filter_str)

    for movie in movies:
        if filter_type not in ('cast', 'genres'):
            if str(movie[filter_type]) == filter_str:
                filtered_movies.append(movie)
        else:
            if filter_str in movie[filter_type]:
                filtered_movies.append(movie)

    return filtered_movies


def filter_between_years(movies: list, begin: int, end: int) -> list:
    """
    Filter de films tussen de jaren

    :param movies: list, lijst met films
    :param begin: int, begin jaar
    :param end: int, eind jaar

    :return list, lijst met films tussen de jaren
    """
    return list(filter(lambda movie: begin <= movie['year'] <= end, movies))


def print_movie(movie: dict) -> str:
    """
    Maak een mooie string met alle data van een film er in

    :param movie: dict, data van een film

    :param pretty_text: str, mooie string
    """
    pretty_text = ""

    pretty_cast = ""
    if len(movie['cast']) > 0:
        pretty_cast = "With: \n- "
        pretty_cast += "\n- ".join(movie['cast'])

    pretty_genres = ""
    if len(movie['genres']) > 0:
        pretty_genres = "\n- "
        pretty_genres += "\n- ".join(movie['genres'])

    pretty_text = f"""
{movie['title']} from {movie['year']}
{pretty_genres}
--------------
{pretty_cast}"""

    print(pretty_text)


def get_movie_index(movies: list, filtered_movies: list) -> list:
    """
    Krijg een lijstje met de indexes van de gefilterde films
    voor updaten en verwijderen.

    :param movies: list, originele lijst met films
    :param filtered_movies: list, gefilterde lijst met films

    :return indexes: list, indexes van de gefilterde films
    """
    indexes = []

    for movie in filtered_movies:
        indexes.append(movies.index(movie))

    return indexes


def change_movie_value(movies: list, indexes: list, change_type: str, from_str: str, to_str: str):
    """
    Verander een waarde of alle waardes in de movies lijst, op basis
    van het type (change_type) en de meegegeven string (change_str)

    :param movies: list, lijst met de films
    :param indexes: list, lijst met de indexes waar de films gevonden is
    :param change_type: str, het type dat veranderd moet worden
    :param from_str: str, welke waarde je wilt veranderen
    :param to_str: str, naar welke waarde je het wilt veranderen
    """
    global MOVIES
    updated_movies = []

    if change_type != "year":
        # zorg dat de string hoofdletters heeft bij elk woord
        from_str = capitalize_str(from_str)
        to_str = capitalize_str(to_str)

    for idx in range(len(movies)):
        movie = movies[idx]
        if idx in indexes:
            if change_type not in ('cast', 'genres'):
                if str(movie[change_type]) == str(from_str):
                    movie[change_type] = int(to_str) if change_type == "year" else to_str
            else:
                if from_str in movie[change_type]:
                    idx = movie[change_type].index(from_str)
                    movie[change_type][idx] = to_str

        updated_movies.append(movie)

    movies_to_json(JSON_FILE, updated_movies)
    MOVIES = json_to_movies(JSON_FILE)


def remove_from_movie(movies: list, indexes: list, delete_type: str, delete_str: str):
    """
    Verwijder een waarde uit de lijst met films.

    :param movies: list, lijst met films
    :param indexes: list, indexes met de plekken waar de films zijn
    :param delete_type: str, het type waar je de waarde van wilt verwijderen
    :param delete_str: str, de waarde die je wilt verwijderen
    """
    global MOVIES
    updated_movies = []
    # zorg dat de string hoofdletters heeft bij elk woord
    delete_str = capitalize_str(delete_str)

    for idx in range(len(movies)):
        movie = movies[idx]
        if idx in indexes:
            if delete_type in ('cast', 'genres') and delete_str in movie[delete_type]:
                idx = movie[delete_type].index(delete_str)
                movie[delete_type].pop(idx)

        updated_movies.append(movie)

    movies_to_json(JSON_FILE, updated_movies)
    MOVIES = json_to_movies(JSON_FILE)


def menu_item_i(movies: list):
    print(len(filter_movies(movies, "year", "2004")))
    print(len(filter_movies(movies, "genres", "science fiction")))
    # print(filter_movies(movies, "cast", "keanu reeves"))
    keanu_movies = filter_movies(movies, "cast", "keanu reeves")
    for movie in keanu_movies:
        print_movie(movie)

    silvester_movies = filter_movies(movies, "cast", "Sylvester Stallone")
    silvester_movies = filter_between_years(silvester_movies, 1995, 2005)

    for movie in silvester_movies:
        print_movie(movie)


def menu_item_m(movies: list):
    first_movie = movies[0]
    change_movie_value(movies, [0], "year", first_movie['year'], 1899)

    gladiator_movie = filter_movies(movies, "title", "gladiator")
    the_gladiator = filter_between_years(gladiator_movie, 1992, 1992)
    indexes = get_movie_index(movies, the_gladiator)
    change_movie_value(movies, indexes, "year", 1992, 2001)

    nat_movies = filter_movies(movies, "cast", "Natalie Portman")
    indexes = get_movie_index(movies, nat_movies)
    change_movie_value(movies, indexes, "cast", "Natalie Portman", "Nat Portman")

    kevin_movies = filter_movies(movies, "cast", "kevin spacey")
    indexes = get_movie_index(movies, kevin_movies)
    remove_from_movie(movies, indexes, "cast", "kevin spacey")


def main():
    """
    Functie waar het programma in gedraaid wordt.
    """
    MOVIES = json_to_movies(JSON_FILE)

    print("[I] Movie information overview")
    print("[M] Make modification based on assignment")
    print("[S] Search a movie title ")
    print("[C] Change title and/or release year by search on title")
    print("[Q] Quit program")

    quit_program = False

    while quit_program is False:
        command = input("> ").lower()
        if command in ('q', 'quit'):
            quit_program = True
        elif command in ('i', 'info'):
            menu_item_i(MOVIES)
        elif command in ('m', 'modify'):
            menu_item_m(MOVIES)
        elif command in ('s', 'search'):
            search_arg = input("s> ").lower()
            searched_movies = filter_movies(MOVIES, "title", search_arg)
            for movie in searched_movies:
                print_movie(movie)
        elif command in ('c', 'change'):
            search_arg = input("c> ").lower()
            found_movie = filter_movies(MOVIES, "title", search_arg)
            indexes = get_movie_index(MOVIES, found_movie)
            change_title = input("New Title> ").lower()
            change_year = input("New year> ").lower()
            # verander de film
            if len(indexes) == 1:
                found_title, found_year = found_movie[0]['title'], found_movie[0]['year']
                change_movie_value(MOVIES, indexes, "title", found_title, change_title)
                change_movie_value(MOVIES, indexes, "year", found_year, change_year)


if __name__ == "__main__":
    main()
