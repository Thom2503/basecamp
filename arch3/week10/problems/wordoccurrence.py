from os import path
import string


def find_longest_words(file_path: str) -> str:
    """
    zoek de minst en meest voor komende woorden in een bestand.

    :param read_file: str, bestand waar gezocht wordt

    :return text: str, minst en meest voorkomende woorden
    """
    all_words = {}

    with open(file_path, "r") as file:
        content = file.read()
        content = content.replace("\n", " ")
        content = content.replace("\t", "")
        content = "".join(list(filter(lambda x: x not in string.punctuation, content)))

        for word in content.split(" "):
            word = word.lower()
            if word == "":
                continue
            if word not in all_words.keys():
                all_words.update({word: 1})
            else:
                count = all_words[word] + 1
                all_words.update({word: count})

    least = min(all_words.values())
    most = max(all_words.values())

    least_words = [word for word, v in all_words.items() if v == least]
    most_words = [word for word, v in all_words.items() if v == most]

    text = " ".join(least_words) + "\n" + " ".join(most_words)

    return text


def main() -> str:
    """
    Main functie om waar het programma vanuit wordt
    gedraaid

    :return str, minst een meest voorkomende woorden
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
