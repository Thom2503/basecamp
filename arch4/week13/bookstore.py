from datetime import datetime, timedelta
from math import ceil
import os
import sys
import json
import sqlite3


def str_to_time(date_str: str, format: str = "%d-%m-%Y %H:%M:%S") -> datetime:
    """
    Maak een datetime object van een gegeven date_str en format.
    """
    return datetime.strptime(date_str, format)


def time_to_str(time: datetime, format: str = "%d-%m-%Y %H:%M:%S") -> str:
    """
    Verander de datetime naar een leesbare string
    gebaseerd op de meegegeven format
    """
    return time.strftime(format)


def json_to_list(file_path: str) -> list:
    """
    Make a list of dictionaries with the content of a json file

    :param file_path: str, path to the json file

    :return json_items: list, list of dictionaries with the json items
    or
    :return str, error if file given isn't a json file
    """

    assert os.path.exists(file_path) is True, f"Input file ({file_path}) to read from doesn't exists"

    json_items = []

    with open(file_path, "r") as json_file:
        try:
            json_items = json.load(json_file)
        except (TypeError, ValueError):
            return "No valid json"

    return json_items


def update_table(cur: object, books: list) -> None:
    """
    Update de tabel op basis van de gegeven json data

    :param cur: object, cursor om de sql queries mee te doen
    :param books: list, alle boeken in het json bestand
    """

    for book in books:
        isbn = book['isbn']
        title = book['title']
        author = book['author']
        pages = book['pages']
        year = book['year']

        sq_book_select = "SELECT * FROM `books` WHERE `isbn` = :isbn"
        cur.execute(sq_book_select, {'isbn': isbn})
        existing_book = cur.fetchone()

        if existing_book is None:
            sq_insert_book = "INSERT INTO `books` (isbn, title, author, pages, year) VALUES (?, ?, ?, ?, ?)"
            cur.execute(sq_insert_book, (isbn, title, author, pages, year))


def borrow_book(cur: object, isbn_or_id: str, duration_in_days: int) -> datetime:
    """
    Leen een boek uit en geef terug hoeveel dagen die geleend kan worden
    als die nog niet geleend is.

    :param cur: object, de cursor voor sql queries
    :param isbn_or_id: str, id of isbn om op te zoeken
    :param duration_in_days: int, hoeveel dagen die geleend kan worden

    :return return_date: str, dag wanneer het boek terug gegeven moet worden
    """
    # Controleer of het boek op dit moment niet uitgeleend is
    sq_book_select = \
        "SELECT * FROM `books` WHERE (`isbn` = :isbn OR id = :id) AND `status` = 'AVAILABLE'"
    cur.execute(sq_book_select, {'isbn': isbn_or_id, 'id': isbn_or_id})
    book = cur.fetchone()
    if book is None:
        # Het boek is niet beschikbaar om te lenen
        return None

    # Bereken de datum waarop het boek teruggebracht moet worden
    current_date = datetime.now()
    return_date = current_date + timedelta(days=int(duration_in_days))

    # Werk de beschikbaarheid in de database bij om aan te geven dat het boek
    # is uitgeleend
    sq_update_book = \
        "UPDATE `books` SET `status` = 'BORROWED', `return_date` = :rdate WHERE `isbn` = :isbn OR `id` = :id"
    cur.execute(sq_update_book, {'rdate': return_date, 'isbn': isbn_or_id, 'id': isbn_or_id})

    # Geef de inleverdatum terug
    return time_to_str(return_date, format="%d-%m-%Y")


def return_book(cur: object, isbn_or_id: str) -> str:
    """
    Lever een boek in en geef een boete terug als die gegeven moet worden.

    :param cur: object, cursor object voor sql queries
    :param isbn_or_id: str, welk boek je wilt inleveren

    :return boete: str, hoeveel je moet betalen
    """
    # Zoek het boek met het opgegeven ISBN- of ID-nummer
    sq_book_select = "SELECT * FROM `books` WHERE `isbn` = :isbn OR `id` = :id"
    cur.execute(sq_book_select, {'isbn': isbn_or_id, 'id': isbn_or_id})
    boek = cur.fetchone()

    if boek is None:
        # Het boek bestaat niet
        return None

    # Bereken het aantal dagen dat het boek te laat is ingeleverd
    huidige_datum = datetime.now()

    format = "%Y-%m-%d %H:%M:%S.%f" if len(boek[7].split(" ")) > 1 else "%d-%m-%Y"
    inleverdatum = str_to_time(boek[7], format=format)
    aantal_dagen_te_laat = ceil((huidige_datum - inleverdatum).days)

    # Werk de beschikbaarheid in de database bij om aan te geven dat het boek
    # is ingeleverd
    sq_update_book = \
        "UPDATE `books` SET `status` = 'AVAILABLE', `return_date` = NULL WHERE `isbn` = :isbn OR `id` = :id"
    cur.execute(sq_update_book, {'isbn': isbn_or_id, 'id': isbn_or_id})

    # Als het boek niet te laat is ingeleverd, hoeft er geen boete betaald te worden
    if aantal_dagen_te_laat <= 0:
        return None
    else:
        # Bereken de boete
        boete = (aantal_dagen_te_laat * 0.5) + 0.5  # + 0.5 voor de eerste dag

    # Geef de boete terug
    return f"{boete:.2f}"


def search_book(cur: object, search_term: str) -> list:
    """
    Zoek een boek en geef een lijst met de info van het boek terug

    :param cur: object, cursor voor de sql queries
    :param search_term: str, op wat je wilt zoeken

    :return resultaten: list, lijst met boeken die gevonden zijn
    """
    # Zoek naar boeken met de opgegeven zoekterm in de titel, ISBN- of auteur
    sq_book_select = "SELECT * FROM `books` WHERE `title` LIKE :title OR `isbn` = :isbn OR `author` = :author"
    sq_book_data = {'title': '%' + search_term + '%', 'isbn': search_term, 'author': search_term}
    cur.execute(sq_book_select, sq_book_data)
    boeken = cur.fetchall()
    if len(boeken) == 0:
        # Er zijn geen boeken gevonden
        return None

    # Geef de boekinformatie en -status terug
    resultaten = []
    for boek in boeken:
        # Maak een dict met informatie over het boek
        boek_info = {
            'id': boek[0],
            'isbn': boek[1],
            'title': boek[2],
            'author': boek[3],
            'pages': boek[4],
            'year': boek[5],
            'status': boek[6],
            'return_date': boek[7]
        }

        # Voeg het boek toe aan de resultaten
        resultaten.append(boek_info)

    return resultaten


def main():
    con = sqlite3.connect(os.path.join(sys.path[0], 'bookstore.db'))
    cur = con.cursor()
    cur.execute(
        '''CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            isbn TEXT NOT NULL,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            pages INTEGER NOT NULL,
            year TEXT NOT NULL,
            status TEXT DEFAULT "AVAILABLE",
            return_date DATE DEFAULT NULL
        );'''
    )

    books = json_to_list("books.json")
    update_table(cur, books)
    con.commit()

    print("""[B] Borrow book
[R] Return book
[S] Search book
[Q] Quit""")

    quit_program = False
    while quit_program is False:
        command = input("> ").lower()

        if command == "q":
            quit_program = True
        elif command == "b":
            what_book = input("isbn/id > ")
            days_amount = input("days > ")
            print(borrow_book(cur, what_book, days_amount))
            con.commit()
        elif command == "r":
            what_book = input("isbn/id > ")
            print(return_book(cur, what_book))
            con.commit()
        elif command == "s":
            search_term = input("search > ")
            print("\n".join([str(row) for row in search_book(cur, search_term)]))

    con.close()


if __name__ == "__main__":
    main()
