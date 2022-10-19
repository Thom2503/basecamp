'''
DESCRIPTION FOR GTIHUB:

Create a progam that can convert a name/string to the hashed representation of that value

The program that needs to be programmed for this assignment is described below.

create a function that given the input string converts it to the encoded/decoded equivalent based on the provided or already set key/hashmap
make sure to only convert values that are in the key/hashmap, if the value is not present, use its own value
- encode_string(data: str, key: str = None) -> str:
- decode_string(data: str, key: str = None) -> str:

create a function that given a list of inputs converts the complete list to the encoded/decoded equivalent based on the key/hashmap
you can use the already created encode/decode function when looping through the list
tip! make use of the map function within python with a lambda to call the internal function with all elements [element, key]
as a return value, you should return a list with the converted values
- encode_list(data: list, key: str = None) -> list:
- decode_list(data: list, key: str = None) -> list:

create a function that given a encoded value, decoded value and a key/hashmap (optional) checks if the values are correct
the return value should be a boolean value (True if values match, False if they don't match)
- validate_values(encoded: str, decoded: str, key: str = None) -> bool:

create a function that given a key, converts to a key_hashmap (Dict) to be used for converting
* each oneven character is the Key of the Dict, each even character is the coresponding Value
* you should validate if the given input is an even input, otherwise show the error: Invalid hashvalue input
* example: a@b.c>d#eA will become: {'a': '@', 'b': '.', 'c': '>', 'd', '#', 'e': 'A'}
- set_hashmap(conversion_string: str) -> None:

Main program [main():]
- Ask for key to use for convertion (make sure to validate against even string length)
- Build menu structure as following (the input can be case-insensitive (so E and e are valid inputs))
[E] Encode value to hashed value
[D] Decode hashed value to normal value
[P] Print all encoded/decoded values
[V] Validate 2 values against eachother
[Q] Quit program

* For ease of use, you can use the following string as a default key to use within your program:
a_b?c9d6e1f4g!h:i<j|k{l0m@n7o+p~q2r+s/t=u^v3w]x(y-z>A*B8C;D%E#F}G5H)I[J$

To test your functions, use the provided unit test file (for boilerplate) and complete the test functions with your own code.
'''

import sys

hashmap_key_value = {}
encoded_values = []
decoded_values = []


def search_letter(code: str) -> str:
    """
    Vind de key van met de code als value

    @param string code - de value waar de key van gevonden moet worden

    @return string - de key in de dictionary
    """
    for key in hashmap_key_value:
        if hashmap_key_value[key] == code:
            return key


# create a function that given the input string converts it to the encoded equivalent based on the provided or already set key/hashmap
# make sure to only convert values that are in the key/hashmap, if the value is not present, use its own value
def encode_string(data: str, key: str = None) -> str:
    # de uiteindelijk geencode string
    encoded = ""
    # loop door de string heen om de characters in
    # de hash map over te zetten om het te encrypten
    # in het voorbeeld heeft elke letter een speciaal teken
    for char in data:
        if char in hashmap_key_value:
            encoded += hashmap_key_value[char]
        else:
            encoded += char

    return encoded


# create a function that given the input string converts it to the decoded equivalent based on the provided or already set key/hashmap
# make sure to only decode values that are in the key/hashmap, if the value is not present, use its own value
def decode_string(data: str, key: str = None) -> str:
    # de uiteindelijk gedecode string
    decoded = ""
    # loop door de string heen en als er een value
    # is gevonden is moet het gedecrypt worden naar
    # de originele waarde
    for char in data:
        if char in hashmap_key_value.values():
            decoded += search_letter(char)
        else:
            decoded += char

    return decoded


# create a function that given a list of inputs converts the complete list to the encoded equivalent based on the key/hashmap
# you can use the already created encode function when looping through the list
# tip! make use of the map function within python with a lambda to call the internal function with all elements
# as a return value, you should return a list with Tuples containing the decoded value as first value and the encode value as second value
def encode_list(data: list, key: str = None) -> list:
    # map over de lijst heen en encode het dan allemaal
    # *lambda kan weg maar moet helaas van codegrade :P*
    return list(map(lambda data_str: encode_string(data_str), data))


# create a function that given a list of inputs converts the complete list to the encoded equivalent based on the key/hashmap
# you can use the already created decode function when looping through the list
# tip! make use of the map function within python with a lambda to call the internal function with all elements
# as a return value, you should return a list with Tuples containing the decoded value as first value and the encode value as second value
def decode_list(data: list, key: str = None) -> list:
    # map over de lijst heen en decode alles
    return list(map(decode_string, data))


# create a function that given a encoded value, decoded value and a key/hashmap (optional) checks if the values are correct
# the return value should be a boolean value (True if values match, False if they don't match)
def validate_values(encoded: str, decoded: str, key: str = None) -> bool:
    # vergelijk of de encoded string hetzelfde is als de
    # decoded string door de encoded string te decoden
    # zo hoef je alleen met 1 iets te doen
    return decode_string(encoded, key) == decoded


# give the option to input a hashvalue to be used/converted to a key/hashmap
# each oneven character is the Key of the Dict, each even character is the coresponding Value
# you should validate if the given input is an even input, otherwise show the error: Invalid hashvalue input
# example: a@b.c>d#eA will become: {'a': '@', 'b': '.', 'c': '>', 'd', '#', 'e': 'A'}
def set_hashmap(key: str) -> None:
    global hashmap_key_value
    # maak met zip 2 lijstjes (dit zijn de even en oneven karakters)
    # die met dict een dictionary worden
    hashmap_key_value = dict(zip(key[::2], key[1::2]))



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
    user_key = input("Input a key to use:\n")
    # check of de key wel even is
    if len(user_key) % 2 != 0:
        print("Invalid hashvalue input")
        sys.exit()
    # als de key even is kan er een hash map van gemaakt worden
    set_hashmap(user_key)
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
        print(validate_values(encode_to_compare, decode_to_compare))
        sys.exit()
    else:
        sys.exit()
    # vraag een tweede keer voor input om het bijvoorbeeld uit te printen
    command = input().lower()
    if command == "p":
        # print alles uit als er values zijn om te printen
        # zet ze netjes onder elkaar bij het uitprinten
        if len(encoded_values) > 0:
            print("\n".join(decode_list(encoded_values)))
        if len(decoded_values) > 0:
            print("\n".join(encode_list(decoded_values)))
    else:
        sys.exit()



# Create a unittest for both the encode and decode function (see test_namehasher.py file for boilerplate)
if __name__ == "__main__":
    main()
