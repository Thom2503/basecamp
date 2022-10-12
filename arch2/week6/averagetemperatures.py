# alle data uit de problem om te checken
march_1995 = (
    '1995',
    '3',
    [
        '47.3',
        '40.0',
        '38.3',
        '36.3',
        '37.4',
        '40.3',
        '41.1',
        '40.5',
        '41.6',
        '43.2',
        '46.2',
        '45.8',
        '44.9',
        '39.4',
        '40.5',
        '42.0',
        '46.5',
        '46.2',
        '43.3',
        '41.7',
        '40.7',
        '39.6',
        '44.2',
        '47.8',
        '45.9',
        '47.3',
        '39.8',
        '35.2',
        '38.5',
        '40.5',
        '47.0'
    ]
)
march_2010 = (
    '2010',
    '3',
    [
        '39.2',
        '36.7',
        '35.5',
        '35.2',
        '35.8',
        '33.8',
        '30.7',
        '33.2',
        '32.3',
        '33.3',
        '37.3',
        '39.9',
        '40.8',
        '42.9',
        '42.7',
        '42.6',
        '44.8',
        '50.3',
        '52.2',
        '55.2',
        '47.2',
        '45.0',
        '48.6',
        '55.0',
        '57.4',
        '50.9',
        '48.6',
        '46.2',
        '49.6',
        '50.1',
        '43.6'
    ]
)
march_2020 = (
    '2020',
    '3',
    [
        '43.2',
        '41.1',
        '40.0',
        '43.6',
        '42.6',
        '44.0',
        '44.0',
        '47.9',
        '46.6',
        '50.5',
        '51.5',
        '47.7',
        '44.7',
        '44.0',
        '48.9',
        '45.3',
        '46.6',
        '49.7',
        '47.2',
        '44.8',
        '41.8',
        '40.9',
        '41.0',
        '42.7',
        '43.4',
        '44.0',
        '46.4',
        '45.5',
        '40.7',
        '39.5',
        '40.6'
    ]
)


def avg(lst):
    """
    Om het gemiddelde uit een lijst te krijgen

    @param list lst - lijstje om gemiddelde van te vinden

    @return float - gemiddelde
    """
    # zet alle items om naar floats zodat je er mee
    # kan rekenen
    lst = [float(temp) for temp in lst]
    return sum(lst) / len(lst)


def find_highest_avg_year():
    """
    Vind het jaar met het hoogste gemiddelde van alle
    jaren

    @return string - jaar met hoogste gemiddelde
    """
    # haal alle lijstjes op om het gemiddelde van te krijgen
    global temps_1995, temps_2010, temps_2020
    # alle gemiddelde van elk jaar om het max van te krijgen
    avg_1995 = avg(temps_1995)
    avg_2010 = avg(temps_2010)
    avg_2020 = avg(temps_2020)
    # krijg de max van het gemiddeld om mee te checken welke het hoogst is
    max_avg = max(avg_1995, avg_2010, avg_2020)
    # geef het jaar terug als het max klopt met het max van het jaar
    if max_avg == avg_1995:
        return "1995"
    elif max_avg == avg_2010:
        return "2010"
    else:
        return "2020"


def find_highest_max_year():
    """
    Vind het het jaar met de grootste max van temperaturen

    @return string - jaar met hoogste temperatuur
    """
    # haal alle lijstjes op om de max van te kunnen krijgen
    global temps_1995, temps_2010, temps_2020
    # krijg de max van alle jaren
    max_1995 = max(temps_1995)
    max_2010 = max(temps_2010)
    max_2020 = max(temps_2020)
    # krijg je max van alle maxes van elk jaar
    max_of_three = max(max_1995, max_2010, max_2020)
    # geef het jaar terug waar het max van alle drie
    # klopt met de max van het jaar
    if max_of_three == max_1995:
        return "1995"
    elif max_of_three == max_2010:
        return "2010"
    else:
        return "2020"


if __name__ == "__main__":
    # krijg je de lijstjes met temperaturen om
    # te gebruiken om gelijken en hoogste enz te vinden
    temps_1995 = march_1995[2]
    temps_2010 = march_2010[2]
    temps_2020 = march_2020[2]
    # zoek met sets de gelijken temperaturen om de hoeveelheid te krijgen
    equal_1995_2010 = list(set(temps_1995).intersection(set(temps_2010)))
    equal_1995_2020 = list(set(temps_1995).intersection(set(temps_2020)))

    # print alle uitkomsten
    print(len(equal_1995_2010))
    print(len(equal_1995_2020))
    print(find_highest_max_year())
    print(find_highest_avg_year())
