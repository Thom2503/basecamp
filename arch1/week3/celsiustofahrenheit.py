def c_to_f_table():
    """
    Functie om een tafel van celcius naar farhenheit te zien.
    (while loop)

    @return string - tafel met F -> C
    """
    table = ""
    # lambda functie om Celcius naar Fahrenheit te berekenen
    convert_to_f = lambda C : C * 1.8 + 32

    # een mooie header voor de tafel
    table += "+-----+-----+\n|  C  |  F  |\n+-----+-----+\n"

    C = 0
    while C < 110:
        # if C % 10 == 0:
        F = int(convert_to_f(C) // 1) # dat het een rond getal is
        # zfill maakt het dat alle getallen 3 getallen minimaal zijn
        # om de tafel mooi te maken
        table += f"| {str(C).zfill(3)} | {str(F).zfill(3)} |\n"
        C += 10

    table += "+-----+-----+" # footer van de tafel
    return table



def c_to_f_table_for():
    """
    Functie om een tafel van celcius naar farhenheit te zien.
    (for loop)

    @return string - tafel met F -> C
    """
    table = ""
    # lambda functie om Celcius naar Fahrenheit te berekenen
    convert_to_f = lambda C : C * 1.8 + 32

    # een mooie header voor de tafel
    table += "+-----+-----+\n|  C  |  F  |\n+-----+-----+\n"

    for C in range(0, 110): # 110 omdat het tot 100 moet gaan
        # het moet elke 10 graden Celcius zijn
        if C % 10 == 0:
            F = int(convert_to_f(C) // 1) # dat het een rond getal is
            # zfill maakt het dat alle getallen 3 getallen minimaal zijn
            # om de tafel mooi te maken
            table += f"| {str(C).zfill(3)} | {str(F).zfill(3)} |\n"
    
    table += "+-----+-----+" # footer van de tafel
    return table


print(c_to_f_table())
print(c_to_f_table_for())
