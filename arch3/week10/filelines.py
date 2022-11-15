from os import path


def add_linenumbers(read_file: str, write_file: str) -> None:
    """
    Voeg lijn nummers toe aan het bestand

    :param read_file: str, welk bestand je wilt lezen
    :param write_file: str, bestand waar de content + lijn nummer van read_file komt

    :return None
    """
    # open beide de input en output bestanden om te lezen
    # en te kunnen schrijven.
    with open(read_file, "r") as file_r:
        with open(write_file, "w") as file_w:
            # loop door het gelezen bestand met enumerate
            # om ook de lijn nummer te krijgen.
            for i, line in enumerate(file_r):
                file_w.write(f"{i}. {line}")


def main() -> str:
    """
    Main functie om waar het programma vanuit wordt
    gedraaid
    """

    input_file = input("Input file:\n")
    output_file = input("Output file:\n")

    # als het bestand niet bestaat moet je een error krijgen
    if path.exists(input_file) is not True:
        return "File does not exists!"

    add_linenumbers(input_file, output_file)
    return "Linenumbers added!"


if __name__ == "__main__":
    print(main())
