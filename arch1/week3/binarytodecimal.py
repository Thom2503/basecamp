def bin_to_dec_int(bin):
    """
    Functie om een binary nummer naar een decimaal over te zetten. 1111 -> 15
    (built-in functie)

    @param string bin - binary nummer

    @return int - decimaal nummer
    """
    return int(bin, 2)


def bin_to_dec_w(bin):
    """
    Functie om een binary nummer naar een decimaal over te zetten. 1111 -> 15
    (while loop)

    @param string bin - binary nummer

    @return int dec - decimaal nummer
    """
    dec = 0

    num = 0
    while num < len(bin):
        dec += int(bin[num]) * 2 ** abs ((num - (len(bin) - 1)))
        num += 1

    return dec


def bin_to_dec_f(bin):
    """
    Functie om een binary nummer naar een decimaal over te zetten. 1111 -> 15
    (for loop)

    @param string bin - binary nummer

    @return int dec - decimaal nummer
    """
    dec = 0
    
    for i in range(len(bin)):
        dec += int(bin[i]) * 2 ** abs ((i - (len(bin) - 1)))

    return dec

binary_input = input("Binary number:\n")

print(bin_to_dec_int(binary_input))
print(bin_to_dec_w(binary_input))
print(bin_to_dec_f(binary_input))

