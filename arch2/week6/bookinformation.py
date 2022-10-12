# boeken dictionary met als key een titel en als value
# de data van het boek, zoals auteur, uitgever en uitgeef datum
# eerste is voorbeeld data.
# 'title':'Norwegian Wood','author':'Haruki Murakami','publisher':'Vintage','pub_date':'1985'
BOOKS = []


def fetch_book_data(books, term):
    """
    Print de data uit van het boek, zodat je iets terug krijgt bij het zoeken van je boek

    @params list books  - de boeken
    @params string term - waar je op zoekt

    @return string - info van het boek
    """

    if search_book(books, term) is True:
        return f"found {term}"

    return "No book found"


def search_book(books, term):
    """
    Functie om te zoeken naar een boek in de lijst.

    @param list   books - de boeken lijst
    @param string term  - term van het boek om naar te zoeken

    @return bool - informatie van het boek of dat het niet bestaat
    """
    for book in books:
        if term in (book['title'], book['author'], book['publisher']):
            return True

    return False


def create_book(title, author, publisher, date):
    """
    Functie om een boek toe te voegen aan de BOOKS dictionary deze dictionary
    gebruikt alle parameters.

    @param string title     - boek titel
    @param string author    - boek auteur
    @param string publisher - boek uitgever
    @param string date      - boek uitgeef datum

    @return bool|void - bool als het al bestaat, void als het niet bestaat
    """
    # eerst checken of het boek al bestaat ga dan niet door
    if search_book(BOOKS, title):
        print("Book already exists!")
        return False

    new_book = {'title': title, 'author': author, 'publisher': publisher, 'pub_date': date}

    BOOKS.append(new_book)
    print(new_book)


def main():
    """
    De main loop die waar alles in geregeld wordt zoals de interface enzo.
    """
    # om bij te houden of je het programma moet sluiten
    program_exit = False
    # print het menu uit
    print("Your book collection!")
    print("(a)dd - (s)earch - (e)xit")
    while program_exit is False:
        # command van de gebruiker om te weten of iets toegevoegd/gezocht/beiendigd moet worden
        command = input().lower()
        if command in ('e', 'exit'):
            program_exit = True  # zet op true zodat de while loop wordt gestopt
        elif command in ('a', 'add'):
            new_book_input = input()
            # als er geen comma's in zitten mag het programma niet doorgaan
            if "," not in new_book_input:
                print("Not in correct format")
                continue
            else:
                # neem de verschillende onderdelen van het nieuwe boek en voeg die
                # toe met de create_book functie de gebruiker krijgt terug te zien
                # wat ze toegevoegd hebben
                book_data = new_book_input.split(",")
                create_book(book_data[0], book_data[1], book_data[2], book_data[3])
        elif command in ('s', 'search'):
            search_command = input()
            # zoek het boek en stop deze in een variable om die uit te kunnen printen
            book = search_book(BOOKS, search_command)
            if book:
                print(fetch_book_data(BOOKS, search_command))
            else:
                print("No book found")


if __name__ == "__main__":
    main()
