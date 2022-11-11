from os import path
import sys


def add_linenumbers(read_file: str, write_file: str) -> None:
    """
    Voeg lijn nummers toe aan het bestand
    """
    # open beide de input en output bestanden om te lezen
    # en te kunnen schrijven.
    with open(read_file, "r") as file_r:
        with open(write_file, "w") as file_w:
            # loop door het gelezen bestand met enumerate
            # om ook de lijn nummer te krijgen.
            for i, line in enumerate(file_r):
                file_w.write(f"{i}: {line}")


def main() -> str:
    """
    Main functie om waar het programma vanuit wordt
    gedraaid
    """
    # probeer het tweede element uit argv op te halen
    # daar is namelijk het bestand die we willen uitlezen
    try:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
    except IndexError:
        # als de tweede element in argv leeg is is er geen file mee gegeven
        return "No parameter given!"

    # als het bestand niet bestaat moet je een error krijgen
    if path.exists(input_file) is not True:
        return "File does not exists!"

    add_linenumbers(input_file, output_file)
    return "Linenumbers added!"


if __name__ == "__main__":
    print(main())
