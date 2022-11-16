from os import path
import random


def create_password(file_path: str) -> str:
    """
    Maak een wachtwoord op basis van 2 woorden
    uit het meegegeven bestand. De woorden moeten
    minimaal 3 letters zijn en het wachtwoord max 8 - 10 letters.

    :param file_path: str, pad naar het bestand

    :return password: str, het gemaakte wachtwoord
    """
    # variable waar uiteindelijk het wachtwoord komt
    password = ""
    # maak een random lengte van 8 tot 10
    random_length = random.randint(8, 10)

    # two words is de twee woorden waar een wachtwoord van wordt gemaakt
    two_words = []

    # open het bestand en stop de worden zonder \n en die een lengte hebben
    # van minimaal 3 letters in de list all words om een random woord uit te
    # kiezen.
    all_words = []
    with open(file_path, "r") as file:
        all_words = [word.replace("\n", "") for word in file.readlines() if len(word) >= 3]

    # kies het eerste word haal de lengte daarvan van de random lengte
    # om de woorden die nog gekozen kunnen worden te kunnen filteren.
    # voeg dit woord ook toe aan de two words list.
    first_word = random.choice(all_words)
    allowed_len = len(first_word) - random_length
    two_words.append(first_word.capitalize())

    # filter voor de gemogen woorden in de lijst
    all_words = list(filter(lambda x: len(x) >= allowed_len, all_words))

    # kies een tweede woord en voeg die aan de lijst toe.
    second_word = random.choice(all_words)
    two_words.append(second_word.capitalize())

    # maak een string van de two words lijst
    password = "".join(two_words)
    return password


def main() -> str:
    """
    Main functie om waar het programma vanuit wordt
    gedraaid
    """
    input_file = input("")
    if len(input_file) < 0:
        return "No input file given!"

    # als het bestand niet bestaat moet je een error krijgen
    if path.exists(input_file) is not True:
        return "File does not exists!"

    return create_password(input_file)


if __name__ == "__main__":
    print(main())
