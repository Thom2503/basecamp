# de opstelling van de dictionary is:
# <datum (dag maand aan elkaar)> : <feestdag>
holidays = {"11"   : "Nieuwjaarsdag",
            "154"  : "Goede vrijdag",
            "174"  : "Pasen (eerste)",
            "184"  : "Pasen (tweede)",
            "274"  : "Koningsdag",
            "55"   : "Bevrijdingsdag",
            "265"  : "Hemelvaartsdag",
            "56"   : "Pinksteren (eerste)",
            "66"   : "Pinksteren (tweede)",
            "2512" : "Kerstmis (eerste)",
            "2612" : "Kerstmis (tweede)"}

month = input("Month:\n")
day   = input("Day:\n")

def is_holiday(m, d):
    """
    Functie om aan te geven of het een feestdag is.

    @param string m - maand
    @param string d - dag

    @return string - Of de feestdag of een bericht dat het geen feestdag is
    """
    date = d + m # maak er 1 string van
    if date in holidays.keys():
        return holidays[date]
    return "Isn't on a holiday"

print(is_holiday(month, day))

