import sys

encoded_values = []
decoded_values = []


def set_hashmap(key: str) -> None:
    hashmap_key_value = {}
    # maak met zip 2 lijstjes (dit zijn de even en oneven karakters)
    # die met dict een dictionary worden
    hashmap_key_value = dict(zip(key[::2], key[1::2]))
    return hashmap_key_value


def search_letter(code: str, hashmap_key_value: dict) -> str:
    """
    Vind de key van met de code als value

    @param string code - de value waar de key van gevonden moet worden
    @param dict   hashmap_key_value - key_value voor de encoding

    @return string - de key in de dictionary
    """
    for key in hashmap_key_value:
        if hashmap_key_value[key] == code:
            return key


def encode_function(data: str) -> str:
    """
    decode de meegegeven char

    :param data: str, string om te encoden
    """
    encoded = ""
    # als de key even is kan er een hash map van gemaakt worden
    hashmap_key_value = set_hashmap("a_b?c9d6e1f4g!h:i<j|k{l0m@n7o+p~q2r+s/t=u^v3w]x(y-z>A*B8C;D%E#F}G5H)I[J$")

    for char in data:
        if char in hashmap_key_value:
            encoded += hashmap_key_value[char]
        else:
            encoded += char
    return encoded


def decode_function(data: str) -> str:
    """
    decode de meegegeven char

    :param data: str, string om te decoden
    """
    decoded = ""
    # als de key even is kan er een hash map van gemaakt worden
    hashmap_key_value = set_hashmap("a_b?c9d6e1f4g!h:i<j|k{l0m@n7o+p~q2r+s/t=u^v3w]x(y-z>A*B8C;D%E#F}G5H)I[J$")

    for char in data:
        if char in hashmap_key_value.values():
            decoded += search_letter(char, hashmap_key_value)
        else:
            decoded += char
    return decoded


def encode_string(data: str, encode_function) -> str:
    return encode_function(data)


def decode_string(data: str, decode_function) -> str:
    return decode_function(data)


def encode_list(data: list, encode_function) -> list:
    # map over de lijst heen en encode het dan allemaal
    # *lambda kan weg maar moet helaas van codegrade :P*
    return list(map(lambda data_str: encode_string(data_str, encode_function), data))


def decode_list(data: list, decode_function) -> list:
    # map over de lijst heen en decode alles
    return list(map(lambda data_str: decode_string(data_str, decode_function), data))


def validate_values(encoded: str, decoded: str, decode_function) -> bool:
    # vergelijk of de encoded string hetzelfde is als de
    # decoded string door de encoded string te decoden
    # zo hoef je alleen met 1 iets te doen
    return decode_string(encoded, decode_function) == decoded


# build menu structure as following
# the input can be case-insensitive (so E and e are valid inputs)
# [E] Encode value to hashed value
# [D] Decode hashed value to normal value
# [P] Print all encoded/decoded values
# [V] Validate 2 values against eachother
# [Q] Quit program
def main():
    # zet de key om mee te hashen
    print("""[E] Encode value to hashed value
[D] Decode hashed value to normal value
[P] Print all encoded/decoded values
[V] Validate 2 values against eachother
[Q] Quit program""")
    # vraag de gebruiker voor een commando
    command = input().lower()
    if command == "q":
        # als je q invult moet je het programma stoppen
        sys.exit()
    elif command == "e":
        value_to_encode = input("Input a value to encode:\n")
        # als er een comma in de input staat moeten er meerdere
        # worden geencode worden dus maak daar een lijstje van en
        # voeg die aan de lijst toe
        if "," in value_to_encode:
            values_to_encode = value_to_encode.replace(", ", ",").split(",")
            decoded_values.extend(values_to_encode)
        else:
            decoded_values.append(value_to_encode)
    elif command == "d":
        value_to_decode = input("Enter a value to decode:\n")
        if "," in value_to_decode:
            values_to_decode = value_to_decode.replace(", ", ",").split(",")
            encoded_values.extend(values_to_decode)
        else:
            encoded_values.append(value_to_decode)
    elif command == "v":
        encode_to_compare = input("Give encoding to compare:\n")
        decode_to_compare = input("Give decoding to compare:\n")
        print(validate_values(encode_to_compare, decode_to_compare, decode_function))
        sys.exit()
    else:
        sys.exit()
    # vraag een tweede keer voor input om het bijvoorbeeld uit te printen
    command = input().lower()
    if command == "p":
        # print alles uit als er values zijn om te printen
        # zet ze netjes onder elkaar bij het uitprinten
        if len(encoded_values) > 0:
            print("\n".join(decode_list(encoded_values, encode_function)))
        if len(decoded_values) > 0:
            print("\n".join(encode_list(decoded_values, decode_function)))
    else:
        sys.exit()


# Create a unittest for both the encode and decode function (see test_namehasher.py file for boilerplate)
if __name__ == "__main__":
    main()
