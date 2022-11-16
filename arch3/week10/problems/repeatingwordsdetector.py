from os import path


def make_text(dup_word: str, line_number: int) -> str:
    """
    Functie om een string te maken zoals:
    Found duplicate word [something] on line: 10

    :param dup_word: str, het gevonden woord
    :param line_number: int, nummer van de lijn

    :return text: str, tekst zoals boven
    """

    # f string waar alle belangrijke info in kan komen
    text = f"Found duplicate word [{dup_word}] on line: {line_number}"

    return text


def get_repeated(file_path: str) -> list:
    """
    Zoek de woorden die herhaald worden achter elkaar,
    en stop die in een lijstje, met de tekst uit make_text()

    :param file_path: str, pad naar bestand

    :return found_duplicates: list, lijstje met alle herhaalde woorden
    """
    found_duplicates = []
    words = []

    with open(file_path) as file:
        for idx, line in enumerate(file.readlines()):
            for word in line.split(" "):
                words.append((word.replace("\n", ""), idx + 1))
    # om bij te houden waar we zijn voor het volgende woord
    i = 0
    for word, line_number in words:
        try:
            if word == words[i + 1][0]:
                found_duplicates.append(make_text(word, line_number))
        except IndexError:
            break
        i += 1

    return found_duplicates


def delete_line(file_path: str, line: str):
    """
    Verwijder het herhaalde woord van de lijn in het meegegeven bestand

    :param file_path: str, pad naar bestand
    :param line: str, de info van de lijn waar het fout gaat
    """
    content = []
    line_number = int(line.partition("line: ")[2]) - 1

    with open(file_path, "r") as in_file:
        content = in_file.readlines()

    content[line_number] = " ".join(dict.fromkeys(content[line_number].split()))

    with open(file_path, "w") as out_file:
        out_file.writelines(content)


def main() -> str:
    """
    Main functie om waar het programma vanuit wordt
    gedraaid
    """
    input_file = input("")
    if len(input_file) < 0:
        return "No file given!"

    # als het bestand niet bestaat moet je een error krijgen
    if path.exists(input_file) is not True:
        return "File does not exists!"

    repeated_words = get_repeated(input_file)
    if len(repeated_words) == 0:
        return "No duplicates found!"
    else:
        for repeated_word in repeated_words:
            print(repeated_word)
            command = input("").lower()
            if command != "continue":
                delete_line(input_file, repeated_word)


if __name__ == "__main__":
    print(main())
