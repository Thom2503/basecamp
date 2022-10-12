MORSE_CODE_DICT = {
    'A': '.-', 'B': '-...',
    'C': '-.-.', 'D': '-..', 'E': '.',
    'F': '..-.', 'G': '--.', 'H': '....',
    'I': '..', 'J': '.---', 'K': '-.-',
    'L': '.-..', 'M': '--', 'N': '-.',
    'O': '---', 'P': '.--.', 'Q': '--.-',
    'R': '.-.', 'S': '...', 'T': '-',
    'U': '..-', 'V': '...-', 'W': '.--',
    'X': '-..-', 'Y': '-.--', 'Z': '--..',
    '1': '.----', '2': '..---', '3': '...--',
    '4': '....-', '5': '.....', '6': '-....',
    '7': '--...', '8': '---..', '9': '----.',
    '0': '-----', ',': '--..--', '.': '.-.-.-',
    '?': '..--..'
}


def message_to_morse(message):
    """
    Functie om tekst zoals "Hello" naar morse code te veranderen

    @param string message - het bericht om te vertalen

    @return string morse - de morse code
    """
    morse = ""

    for letter in message.upper():
        if letter in MORSE_CODE_DICT.keys():
            morse += f"{MORSE_CODE_DICT[letter]} "
        elif letter == " ":
            morse += "    "
        else:
            return f"Can't convert char [{letter}]"

    return morse


def search_letter(code):
    """
    Vind de key van met de code als value

    @param string code - de value waar de key van gevonden moet worden

    @return string - de key in de dictionary
    """
    for key in MORSE_CODE_DICT:
        if MORSE_CODE_DICT[key] == code:
            return key


def morse_to_message(morse):
    """
    Functie om morse code te vertalen naar bijv: "hallo".

    @param string morse - de morse code om te vertalen

    @return string message - het vertaalde bericht
    """
    message = ""

    morse = morse.replace("     ", " # ")  # dankje jurn :)

    for code in morse.split(" "):
        if code in MORSE_CODE_DICT.values():
            message += search_letter(code)
        elif code == "#":
            message += " "
        else:
            return f"Can't convert code [{code}]"

    return message.lower()


def translate_text(to_translate):
    """
    Check wat voor soort tekst het is en vertaal die dan
    met de goede functie.

    @param string to_translate - tekst om te vertalen

    @return string - vertaling van de tekst
    """

    for char in to_translate.split():
        if char in MORSE_CODE_DICT.values():
            return morse_to_message(to_translate)
        else:
            return message_to_morse(to_translate)


if __name__ == "__main__":
    message_input = input("Message to convert:\n")
    print(message_to_morse(message_input))
