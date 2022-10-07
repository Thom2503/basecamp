from random import sample, randint
import string


def generate_random_password():
    """
    Functie om een random wachtwoord te genereren van 7 tot 10 karakters die gebruik
    maakt van de 33 tot 126 karakters in de ASCII Table.

    @return string password - het random wachtwoord
    """
    # alle karakters in de ASCII Table die we kunnen gebruiken
    lower_letters = string.ascii_lowercase
    upper_letters = string.ascii_uppercase
    numbers = string.digits
    symbols = string.punctuation
    # combineer de karakters
    all = lower_letters + upper_letters + numbers + symbols
    # maak het wachtwoord met gebruik van random.sample die random elementen uit een
    # lijst kan pakken met een bepaalde lengte (dit is dan random 7-10)
    password = "".join(sample(all, randint(7, 10)))

    return password


if __name__ == "__main__":
    print(generate_random_password())
