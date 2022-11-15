from os import path


def find_longest_words(file_path: str) -> str:
    """
    Zoek de langste woorden in een bestand.

    :param read_file: str, bestand waar gezocht wordt

    :return longest_words: str, langste woord met hoe vaak het voor kwam
    """
    all_words = {}
    longest_words = []

    with open(file_path, "r+") as file:
        content = file.read()
        content = content.replace("\n", " ")
        content = content.replace("\t", "")

        for word in content.split(" "):
            if word not in all_words.keys():
                all_words.update({word: 1})
            else:
                count = all_words[word] + 1
                all_words.update({word: count})

    # sorteer de lijst op de langste woorden
    sorted_words = sorted(all_words.keys(), key=lambda x: len(x), reverse=True)

    for word, count in all_words.items():
        if len(word) >= len(sorted_words[0]):
            longest_words.append(word)

    return " ".join(longest_words)


def main() -> str:
    """
    Main functie om waar het programma vanuit wordt
    gedraaid

    :return str, langste woord in het megegeven bestand
    """
    input_file = input("")
    if len(input_file) < 0:
        return "No parameters given!"

    # als het bestand niet bestaat moet je een error krijgen
    if path.exists(input_file) is not True:
        return "File does not exists!"

    return find_longest_words(input_file)


if __name__ == "__main__":
    print(main())
