from os import path
import sys


def read_file(file_path: str) -> str:
    """
    Lees de eerste 10 lines in een bestand.
    """
    # een lijst met de individuele lijnen om de eerste
    # 10 van te krijgen
    file_lines = []

    # open het bestand om het uit te lezen
    with open(file_path, "r+") as file:
        content = file.read()
        # split de gelezen content om aan de
        # lijst toe te voegen
        file_lines += content.split("\n")

    # maak een string van de eerste 10 lines
    return "\n".join(file_lines[0:10])


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

    return read_file(input_file)


if __name__ == "__main__":
    print(main())
