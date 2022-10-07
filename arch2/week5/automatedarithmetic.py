from random import randint


def arithmetic_operation(arithmetic_type):
    """
    Functie om te oefenen op een bepaald rekensom, zoals plus, min en keer.

    @param string arithmetic_type - plus, min, keer
    """
    # de oefeningen die gedaan kunnen worden om te oefenen. Dit is een dictionary
    # met als key de oefeningen en als value een lijst met de operator en en functie met
    # de operator die gebruikt kan worden.
    types = {
        'summation': [lambda x, y: x + y, "+"],
        'multiplication': [lambda x, y: x * y, "*"],
        'subtraction': [lambda x, y: x - y, "-"]
    }
    # de functie definitie op basis van de parameter en de operator (+, -, *) enz.
    # de operator wordt gebruikt in het printen van bijv. 1 + 1 =
    arithmetic_function = types[arithmetic_type][0]
    arithmetic_operator = types[arithmetic_type][1]
    # Er moeten 10 sommen geoefend worden
    for i in range(1, 10):
        # de twee random getallen om mee te oefenen
        a, b = randint(1, 100), randint(1, 100)
        # de oefening en waar de gebruiker het antwoord kan invullen
        answer = int(input(f"{a} {arithmetic_operator} {b} = "))
        # check of het antwoord correct is
        if answer == arithmetic_function(a, b):
            print("Correct")
        else:
            print("Not correct")


if __name__ == "__main__":
    type = input("Type to learn: \n")
    arithmetic_operation(type)
