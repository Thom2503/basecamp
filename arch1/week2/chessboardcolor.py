square = input("What square are you on?\n")

def is_square_black(c, r):
    """
    functie om te bepalen of het vakje zwart is. Er is een patroon in
    een schaakboord waar alle even coordinaten zwart zijn en alle oneven wit.

    @param string c - kolom a t/m h
    @param string r - rij 1 t/m 8

    @return bool - of het vakje zwart is
    """
    # maak een nummer van coordinaten
    # interessant trucje om de plaats in het alfabet te vinden op basis van de ascii table
    column = ord(c) - 96
    row = int(r)

    sum_of_coords = column + row
    
    return sum_of_coords % 2 == 0

if len(square) != 2:
    print("The input length must be 2!")
else:
    column, row = square[0], square[1]
    
    is_black = is_square_black(column, row)
    print(f"{square} is black") if is_black else print(f"{square} is white")

