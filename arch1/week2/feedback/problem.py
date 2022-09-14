"""
Problem:
    Soms moet je een string omdraaien. Zoals: hallo -> ollah. Lees een woord van de
    gebruiker en draai die om, print dan dat resultaat.
"""

def solution_1(string):
    return string[::-1]

def solution_2(string):
    return "".join(reversed(string))

def solution_3(string):
    str = ""
    for i in string:
        str = i + str
    return str

woord = input("Woord:\n")

print(f"{woord} omgedraaid met 1 is {solution_1(woord)}")
print(f"{woord} omgedraaid met 2 is {solution_2(woord)}")
print(f"{woord} omgedraaid met 3 is {solution_3(woord)}")
