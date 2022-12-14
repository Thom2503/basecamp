from namehasher import *


def test_encode_string():
    # check if given the hashmap string, the correct output is given
    assert "~1=1+" == encode_string("peter", encode_function)
    # check if case insesitive input is handle correctly
    assert "P#T#R" == encode_string("PETER", encode_function)


def test_decode_string():
    # check if given hasmap string, the correct decode output is given
    assert "peteo" == decode_string("~1=1+", decode_function)
    # check if case insesitive input is handle correctly
    assert "PETER" == decode_string("P#T#R", decode_function)


def test_encode_list():
    # check if given a list of values the encoded output is a list of tuples containing (decoded, encoded)
    assert ["P[#T#R", "P*N"] == encode_list(["PIETER", "PAN"], encode_function)


def test_decode_list():
    # check if given a list of values the encoded output is a list of tuples containing (decoded, encoded)
    assert ["PIETER", "PAN"] == decode_list(["P[#T#R", "P*N"], decode_function)


def test_validate_values():
    # check if the given values are equal based on the provided hashmap
    assert True is validate_values("P[#T#R", "PIETER", decode_function)
    # check if the given values are not equal based on case sensitivity and the provided hashmap
    assert False is validate_values("P[#T#R", "Pieter", decode_function)
