def is_palindrome(word):
    """
    Functie om te checken of een woord een palindrome is.
    zoals civic is hetzelfde omgedraaid. (zonder loop)

    @param string word - woord om te checken

    @return bool - of het een palindrome is
    """
    return word == word[::-1]


def is_palindrome_w(word):
    """
    Functie om te checken of een woord een palindrome is.
    zoals civic is hetzelfde omgedraaid. (while loop)

    @param string word - woord om te checken

    @return bool - of het een palindrome is
    """
    # om de eerste en laatste index van een woord te krijgen
    first, last = 0, len(word) - 1

    while first < last:
        if word[first] == word[last]:
            first += 1
            last -= 1
        else:
            return False

    return True


def is_palindrome_f(word):
    """
    Functie om te checken of een woord een palindrome is.
    zoals civic is hetzelfde omgedraaid. (for loop)

    @param string word - woord om te checken

    @return bool - of het een palindrome is
    """
    reversed_str = ""
    for i in range(len(word), 0, -1):
        reversed_str += word[i - 1]

    return reversed_str == word


woord = input("Woord:\n")

print(is_palindrome(woord))
print(is_palindrome_w(woord))
print(is_palindrome_f(woord))
