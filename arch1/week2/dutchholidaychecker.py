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

date = input("Date:\n")

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
    return "Is geen feestdag"

month_day = date.replace(" ", "").split(",")
month = month_day[0].split(":")[1] # pak de cijfers in de eerste index van month_day
day   = month_day[1].split(":")[1] # zelfde als maand
print(is_holiday(month, day))

