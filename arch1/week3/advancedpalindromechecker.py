PUNCTUATIONS = ['!', '?', ',', '.', ';'] # lijstje met speciale tekens die niet mogen

# functie voor filter om te checken of een deel van de string in punctuations voor komt
filter_puncts = lambda c : c not in PUNCTUATIONS


def is_palindrome(text):
    """
    Functie om te checken of een woord/zin een palindrome is.
    zoals civic of go dog is hetzelfde omgedraaid. (zonder loop)

    @param string text - woord/zin om te checken

    @return bool - of het een palindrome is
    """
    # om spaties en speciale tekens weg te halen en de tekst naar kleine letters te veranderen
    text = "".join((filter(filter_puncts, text.lower()))).replace(" ", "")
    return text == text[::-1]


def is_palindrome_w(text):
    """
    Functie om te checken of een woord/zin een palindrome is.
    zoals civic of go dog is hetzelfde omgedraaid. (while loop)

    @param string text - woord/zin om te checken

    @return bool - of het een palindrome is
    """
    # om spaties en speciale tekens weg te halen en de tekst naar kleine letters te veranderen
    text = "".join((filter(filter_puncts, text.lower()))).replace(" ", "")
    # om de eerste en laatste index van een woord te krijgen
    first, last = 0, len(text) - 1

    while first < last:
        if text[first] == text[last]:
            first += 1
            last -= 1
        else:
            return False

    return True


def is_palindrome_f(text):
    """
    Functie om te checken of een woord/zin een palindrome is.
    zoals civic of go dog is hetzelfde omgedraaid. (for loop)

    @param string text - woord/zin om te checken

    @return bool - of het een palindrome is
    """
    # om spaties en speciale tekens weg te halen en de tekst naar kleine letters te veranderen
    text = "".join((filter(filter_puncts, text.lower()))).replace(" ", "")
    reversed_str = ""
    for i in range(len(text), 0, -1):
        reversed_str += text[i - 1]

    return reversed_str == text


tekst = input("Woord/Zin:\n")

print(is_palindrome(tekst))
print(is_palindrome_w(tekst))
print(is_palindrome_f(tekst))
