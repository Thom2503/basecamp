"""
Ik zou deze oplossing eerder met een set doen want het is sneller
en bij een dictionary moet je ook nog een nutteloze value mee
geven
"""


def unique_chars_dict(text):
    """
    Functie om te checken op unieke tekens in een string deze gebruikt een dictionary

    @param string text - string om de unieke characters te zoeken

    @return int unique_amount - het aantal unieke tekens
    """
    # de dictionary om de letters mee te vullen
    # de keys worden de chars en keys moeten uniek zijn
    # dus dubbellen zullen er uit gehaald worden
    char_dict = {char: '' for char in text}
    # de lengte van de dictionary is hoeveel unieke tekens er zijn
    unique_amount = len(char_dict)

    return unique_amount


def unique_chars_set(text):
    """
    Functie om te checken op unieke tekens in een string deze gebruikt een set
    een set moet net als de keys bij een dictionary uniek zijn

    @param string text - string om de unieke characters te zoeken

    @return int unique_amount - het aantal unieke tekens
    """
    # zet de string om in een set die pakt al namelijk alle
    # unieke tekens
    char_set = set(text)
    # de lengte van de set is hoeveel unieke tekens er zijn
    unique_amount = len(char_set)

    return unique_amount


if __name__ == "__main__":
    input_text = input("What text to check for unique characters\n")

    print(unique_chars_dict(input_text))
    print(unique_chars_set(input_text))
