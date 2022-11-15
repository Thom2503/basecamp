from os import path


def remove_comments(input_file: str, output_file: str):
    """
    Functie om de comments van een python file te verwijderen.
    Als een lijn begint met een "#" dan is het een comment en
    kan alles daarna verwijderd worden.

    :param input_file: str, pad naar het bestand
    :param output_file: str, pad naar het nieuw bestand
    """
    with open(input_file, "r+") as in_file:
        with open(output_file, "w+") as out_file:
            content = in_file.readlines()
            for line in content:
                if line.startswith("#") is not True:
                    out_file.write(line)


def main() -> str:
    """
    Main functie om waar het programma vanuit wordt
    gedraaid

    :return str, fout of success
    """
    input_file = input("")
    if len(input_file) < 0:
        return "No input file given!"

    output_file = input("")
    if len(output_file) < 0:
        return "No output file given!"

    # als het bestand niet bestaat moet je een error krijgen
    if path.exists(input_file) is not True:
        return "File does not exists!"

    remove_comments(input_file, output_file)
    return "Success!"


if __name__ == "__main__":
    print(main())
