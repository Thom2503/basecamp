from os import path


def get_words(file_path: str) -> list:
    """
    Maak een lijst met alle woorden in het bestand.

    :param file_path: str, pad naar het bestand

    :return words: list, lijst met woorden
    """
    words = []
    with open(file_path) as file:
        for line in file.readlines():
            for word in line.split(" "):
                word = word.replace("\n", "")
                words.append(word)

    return words


def redact_words(input_file: str, output_file: str, sensitive_words: list):
    """
    Maak een nieuw bestand waar alle woorden die "sensitive" zijn
    geredact worden met * in plaats dan de letters

    :param input_file: str, pad van het bestand dat gelezen word
    :param output_file: str, pad naar het nieuwe bestand
    :param sensitive_words: list, de worden die geredact moeten worden
    """
    content = []
    with open(input_file, "r") as in_file:
        content = in_file.readlines()

    for idx, line in enumerate(content):
        has_word = [ele for ele in sensitive_words if ele in line]
        if has_word:
            for word in has_word:
                content[idx] = content[idx].replace(word, "*" * len(word))

    with open(output_file, "w") as out_file:
        out_file.writelines(content)


def main() -> str:
    """
    Main functie om waar het programma vanuit wordt
    gedraaid
    """
    input_file = input("")
    if len(input_file) < 0:
        return "No input file given!"

    sensitive_file = input("")
    if len(sensitive_file) < 0:
        return "No sensitive words file given!"

    output_file = input("")
    if len(output_file) < 0:
        return "No output file given!"

    # als het bestand niet bestaat moet je een error krijgen
    for file in [input_file, sensitive_file]:
        if path.exists(file) is not True:
            return "File does not exists!"

    sensitive_words = get_words(sensitive_file)

    redact_words(input_file, output_file, sensitive_words)
    return "Success!"


if __name__ == "__main__":
    print(main())
