def create_truth_table_bitwise():
    """
    Functie om een truth table te maken die gebruik maakt van de bitwise operators.

    @return string table - de truth table
    """
    table = ""
    # lijst met de bits die je vergelijkt in een truth table
    binary_list = [[1, 0], [0, 1], [1, 1], [0, 0]]

    table += "---OR----\n"
    # loop voor de bitwise or operator
    for binary in binary_list:
        first_bit, second_bit = binary[0], binary[1]
        truth = first_bit | second_bit
        table += f"{first_bit} | {second_bit} = {truth}\n"

    table += "---AND---\n"
    # loop voor de bitwise and operator
    for binary in binary_list:
        first_bit, second_bit = binary[0], binary[1]
        truth = first_bit & second_bit
        table += f"{first_bit} & {second_bit} = {truth}\n"

    return table


def create_truth_table():
    """
    Functie om een truth table te maken die gebruik maakt van de bitwise operators.
    Geen 0 en 1 maar True en False

    @return string table - de truth table
    """
    table = ""
    # lijst met de True en False die je vergelijkt in een truth table
    bool_list = [[True, False], [False, True], [True, True], [False, False]]

    table += "---OR----\n"
    # loop voor de bitwise or operator
    for bools in bool_list:
        first_bool, second_bool = bools[0], bools[1]
        truth = first_bool | second_bool
        table += f"{first_bool} {second_bool} {truth}\n"

    table += "---AND---\n"
    # loop voor de bitwise and operator
    for bools in bool_list:
        first_bool, second_bool = bools[0], bools[1]
        truth = first_bool & second_bool
        table += f"{first_bool} {second_bool} {truth}\n"

    return table


print(create_truth_table())
