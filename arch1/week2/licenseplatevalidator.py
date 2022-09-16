license_plate = input("What is your license plate?\n")

def check_license_plate(license):
    """
    Functie om te checken of een kentekenplaat correct is. Op basis van dit 
    patroon: 09-AA-ZZ.

    @param string license - kenteken plaat

    @return bool - of het een correct kentekenplaat is
    """
    is_correct = False
    
    if len(license) != 8:
        return is_correct

    sections = license.split("-")

    # check of de eerste 2 cijfers daadwerkelijk cijfers zijn tussen 00 en 99
    if "00" <= sections[0] <= "99":
        is_correct = True

    # loop door de laatste 2 secties heen en check of de letters tussen AA en ZZ vallen
    for section in sections[1:]:
        if "AA" <= section <= "ZZ":
            is_correct = True
        else:
            is_correct = False

    return is_correct

is_valid = "valid" if check_license_plate(license_plate) else "invalid"

print(f"{license_plate} is {is_valid}")
