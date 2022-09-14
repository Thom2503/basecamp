def days_in_month(month):
    """
    Functie om terug te geven hoeveel dagen in een maand zitten.

    @param int month - huidige maand

    @return int - aantal dagen
    """
    # als maand in het lijstje van maanden valt dan zitten er 31 dagen
    if month in [1, 3, 5, 7, 8, 10, 12]:
        return 31
    # als de maand februari is is het 28 dagen
    if month == 2:
        return 28
    return 30 # standaard is het 30 dagen


def next_day(current_day):
    """
    Functie om een de volgende datum te kunnen krijgen op basis van de format 
    YYYY-MM-DD. Bijvoorbeeld 2014-12-31 -> 2015-01-01.

    @params string current_day - de dag waar de volgende van berekent kan worden

    @return string next_day - volgende dag van current_day of error message
    """
    next_day = "" # nog te vullen variable voor de volgende dag in YYYY-MM-DD format

    # functie om een mooie error message te maken
    error_msg = lambda err : f"Input format: {err}. Correct format 'YYYY-MM-DD'"
    # check of de lengte correct is
    if len(current_day) != 10:
        return error_msg("Character length must be 10!")

    # check of er '-' in zit en niet '/' of '_' om later een array van te maken
    if "-" not in current_day:
        return error_msg("Missing '-'!")
    
    # split het in een lijstje met [jaar, maand, dag]
    date_parts = current_day.split("-")
    
    # check of het jaar een 4 cijfer getal is zoals het format
    if len(date_parts[0]) != 4:
        return error_msg("Year mus be YYYY!")
    # check of de maand niet meer is dan 12 want het kan ook dat er een datum is ingevuld
    if int(date_parts[1]) > 12:
        return error_msg("Month can't be more than 12!")
    # check of de dag niet meer is dan 31, het kan ook zijn dat er jaar is ingevuld
    if int(date_parts[2]) > 31:
        return error_msg("Day can't be more than 31!")

    year_days = int(date_parts[0]) * 365 # verander het jaar naar het aantal dagen
    month_days = 0 # aantal dagen van alle maanden bij elkaar
    # loop door het aantal maanden heen in de aangegeven datum
    for month in range(1, int(date_parts[1])):
        month_days += days_in_month(month) # voeg het aantal dagen van die maand toe

    # alle dagen bij elkaar opgeteld + 1 extra dag voor de volgende dag
    sum_of_days = year_days + month_days + int(date_parts[2]) + 1

    # aantal jaar in de dagen
    next_year = sum_of_days / 365
    # overgebleven dagen om te kunnen weten of je verder in het jaar bent
    days_left = sum_of_days % 365 

    # als er meer dan 1 dag over is is het geen nieuw jaar anders is het wel een nieuw jaar
    if days_left > 1:
        # als het onder de 31 dagen is kan je ervan uitgaan dat het in de eerste maand is
        if days_left < 31:
            # het kan zijn dat een dag 1 cijfer dan moet er een 0 voor komen
            days_left = days_left if days_left > 10 else "0" + str(days_left)
            next_day = f"{next_year:.0f}-01-{days_left}"
        else:
            month = 0
            # loop door alle maanden en haal de dagen van de overgebleven dagen af
            # en als er niet meer dagen dan in een maand over zijn is het niet meer
            # een volledige maand. Breek dan uit de loop.
            while True:
                month += 1
                days_of_month = days_in_month(month) # aantal dagen in de maand
                if days_left < days_of_month:
                    break
                days_left -= days_of_month
            # zelfde als boven
            days_left = days_left if days_left > 10 else "0" + str(days_left)
            # zelfde als dag moet met maand
            month = month if month > 10 else "0" + str(month)
            # nieuwe datum 
            next_day = f"{int(next_year // 1)}-{month}-{days_left}"

    else:
        next_day = f"{next_year:.0f}-01-01"

    # geef de nieuwe datum terug
    return next_day


current_date = input("What is the current date?\n") 

result = next_day(current_date)
print(result)
