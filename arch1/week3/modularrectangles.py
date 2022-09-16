def create_rectangle(w, h):
    """
    Functie om een rechthoek te maken met nummers 0 t/m 9, op basis van de 
    hoogte en breedte aangegeven door de gebruiker. (while loop)
    
    @param int w - de breedte
    @param int h - de hoogte

    @return string - de rechthoek
    """
    rectangle = ""

    # de huidige breedte en hoogte in de rechthoek
    current_width = 0
    current_height = 0
    i = 0 # om bij te houden in welke loop je bent en de rechthoek mee te vullen
    while True:
        rectangle += str(i % 10)
        current_width += 1
        if current_width == w:
            rectangle += "\n" # nu gaat het een laag naar beneden
            current_height += 1
            current_width = 0 # er moet nu een nieuwe laag beginnen
        # dit is de definitieve stop van de rechthoek
        if current_height >= h:
            break
        i += 1

    return rectangle


def create_rectangle_f(w, h):
    """
    Functie om een rechthoek te maken met nummers 0 t/m 9, op basis van de 
    hoogte en breedte aangegeven door de gebruiker. (for loop)
    
    @param int w - de breedte
    @param int h - de hoogte

    @return string - de rechthoek
    """
    rectangle = ""
    
    k = 0 # variable voor de nummers in de rechthoek

    for i in range(0, h): # loop de width het aantal van h
        for j in range(0, w): # loop het aantal keer in de width
            rectangle += str(k % 10)
            k += 1
        rectangle += "\n"

    return rectangle


width = int(input("What's the width of the rectangle?\n"))
height = int(input("What's the height of the rectangle?\n"))

print(create_rectangle(width, height))
print(create_rectangle_f(width, height))
