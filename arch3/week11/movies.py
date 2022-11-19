import json


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
    parts = filter_str.split(" ")
    capitalized_parts = [p.capitalize() for p in parts]
    filter_str = " ".join(capitalized_parts)

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
    """
    return list(filter(lambda x: begin <= x['year'] <= end, movies))


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


def main():
    """
    Functie waar het programma in gedraaid wordt.
    """
    movies = json_to_movies("movies.json")
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


if __name__ == "__main__":
    main()
