def calculate_fare(distance):
    """
    Functie om te berekenen hoeveel het kost om te km te reizen met de taxi

    @param int|float distance - hoeveel kilometers

    @param float price - hoeveel het kost
    """
    price = 4.0  # start bij 4 omdat dat de basis price is
    # verander het van km naar meters
    meters = distance * 1000
    # tel 0.25 bij de prijs met een stap van 140 meter
    for meter in range(0, int(meters), 140):
        price += 0.25

    return price


if __name__ == "__main__":
    kilometers = float(input("How many kilometers do you want to travel?\n"))
    print(calculate_fare(kilometers))
