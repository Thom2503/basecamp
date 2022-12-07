import os
import sys
import sqlite3


def add_student(cur: object, new_data: dict) -> int:
    """
    Voeg een student toe met deze data
    first_name, last_name, city, date_of_birth (DD-MM-YYYY), class (optional)
    en geef de toegevoegde studentnummer terug.

    :param cur: object, de connection cursor
    :param new_data: dict, de nieuwe data om toe te voegen

    :return studentnummer: int, nieuwe student nummer
    """
    studentnummer = 0

    sq_query = "INSERT INTO `students` VALUES (NULL, :first_name, :last_name, :city, :date_of_birth, :class)"

    cur.execute(sq_query, new_data)

    studentnummer = cur.execute("SELECT max(studentnumber) FROM `students`").fetchone()[0]

    return studentnummer


def change_class(cur: object, new_data: dict) -> str:
    """
    verander de class van de meegegeven student nummer. als die niet bestaat geef dan een error.

    :param cur: object, de cursor voor de sql queries
    :param new_data: dict, nieuwe data om te updaten

    :return str, een error of als het goed gaat
    """
    studentnumber = new_data['studentnumber']

    sq_search_student = "SELECT * FROM `students` WHERE `studentnumber` = :studentnumber"

    result = cur.execute(sq_search_student, {'studentnumber': studentnumber}).fetchall()

    if len(result) == 0:
        return f"Could not find student with number: {studentnumber}"

    sq_update_query = "UPDATE `students` SET `class` = :class WHERE `studentnumber` = :studentnumber"

    cur.execute(sq_update_query, new_data)

    return "Student added to class!"


def list_all_students(cur: object) -> str:
    """
    list alle studenten in desc order op basis van de class.

    :param cur: object, cursor voor de sql queries

    :return str, lijst met alle studenten
    """
    sq_all_students = "SELECT * FROM `students` ORDER BY `class` DESC"

    result = cur.execute(sq_all_students).fetchall()

    return "\n".join([str(row) for row in result])


def list_all_students_class(cur: object, klas: str) -> str:
    """
    list alle studenten in desc order op basis van de class.

    :param cur: object, cursor voor de sql queries

    :return result_text: str, lijst met alle studenten
    """
    sq_all_students = "SELECT * FROM `students` WHERE `class` = :klas ORDER BY `studentnumber` ASC"

    result = cur.execute(sq_all_students, {'klas': klas}).fetchall()

    return "\n".join([str(row) for row in result])


def return_student_data(cur: object, student: str) -> str:
    """
    return de data van de student

    :param cur: object, cursor voor sql queries
    :param student: str, student die je wilt zoeken

    :return str, data van de student
    """
    sq_student_data = "SELECT * FROM `students` WHERE `first_name` = :first OR `city` = :city OR `last_name` = :last"

    result = cur.execute(sq_student_data, {'first': student, 'city': student, 'last': student})

    return "\n".join([str(row) for row in result])


def main():
    con = sqlite3.connect(os.path.join(sys.path[0], 'studentdatabase.db'))
    cur = con.cursor()
    cur.execute(
        '''CREATE TABLE IF NOT EXISTS students (
            studentnumber INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            city TEXT NOT NULL,
            date_of_birth DATE NOT NULL,
            class TEXT DEFAULT NULL
        );'''
    )

    print("""[A] Add new student
[C] Assign student to class
[D] List all students
[L] List all students in class
[S] Search student
[Q] Quit""")

    quit_program = False

    while quit_program is False:
        command = input("> ").lower()
        if command == "q":
            quit_program = True
        elif command == "a":
            new_data = {'first_name': '', 'last_name': '', 'city': '', 'date_of_birth': '', 'class': None}

            for data in new_data.keys():
                new_input = input(f"{data} > ")
                if new_input == "" and data == "class":
                    new_input = None

                new_data[data] = new_input

            print(add_student(cur, new_data))
            con.commit()
        elif command == "c":
            new_data = {'studentnumber': '', 'class': ''}

            for data in new_data.keys():
                new_input = input(f"{data} > ")
                new_data[data] = new_input

            print(change_class(cur, new_data))
            con.commit()
        elif command == "d":
            print(list_all_students(cur))
        elif command == "l":
            user_class = input("class > ")
            if user_class != "":
                print(list_all_students_class(cur, user_class))
        elif command == "s":
            user_student_id = input("student > ")
            print(return_student_data(cur, user_student_id))

    con.close()


if __name__ == "__main__":
    main()
