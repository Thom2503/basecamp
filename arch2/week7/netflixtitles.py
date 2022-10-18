import os
import sys
import csv


def load_csv_file(file_name: str) -> list:
    """
    Functie om de csv als een list in te laden dit wordt dan geanalyseerd

    @param string file_name - csv file naam

    @return list file_content - de content van de csv
    """
    file_content = []

    with open(os.path.join(sys.path[0], file_name), newline='', encoding="utf8") as csv_file:
        file_content = list(csv.reader(csv_file, delimiter=","))

    return file_content


def get_headers(file_content: list) -> list:
    """
    Functie om de headers van het bestand te krijgen

    @param list file_content - de data van de csv

    @return string - de headers
    """
    return file_content[0]


def search_by_type(file_content: list, show_type: str) -> list:
    """
    Functie om alle titels met het type film of tv show te krijgen
    hier wordt dan op gefilterd

    @param list file_content - de titels
    @param string show_type  - type waar gefilterd op wordt

    @return list - gefilterde list met de films/tv shows
    """
    # maak er lowercase van is makkelijker zoeken
    show_type = show_type.lower()
    # [1] is de type kolom
    return list(filter(lambda x: x[1].lower() != show_type, file_content))


def search_by_director(file_content: list, director: str) -> list:
    """
    Functie om alle titels met van een director te krijgen
    hier wordt dan op gefilterd

    @param list file_content - de titels
    @param string director   - director waar gefilterd op wordt

    @return list - gefilterde list titels van de director
    """
    # maak er lowercase van is makkelijker zoeken
    director = director.lower()
    # [3] is de director kolom
    return list(filter(lambda x: x[3].lower() == director, file_content))


def get_directors(file_content: list) -> set:
    """
    Functie om de namen van alle directors te krijgen

    @param list file_content - de titels

    @return set directors - de namen van alle directors
    """
    # maak een set van alle directors sets zijn uniek
    # dus er zitten geen duplicates in
    directors = {content[3] for content in file_content}
    return directors


def show_show_movie_directors(file_content: list, get_amount: bool = True) -> list:
    """
    Functie om een lijst te maken met tuples deze tuple
    bevat de naam van director, het aantal films en het aantal tv shows
    of als get_amount false is moet je een lijst met alle namen van
    directors die beide een film en tv show hebben gerigiseerd terug geven

    @param list file_content - de titels
    @param bool get_amount   - of je de aantallen moet krijgen

    @return list names - de lijst met tuples
    """
    names = []
    # krijg alle directors om op te zoeken
    directors = get_directors(file_content)
    # loop door de directors heen om specifieke titels te vinden
    for director in directors:
        # als de director leeg is skip het want er kan dan niks
        # gevonden worden
        if director == "" or director == "director":
            continue
        # alle titels van de director om types op te zoeken
        titles_by_director = search_by_director(file_content, director)
        # zoek alle types om die te tellen
        movies_by_director = search_by_type(titles_by_director, "movie")
        shows_by_director = search_by_type(titles_by_director, "tv show")
        # tel het aantal types
        amount_of_movies = len(movies_by_director)
        amount_of_shows = len(shows_by_director)
        if get_amount is False:
            if amount_of_movies > 0 and amount_of_shows > 0:
                names.append(director)
        else:
            # voeg de tuple toe met de director, aantal films en aantal tv shows
            names.append((director, amount_of_shows, amount_of_movies))
    # geef de lijst terug en sorteer die op alfabetische form
    return sorted(names, key=lambda x: x[0])


def main() -> None:
    titles = load_csv_file('netflix_titles.csv')
    print("""[1] Print the amount of TV Shows
[2] Print the amount of Movies
[3] Print the (full) names of directors in alphabetical order who lead both tv shows and movies.
    (for example, search the name David Ayer. He is the director of three movies and one tv show)
[4] Print the name of each director in alphabetical order,
    the number of movies and the number of tv shows (s)he was the director of.
    Use a tuple with format: (director name, number of movies, number of tv shows) to print.""")
    command = int(input())
    if command == 1:
        # - 1 om de header te vergeten
        print(len(search_by_type(titles, "movie")) - 1)
    elif command == 2:
        print(len(search_by_type(titles, "tv show")) - 1)
    elif command == 3:
        print(show_show_movie_directors(titles, False))
    elif command == 4:
        print(show_show_movie_directors(titles))


if __name__ == "__main__":
    main()
