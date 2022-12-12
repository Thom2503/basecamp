def get_num_of_vowels(inp: str) -> int:
    letters = [
        'a', 'e', 'i', 'u', 'e', 'o'
    ]
    vowel_count = len(list(filter(lambda x: x.lower() in letters, inp)))
    return vowel_count


def sort_basedon_vowels():
    cases = ['code', 'programming', 'description', 'fly', 'free']
    print(sorted(cases, key=get_num_of_vowels))


if __name__ == "__main__":
    sort_basedon_vowels()
