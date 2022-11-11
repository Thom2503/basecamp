from os import path
import fileinput
import sys


def add_linenumbers(file_path: str) -> None:
    """
    Voeg lijn nummers toe aan het bestand
    """

    # open het bestand met fileinput om het uit te lezen
    # inplace is zodat je de het bestand veranderd op de lijn
    # terwijl je stdout gebruikt
    for line in fileinput.input(files=file_path, inplace=True):
        # schrijf via de standard output naar de file
        # gebruik filelineno van fileinput om de het lijn nummer
        # te krijgen
        sys.stdout.write(f"{fileinput.filelineno()} {line}")


def main() -> str:
    """
    Main functie om waar het programma vanuit wordt
    gedraaid
    """
    # probeer het tweede element uit argv op te halen
    # daar is namelijk het bestand die we willen uitlezen
    try:
        input_file = sys.argv[1]
    except IndexError:
        # als de tweede element in argv leeg is is er geen file mee gegeven
        return "No parameter given!"

    # als het bestand niet bestaat moet je een error krijgen
    if path.exists(input_file) is not True:
        return "File does not exists!"

    add_linenumbers(input_file)
    return "Linenumbers added!"


if __name__ == "__main__":
    print(main())
