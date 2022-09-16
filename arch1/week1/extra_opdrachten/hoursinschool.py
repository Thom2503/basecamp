
class Student():
    def __init__(self, name, lessons):
        self.name = name
        self.lessons = lessons
        self.hours = 0
        self.minutes = 0

    def calc_minutes(self):
        self.minutes = self.lessons * 50

    def calc_hours(self):
        self.hours = self.minutes / 60

    def print_hours_minutes(self):
        print(f"hours is {self.hours:.1f} and minutes is {self.minutes:.1f}")

students_amount = int(input("How many students are there?\n"))

for i in range(0, students_amount):
    name = input("Students name:\n")
    lessons = int(input("Amount of lessons:\n"))

    student = Student(name, lessons)
    student.calc_minutes()
    student.calc_hours()
    student.print_hours_minutes()
