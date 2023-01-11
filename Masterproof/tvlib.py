"""TV Lib a.k.a Thom Veldhuis' Library

This is a library with functions that I use a lot
but aren't necesseraly built in

"""

import os
import json
import csv
import datetime


def is_number(n: str) -> bool:
    """
    Check if n is a number. Can be float, int, precise.

    @param string n - what needs to be checked

    @return bool - if it's a number
    """
    try:
        float(n)   # Type-casting the string to `float`.
    except ValueError:
        return False
    return True


def average(lst: list) -> float:
    """
    Get the average of an array. And format it with "g"

    @param array lst - input array

    @return float avg - the average
    """
    # just to be sure make it a list
    lst = list(lst)
    # check if it's a list
    assert isinstance(lst, list) is True, "list parameter is not a list"
    # check if the first item is a number otherwise it can't
    # go further
    assert is_number(str(lst[0])) is True, "Items in list must be numeric"
    # simple average to get the precise float from
    avg = sum(lst) / len(lst)
    return float(format(avg, 'g'))


def get_key(hash: dict, value: any) -> any:
    """
    Function to get the key of a dictionary with
    the value of param value

    @param dict hash  - the dictionary
    @param any  value - the value to get the key from

    @return any key
    """
    assert isinstance(hash, dict) is True, "Hash is not a dictionary"

    for key in hash:
        if hash[key] == value:
            return key


def to_celsius(fahrenheit: float, decimal: int) -> float:
    """
    Function to convert fahrenheit to celcius and
    round it on param decimal numbers

    @param float fahrenheit - degree to convert
    @param int   decimal    - on what number to round

    @return float - celcius
    """
    assert isinstance(fahrenheit, float), "Fahrenheit must be float"
    assert isinstance(decimal, int), "Decimal must be an int"

    return round((fahrenheit - 32) / 1.8, decimal)


def to_fahrenheit(celcius: float, decimal: int) -> float:
    """
    Function to convert celcius to fahrenheit and
    round is on param decimal numbers

    @param float celcius - degree to convert
    @param int   decimal - number to round on

    @return float - fahrenheit
    """
    assert isinstance(celcius, float), "Fahrenheit must be float"
    assert isinstance(decimal, int), "Decimal must be an int"

    return round((celcius * 1.8) + 32, decimal)


def get_words(file_path: str) -> list:
    """
    Make a list of words in a file.

    :param file_path: str, path to file

    :return words: list, list of words
    """

    assert os.path.exists(file_path) is True, f"Input file ({file_path}) to read from doesn't exists"

    words = []
    with open(file_path) as file:
        for line in file.readlines():
            for word in line.split(" "):
                word = word.replace("\n", "")
                words.append(word)

    return words


def json_to_list(file_path: str) -> list:
    """
    Make a list of dictionaries with the content of a json file

    :param file_path: str, path to the json file

    :return json_items: list, list of dictionaries with the json items
    or
    :return str, error if file given isn't a json file
    """

    assert os.path.exists(file_path) is True, f"Input file ({file_path}) to read from doesn't exists"

    json_items = []

    with open(file_path, "r") as json_file:
        try:
            json_items = json.load(json_file)
        except (TypeError, ValueError):
            return "No valid json"

    return json_items


def list_to_json(file_path: str, lst: list) -> None:
    """
    Simple function to write a list of dictionaries to json

    :param file_path: str, path to file
    :param lst: list, list of dictionaries
    """
    assert isinstance(lst[0], dict) is True, "lst: list items does not contain dictionaries!"
    assert os.path.exists(file_path) is True, f"Input file ({file_path}) to read from doesn't exists"

    json_items = json.dumps(lst, indent=4)

    with open(file_path, "w") as file:
        file.write(json_items)


def csv_to_list(file_path: str) -> list:
    """
    Make a list of dictionaries based on de csv file given

    :param file_path: str, path to the csv file

    :return file_content: list, list of dictionaries from csv
    """

    assert os.path.exists(file_path) is True, f"Input file ({file_path}) to read from doesn't exists"

    file_content = []
    with open(file_path, "r") as file:
        file_content = list(csv.DictReader(file))

    return file_content


def list_to_csv(file_path: str, content: list) -> None:
    """
    Simple way to convert a list of dictionaries to a csv file

    :param file_path: str, path to csv file
    :param content: list, content of the list of dictionaries
    """

    assert isinstance(content[0], dict) is True, "lst: list items does not contain dictionaries!"
    assert os.path.exists(file_path) is True, f"Input file ({file_path}) to read from doesn't exists"

    # headers die csv nodig heeft
    headers = content[0].keys()

    with open(file_path, "w") as out_file:
        writer = csv.DictWriter(out_file, headers)
        writer.writeheader()
        writer.writerows(content)


def time_to_str(time: datetime, format: str = "%d-%m-%Y %H:%M:%S") -> str:
    """
    Verander de datetime naar een leesbare string
    gebaseerd op de meegegeven format
    """
    return time.strftime(format)


def str_to_time(date_str: str, format: str = "%d-%m-%Y %H:%M:%S") -> datetime:
    """
    Maak een datetime object van een gegeven date_str en format.
    """
    return datetime.datetime.strptime(date_str, format)