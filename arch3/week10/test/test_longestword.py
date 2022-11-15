from longestword import *


def test_find_longest_word():
    full_path = "/Users/thom2503/Documents/School/basecamp/arch3/week10/randomtext.txt"
    result = find_longest_words(full_path)

    assert result == "solicitude. favourable. discovered. themselves. interested. continuing. everything.", \
           f"Longest words not found in {result}"
