import os
import sys

temperatures = {}

month_names = (
    'January',
    'Febuary',
    'March',
    'April',
    'May',
    'June',
    'July',
    'August',
    'September',
    'October',
    'November',
    'December'
)


def load_txt_file(file_name):
    """
    Functie om een text file in te laden en die te lezen

    @param string file_name - bestand naam

    @return string file_content - content van het bestand
    """
    file_content = []

    with open(os.path.join(sys.path[0], file_name), newline='', encoding="utf8") as file_obj:
        for line in file_obj.readlines():
            file_content.append(line.split())

    return file_content


def fahrenheit_to_celcius(fahrenheit: float) -> float:
    """
    Functie om fahrenheit naar celcius te kunnen berekenen
    dit kan bijvoorbeel met map gebruikt worden over een lijst.
    Resultaat wordt op 1 decimaal afgerond

    @param float fahrenheit - temperatuur om naar celcius
                              te berekenen
    """
    return (fahrenheit - 32) / 1.8


def average_temp_per_year(temperatures: dict) -> list:

    year_avgs = []

    for year in temperatures:
        this_year = temperatures[year]
        avg_months = average_temp_per_month(this_year)
        avg_this_year = average(avg_months)
        year_avgs.append((year, avg_this_year))

    return year_avgs


def average_temp_per_month(temperatures: dict) -> list:

    month_avg = []
    for month in temperatures:
        temp_lst = temperatures[month]
        avg_this_month = average(temp_lst)
        month_avg.append(avg_this_month)

    return month_avg


def average(data_points):
    if (num_points := len(data_points)) == 0:
        raise ValueError("average requires at least one data point")
    return round(sum(data_points) / num_points, 4)


def parse_temp_data(file_name: str) -> dict:
    """
    Functie om de data te parsen en dit in een mooie dict
    te stoppen dit moet als een dict er uit komen.
    vb: {year: {month: [temp, temp, temp, ...]}, ...}

    @param string file_name - file met data waar load_txt_file
                              op wordt aangeroepen

    @return dict data - de mooi formatted data
    """
    data = {}
    previous_month = 0  # om bij te houden of het een nieuwe maand is
    # alle temperaturen van 1 maand om in een dict te kunnen appenden
    month_temps = []
    month_dict = {}
    # geeft een lijst met 4 kolommen maand, dag, jaar, temperatuur
    file_contents = load_txt_file(file_name)
    for content in file_contents:
        # de nodige data
        month = int(content[0])
        year = int(content[2])
        temp = float(content[3])
        # checken of de maand nog hetzelfde is anders moet je een
        # nieuwe maand starten om te appenden aan data
        if previous_month == month:
            month_temps.append(temp)
        else:
            # nieuwe maand reset eerst alles en append
            # dan de eerste dag nog
            month_temps = []
            month_dict = {}
            month_temps.append(temp)
        # array om te appenden aan een jaar.
        month_dict.update({month: month_temps})
        # voor appenden als de key al bestaat
        # kan je update gebruiken anders moet je
        # die eerst maken
        if year in data:
            data[year].update(month_dict)
        else:
            data[year] = month_dict

        previous_month = int(month)

    return data


def list_all_avg_in_c(data: dict) -> list:
    """
    Functie om een lijst met tuples te genereren de eerste element
    moet het jaar zijn en de tweede een dictionary met als key de
    maand naam en als value de gemiddelde temperatuur in celcius

    @param dict data - de input data

    @return list list_avgs - de lijst zoals aangegeven
    """
    # de lijst die returned gaat worden met de tuples en dictionary er in
    list_avgs = []
    # om de dictionary van de maanden te maken
    month_dict = {}
    # haal alle jaren om daar door heen te loopen
    years = average_temp_per_year(data)

    for year in years:
        # haal de lijst van de maand gemiddelde van het jaar om
        # daar ceclius van de maken en dan in de dictionary te
        # stoppen
        month_avg = average_temp_per_month(data[year[0]])
        month_avg_c = list(map(fahrenheit_to_celcius, month_avg))
        # loop door de maanden om dan een dictionary te maken
        # met {maand: temperatuur}
        for idx_month, month_temp in enumerate(month_avg_c):
            month_dict.update({month_names[idx_month]: month_temp})
        # voeg het allemaal van dat jaar toe aan de uiteindelijke lijst
        list_avgs.append((year[0], month_dict))
        # reset de dictionary voor het volgende jaar
        month_dict = {}

    return list_avgs


def main() -> None:
    data = parse_temp_data('NLAMSTDM.txt')
    print("""[1] Print the average temperatures per year (fahrenheit)
[2] Print the average temperatures per year (celsius) Hint: Use built-in map() function.
[3] Print the warmest and coldest year as tuple based on the average temperature
[4] Print the warmest month of a year based on the input year of the user (full month name)
[5] Print the coldest month of a year based on the input year of the user (full month name)
[6] Print a list of tuples where the first element of each tuple is the year and
    the second element of the tuple is a dictionary with months as the keys and
    the average temprature (in Celsius) of each month as the value""")
    quit_program = False
    while quit_program is False:
        command = int(input("> "))
        if command > 6:
            quit_program = True
        if command == 1:
            print(average_temp_per_year(data))
        if command == 2:
            years_avg = average_temp_per_year(data)
            avg_in_c = list(map(fahrenheit_to_celcius, list(zip(*years_avg))[1]))
            print(list(map(lambda x, y: (y, x), avg_in_c, list(zip(*years_avg))[0])))
        if command == 3:
            years_avg = average_temp_per_year(data)
            warmest_year = max(years_avg, key=lambda item: item[1])
            coldest_year = min(years_avg, key=lambda item: item[1])

            print((warmest_year[0], coldest_year[0]))
        if command == 4:
            year = int(input("Input a year:\n"))
            month_avg = average_temp_per_month(data[year])
            idx_max_avg = month_avg.index(max(month_avg))
            print(month_names[idx_max_avg])
        if command == 5:
            year = int(input("Input a year:\n"))
            month_avg = average_temp_per_month(data[year])
            idx_min_avg = month_avg.index(min(month_avg))
            print(month_names[idx_min_avg])
        if command == 6:
            print(list_all_avg_in_c(data))



if __name__ == "__main__":
    main()
