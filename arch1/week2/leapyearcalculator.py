year = int(input("Year: \n"))

def is_leap_year(year):
    if year % 100 != 0:
        if year % 400 == 0 or year % 4 == 0: 
            return True

    return False

print("leap year") if is_leap_year(year) == True else print("no leap year")
