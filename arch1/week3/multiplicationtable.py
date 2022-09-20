def multiplication_table():
    """
    Functie om een vermenigvuldigingstabel te maken met getallen 1 t/m 10.
    (while loop)

    @return table - vermenigvuldigingstafel
    """
    table = ""

    i = 1
    while i < 11:
        j = 1
        table += str(i)
        while j < 11:
            product = i * j
            table += f"{product:2d} "
            j += 1
        table += "\n"
        i += 1

    return table


def multiplication_table_f():
    """
    Functie om een vermenigvuldigingstabel te maken met getallen 1 t/m 10.
    (for loop)

    @return table - vermenigvuldigingstafel
    """
    table = ""
    for i in range(1, 11):
        table += str(i)
        for j in range(1, 11):
            product = i * j
            table += f"{product:2d} "
        table += "\n"

    return table


print(multiplication_table())
print(multiplication_table_f())
