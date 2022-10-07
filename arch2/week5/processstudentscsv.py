"""
A dataset is given with information of students: student number, first name,
last name, date of birth, study program.
You are asked to implement a program that given this dataset (as a csv file),
the program processes the information. The requested criteria are:
Sometimes data values are corrupted. The program must report corupted values.
Any invalid or empty value is defined as corrupted.

- Student number has this format: 7 digits, starting with 0 and second digit
  (from left) can be either 9 or 8. Example: 0212345 is not valid
- First name and last names, contains only alphabet.
- Date of birth has this format: YYYY-MM-DD. Days between 1 and 31,
  months between 1 and 12 and Years between 1960 and 2004.
- Study program can have one of these values: INF, TINF, CMD, AI.

A template Python file is provided with a function that loads the data set.

The program should make two separate lists: list of rows with correct values
and a list of rows with corrupted values.
These two lists will be printed with this format:
"""
import os
import sys
import string

valid_lines = []
corrupt_lines = []

'''
The validate_data function will check the students.csv line by line for corrupt data.

- Valid lines should be added to the valid_lines list.
- Invalid lines should be added to the corrupt_lines list.

Example input: 0896801,Kari,Wilmore,1970-06-18,INF
This data is valid and the line should be added to the valid_lines list unchanged.

Example input: 0773226,Junette,Gur_ry,1995-12-05,
This data is invalid and the line should be added to the corrupt_lines list in the following
format:

0773226,Junette,Gur_ry,1995-12-05, => INVALID DATA: ['0773226', 'Gur_ry', '']

In the above example the studentnumber does not start with '08' or '09',
the last name contains a special character and the student program is empty.

Don't forget to put the students.csv file in the same location as this file!
'''


def is_valid_program(program):
    """
    Functie om te checken of de student in het goede programma zit.
    Dit moet zijn: [INF, TINF, CMD, AI]

    @param string program - het programma

    @return bool - of het een juist programma is
    """
    # de geaccepteerde programmas waar op gecheckt moet worden
    programs = ['INF', 'TINF', 'CMD', 'AI']
    # return True als het het programma in programs zit anders return False
    return program.upper() in programs


def is_valid_date(date):
    """
    Functie om te checken of de data klopt op basis van format, of de dagen/jaren/maanden kloppen

    @param string date - datum om te checken

    @return bool - of het een correcte datum is
    """
    # check of de lengte correct is
    if len(date) != 10:
        return False

    # check of er '-' in zit en niet '/' of '_' om later een array van te maken
    if "-" not in date:
        return False

    # split het in een lijstje met [jaar, maand, dag]
    date_parts = date.split("-")
    year = date_parts[0]
    month = int(date_parts[1])
    day = int(date_parts[2])

    # check of het jaar een 4 cijfer getal is zoals het format
    if len(year) != 4:
        return False
    # als het jaar niet tussen 1960 en 2004 is klopt het niet
    if int(year) < 1960 or int(year) > 2004:
        return False
    # check of de maand niet meer is dan 12 en niet 0 is
    # want het kan ook dat er een datum is ingevuld
    if month > 12 and month != 0:
        return False
    # check of de dag niet meer is dan 31 en niet 0 is,
    # het kan ook zijn dat er jaar is ingevuld
    if day > 31 and day != 0:
        return False

    return True


def is_valid_string(name):
    """
    Check of de string die je geeft geen gekke tekens heeft maar alleen alfabet letters

    @param string name - String om te checken

    @return bool - of er geen gekke tekens in zitten
    """
    # alle geaccepteerde karakters uit de ascii table waar gecheckt op word
    all_lower = string.ascii_lowercase
    # loop door de string heen, als er een karakter in niet all_lower komt
    # moet je false returnen want dan is het niet alleen letters
    for char in name.lower():
        if char not in all_lower:
            return False

    return True


def check_student_id(s_id):
    """
    Functie om een student nummer te checken op lengte maar ook dat het start met 0
    en dat daarna een 9 of 8 komt.

    @param string s_id - student nummer om te checken

    @return bool - of het een valid student id is
    """
    # de student_id mag niet minder zijn dan 7 characters
    if len(s_id) < 7:
        return False
    # de student_id moet starten met 0
    if s_id[0] != "0":
        return False
    # het tweede cijfer moet of een 8 of 9 zijn
    if s_id[1] not in ('8', '9'):
        return False

    return True


def validate_data(line):
    """
    Functie om de data te valideren die per lijn binnen komt uit een csv.
    Dit moet op paar criteria gecheckt worden, als de lijn aan die eisen
    voldoet moet je het aan valid_lines toevoegen anders moet het aan
    corrupt_data toegevoegd worden.

    @param string line - de lijn in de csv file
    """
    # de delen van de line die fout zijn dit moet dan getoont kunnen worden
    invalid_line_elements = []
    # om bij te houden of de line valid is
    is_valid = True
    # split de lijn zodat je de verschillende delen hebt om te kunnen checken
    record_parts = line.split(",")
    # alle records uit de lijn in eigen variables voor meer duidelijkheid
    student_id = record_parts[0]
    student_name = record_parts[1]
    student_family_name = record_parts[2]
    student_date = record_parts[3]
    student_program = record_parts[4]
    # check hier of alle data klopt, de data mag niet leeg zijn anders is
    # het corrupt, maar het moet ook nog kloppen en dat checken de verschillende
    # functies.
    if student_id == '' or check_student_id(student_id) is not True:
        invalid_line_elements.append(student_id)
        is_valid = False
    if student_name == '' or is_valid_string(student_name) is not True:
        invalid_line_elements.append(student_name)
        is_valid = False
    if student_family_name == '' or is_valid_string(student_family_name) is not True:
        invalid_line_elements.append(student_family_name)
        is_valid = False
    if student_date == '' or is_valid_date(student_date) is not True:
        invalid_line_elements.append(student_date)
        is_valid = False
    if student_program == '' or is_valid_program(student_program) is not True:
        invalid_line_elements.append(student_program)
        is_valid = False
    # als er geen fouten zijn gevonden bij de lijn kan die toegevoegd worden aan
    # de valid_lines list
    if is_valid:
        valid_lines.append(line)
    # als er corrupte onderdelen zijn moet je dat bij corrupt_lines toevoegen
    # en dit moet met de lijn en de data die corrupt is in een lijstje
    if len(invalid_line_elements) > 0:
        invalid_text = f"{line} => INVALID DATA: {invalid_line_elements}"
        corrupt_lines.append(invalid_text)


def main(csv_file):
    with open(os.path.join(sys.path[0], csv_file), newline='') as csv_file:
        # skip header line
        next(csv_file)

        for line in csv_file:
            validate_data(line.strip())

    print('### VALID LINES ###')
    print("\n".join(valid_lines))
    print('### CORRUPT LINES ###')
    print("\n".join(corrupt_lines))


if __name__ == "__main__":
    main('students.csv')
