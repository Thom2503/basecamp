def remove_non_integer(x):
    """
    Functie om alle niet getallen uit de string te verwijderen

    @param string x - string om alle niet getallen te verwijderen

    @return string - string met alleen getallen
    """
    # lijst met alle karakters die wel mogen in de string
    valid_characters = ('1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '+')
    # lege string voor de nieuwe string met alle correcte getallen er in
    valid_integer = ""
    # loop door de input string om alle getallen die in x zitten toe te voegen aan valid_integer
    for c in x.replace(" ", ""):
        if c in valid_characters:
            valid_integer += c
    # dit is om bij te houden of er een 0 is in de string voor een ander getal zoals 023
    has_zeroes = False
    # voer dit alleen uit als het start met - of + anders moeten die ook verwijderd worden
    if valid_integer.startswith("-") or valid_integer.startswith("+"):
        # loop door de nieuwe valid_integer heen om te checken of er een 0 is met een ander getal
        for idx, c in enumerate(valid_integer[1:]):
            # als er een 0 is met een ander getal moet je true en dan kunnen die verwijderd worden
            if c == "0" and valid_integer[idx + 1] == "0":
                has_zeroes = True
        # als er dus nullen voor een ander getal zijn strip die dan van de string
        if has_zeroes:
            valid_integer = valid_integer[0] + valid_integer[1:].lstrip("0")
    else:
        # verwijder de + en - van de string
        valid_integer = valid_integer.replace("-", "")
        valid_integer = valid_integer.replace("+", "")

    return valid_integer


def is_integer(x):
    """
    Functie om te checken of de input een integer is.

    @param string x - input om te checken

    @return bool - of het een integer is
    """
    # zorg dat de spatie weg is en alle tekens klein zijn, je kan spaties namelijk negeren
    string = x.replace(" ", "").lower()
    # alle cijfers die waarop gecheckt kan worden en die het correct maken
    valid_integers = ('1', '2', '3', '4', '5', '6', '7', '8', '9', '0')
    # als het minder dan 1 karakter lang is mag je het allemaal overslaan en is het geen integer
    if len(string) < 1:
        return False
    # loop door de string heen om per karakter te checken of het een cijfer is
    for char in string:
        # als het eerste karakter een plus of min is kan je die overslaan want dat mag ook
        if string[0] in ('-', '+'):
            continue
        if char not in valid_integers:
            return False

    return True


if __name__ == "__main__":
    string_to_check = input("Check if it's an integer\n")
    # als het een goede integer is dan moet je terug geven "is integer" anders "is not an integer"
    is_valid_integer = "valid" if is_integer(string_to_check) else "invalid"
    print(is_valid_integer)
