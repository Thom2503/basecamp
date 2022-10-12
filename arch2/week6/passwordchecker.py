def is_valid_password(password):
    """
    Check of het wachtwoord dat ingevoerd is een goed wachtwoord is,
    dit wachtwoord moet meer dan 8 maar niet meer dan 20 tekens zijn,
    kleine-, grote letters hebben getallen en een van deze vier symbolen: ? * @ !

    @param string password - wachtwoord om te checken

    @return bool - of het een goed wachtwoord is
    """
    # eerst checken of het niet te kort is of te lang
    # want dat mag niet
    if len(password) < 8 or len(password) > 20:
        return False
    # lijst met de toegestaande symbolen
    valid_symbols = {'?', '*', '@', '!'}
    # alle toegestaande letters en cijfers in sets
    valid_lowercase = set("abcdefghijklmnopqrstuvwxyz")
    valid_uppercase = set(letter.upper() for letter in valid_lowercase)
    valid_digits = set("0123456789")
    # alle sets bij elkaar om later de set operation te kunnen gebruiken
    all_sets = (valid_symbols, valid_lowercase, valid_uppercase, valid_digits)
    # stop het wachtwoord in een set
    password_set = set(password)
    # de nieuwe set waar als er 0 in zit moet het een correct wachtwoord zijn
    new_set = {}
    i = 0
    while i < len(all_sets):
        # de nieuwe set moet eerst beginnen met de password set
        # daarna moet het verder met de overgebleven dingen in de
        # nieuwe set
        if i == 0:
            # update de password set zonder de tekens, en zet deze
            # in een nieuwe set die op de rest gecheckt gaat worden
            password_set.difference_update(all_sets[i])
            new_set = password_set
        else:
            # als een intersection niks terug geeft zijn mist het
            # nodige tekens en kan je False returnen want dan is
            # het niet valid
            # if len(new_set & all_sets[i]) > 0:
            if len(new_set.intersection(all_sets[i])) > 0:
                new_set = new_set - all_sets[i]
            else:
                return False
        i += 1

    # als er nog dingen over zijn is het geen goed wachtwoord
    if len(new_set) > 0:
        return False

    return True


if __name__ == "__main__":
    tries = 3
    while tries > 0:
        pass_input = input("Password:\n")
        is_valid = is_valid_password(pass_input)
        if is_valid:
            print("valid")
            break
        else:
            print("invalid")
            tries -= 1
