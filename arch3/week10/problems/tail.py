from os import path
import sys


def read_file_once(file_path: str) -> str:
    """
    Lees de eerste 10 lines in een bestand.
    """
    # open het bestand om het uit te lezen
    with open(file_path, "r+") as file:
        return "\n".join(file.read().split("\n")[-10:])


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

    return read_file_once(input_file)


if __name__ == "__main__":
    print(main())
