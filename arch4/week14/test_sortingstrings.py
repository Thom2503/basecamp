from sortingstrings import get_num_of_vowels


def test_get_num_of_vowels():
    assert get_num_of_vowels("fly") == 0
    assert get_num_of_vowels("aiueo") == 5
    assert get_num_of_vowels("Thom") == 1
    assert get_num_of_vowels("AIUEO") == 5
