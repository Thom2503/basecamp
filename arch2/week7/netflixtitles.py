import os
import sys
import csv


def load_csv_file(file_name):
    file_content = []

    with open(os.path.join(sys.path[0], file_name), newline='', encoding="utf8") as csv_file:
        file_content = list(csv.reader(csv_file, delimiter=","))

    return file_content


def get_headers(file_content: list) -> list:
    return file_content[0]


def search_by_type(file_content: list, show_type: str) -> list:

    return list(filter(lambda x: x[1].lower() != show_type, file_content))

def main() -> None:
    titles = load_csv_file('netflix_titles.csv')
    print(len(search_by_type(titles, "movie")))
    print(len(search_by_type(titles, "tv show")))

if __name__ == "__main__":
    main()
