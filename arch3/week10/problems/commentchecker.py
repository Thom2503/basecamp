from os import path


def make_text(file_path: str, line: str, line_number: int) -> str:
    """
    Functie om een string te maken zoals:
    File: functiontest.txt contains a function [function_name_here()] on line [1] without a preceding comment.

    :param file_path: str, pad naar bestand
    :param line: str, over welke lijn die text gemaakt moet worden
    :param line_number: int, nummer van de lijn

    :return text: str, tekst zoals boven
    """
    # pak de naam van de functie na def
    # haal ook de : en \n weg want je wilt alleen de functie naam
    function_name = line.partition("def ")[2]
    function_name = function_name.replace(":", "")
    function_name = function_name.replace("\n", "")

    # f string waar alle belangrijke info in kan komen
    text = \
        f"File: {file_path} contains a function [{function_name}] on line [{line_number}] without a preceding comment."

    return text


def check_comments(file_path: str) -> list:
    """
    Maak een lijstje met de lijnen waar functies staan
    die nog geen functie doc hebben

    :param input_file: str, pad naar het bestand
    """
    lines_without = []
    with open(file_path, "r+") as in_file:
        content = in_file.readlines()
        content = [line.strip() for line in content]
        for idx, line in enumerate(content):
            if line.startswith("def "):
                next_line = content[idx - 1]
                if next_line.startswith("#") is not True:
                    error_text = make_text(file_path, line, idx + 1)
                    lines_without.append(error_text)

    return lines_without


def main() -> str:
    """
    Main functie om waar het programma vanuit wordt
    gedraaid

    :return str, fout of success
    """
    checked_comments = []

    files = input("").replace(" ", "").split(",")

    for file in files:
        # als het bestand niet bestaat moet je een error krijgen
        if path.exists(file) is not True:
            return "File does not exists!"

        checked_comments.append("\n".join(check_comments(file)))

    return "\n".join(checked_comments)


if __name__ == "__main__":
    print(main())
