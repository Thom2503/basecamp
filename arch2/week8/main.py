from urllib.request import urlopen
import matplotlib.pyplot as plt
import numpy as np
import json
import statistics

# haal de data op en stop die met json loads in een
# list met dictionaries
url = "https://api.basecampserver.tech/sensors?node_id=26"
url = urlopen(url).read()

data = json.loads(url)

# lijstjes met alle data om beter de mean, max enz. te krijgen
temps = []
humidities = []
pressures = []
timestamps = []

# stop alle data in de goede list
for _ in data:
    for key, value in _.items():
        if key == "timestamp":
            timestamps.append(value)
        if key == "temperature":
            temps.append(value)
        elif key == "humidity":
            humidities.append(value)
        elif key == "pressure":
            pressures.append(value)
        else:
            continue


def pick_data(data_type: str) -> list:
    """
    Functie om een list te returnen op basis
    van de data_type parameter.

    @param str data_type - data_type list die je wilt hebben

    @return list data - de list die je gekozen hebt
    """
    data = []
    if data_type == "temperature":
        data = temps
    elif data_type == "humidity":
        data = humidities
    elif data_type == "pressure":
        data = pressures
    elif data_type == "timestamp":
        data = timestamps

    return data


def is_prime(n: int) -> bool:
    """
    Functie om te berekenen of het meegegeven
    getal een prime getals is. (dus alleen maar
    te delen door zichzelf)

    @param int n - nummer om te checken

    @return bool - of het een prime getal is
    """
    if n < 2:
        return False

    for i in range(2, n):
        if n % i == 0:
            return False
    else:
        return True


def primes_and_no_primes(data_type: str) -> tuple:
    """
    Functie om een tuple te maken met aantal
    prime getallen en niet prime getallen in
    de lijst.

    @param str data_type - welke lijst gekozen wordt

    @return tuple - lijst met aantal prime en niet prime getallen
    """
    # lijstjes met alle prime en niet prime getallen.
    # de lengte van deze bepaald de hoeveelheid
    primes = []
    non_primes = []
    # loop door alle getallen heen en check of die een
    # prime getal is
    for n in pick_data(data_type):
        if is_prime(int(n)) is True:
            primes.append(n)
        else:
            non_primes.append(n)

    prime = len(primes)
    non_prime = len(non_primes)

    return (prime, non_prime)


def standard_deviation(data_type: str) -> float:
    """
    Functie om de standard deviation te krijgen van
    een lijst.

    @param str data_type - welke lijst gekozen wordt.

    @return float - de standard deviation
    """
    return statistics.stdev(pick_data(data_type))


def mean(data_type: str) -> float:
    """
    Functie om de mean data te krijgen van een lijst
    met data.

    @param str data_type - welke lijst gekozen wordt.

    @return float - de mean van de lijst
    """
    return statistics.mean(pick_data(data_type))


def plot_standard_deviation(data_type: str) -> None:
    """
    Functie om een grafiek te maken met de standard
    deviation. Dit is op basis van de mean en standard
    deviation.

    @param str data_type - welke lijst geplot moet worden

    @return None
    """
    # lijst met data voor om mee te plotten.
    data = pick_data(data_type)
    # de mean en standard deviation om mee te rekenen
    mu, sigma = mean(data_type), standard_deviation(data_type)
    # maak een normal destribution om de standard deviation mee
    # te vergelijken
    s = np.random.normal(mu, sigma, len(data))
    # haal data uit een histogram om te gebruiken in de berekening
    count, bins, ignored = plt.hist(s, len(data), density=True)
    # hele complexe berekening.
    # het is ten minste dezelfde berekening als het berekenen van
    # de kans in een Gaussische verdeling
    plt.plot(bins, 1/(sigma * np.sqrt(2 * np.pi)) *
             np.exp(- (bins - mu)**2 / (2 * sigma**2)),
             linewidth=2, color='r')
    plt.show()


def minimum(data_type: str) -> float:
    """
    Zoek de kleinste waarde in een list.

    @param str data_type - welke lijst gezocht moet worden

    @return float - kleinste waarde
    """
    return min(pick_data(data_type))


def maximum(data_type: str) -> float:
    """
    Zoek de grootste waarde in een list.

    @param str data_type - welke lijst gezocht moet worden

    @return float - de hoogste waarde in de lijst
    """
    return max(pick_data(data_type))


def ask_type(func: callable) -> tuple[float, str]:
    """
    Functie om wat dingen niet veel te herhalen zoals de eerste paar
    statistieken dingen in de main functie, mean, max, min en
    standard deviation.

    @param callable func - functie die je wilt gebruiken

    @return None|Tuple - of een error of een tuple met
                         een functie return en type string
    """
    # de data_types die gezocht kunnen worden hier wordt ook mee gechecked
    data_types = ('temperature', 'humidity', 'pressure', 'timestamp')

    invalid_data_type_err = "Invalid data_type!"
    user_type = input("What type do you want to show?\n").lower()
    if user_type in data_types:
        return (func(user_type), user_type)
    else:
        print(invalid_data_type_err)


def main() -> None:
    """
    Functie voor de main CLI Dashboard waar de gebruiker
    kan zoeken op verschillende data en ook grafieken kan
    zien met die data.
    """
    invalid_command_err = "Invalid command!"
    invalid_type_err = "Invalid data_type!"
    # de data_types die gezocht kunnen worden hier wordt ook mee gechecked
    types = ('temperature', 'humidity', 'pressure', 'timestamp')
    # maak een string om te tonen bij het opstarten van het programma
    types_string = " ".join(types)
    # of je het moet afsluiten
    quit_program = False
    # toon wat informatie aan de gebruiker
    print(f"""Welcome to the weather dashboard!
You can print 'mean', 'maximum', 'minimum', 'standard_deviation', 'graph', or 'heatmap'.
Valid types: {types_string.replace('timestamp', '')}
""")
    while quit_program is not True:
        command = input("> ").lower()
        if command in ('mean'):
            mean_number = ask_type(mean)
            if isinstance(None, type(mean_number)) is not True:
                print(f"The mean of {mean_number[1]} is {mean_number[0]:.1f}")
        elif command in ('maximum', 'max'):
            max_number = ask_type(maximum)
            if isinstance(None, type(mean_number)) is not True:
                print(f"The maximum number of {max_number[1]} is {max_number[0]:.1f}")
        elif command in ('minimum', 'min'):
            min_number = ask_type(minimum)
            if isinstance(None, type(mean_number)) is not True:
                print(f"The minimum number of {min_number[1]} is {min_number[0]:.1f}")
        elif command in ('standard_deviation', 'standard deviation'):
            user_type = input("What type do you want to show?\n").lower()
            if user_type in types:
                print(standard_deviation(user_type))
                plot_standard_deviation(user_type)
            else:
                print(invalid_type_err)
        elif command in ('graph'):
            user_data_type = input("What do you want to plot?\n").lower()
            if user_data_type in types:
                # dit maakt een lijn grafiek met de data over de tijd.
                plt.plot(range(len(pick_data(user_data_type))), pick_data(user_type))
                plt.xlabel("Time")
                plt.ylabel(user_data_type.capitalize())
                plt.show()
            else:
                print(invalid_type_err)
        elif command in ('primes'):
            user_data_type = input("What do you want to plot?\n").lower()
            if user_data_type in types:
                # een pie chart om het procent niet primes en primes te
                # tonen
                labels = ['primes', 'non primes']
                sizes = primes_and_no_primes(user_data_type)
                fig1, ax1 = plt.subplots()
                ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
                        shadow=True, startangle=90)
                ax1.axis('equal')
                plt.show()
            else:
                print(invalid_type_err)
        elif command in ('heatmap'):
            user_data_type = input("What do you want to plot?\n").lower()
            if user_data_type in types:
                data = np.asarray(pick_data(user_data_type))
                # tijd gebruiken voor de y as
                y = np.asarray(range(len(timestamps)))
                heatmap, xedges, yedges = np.histogram2d(y, data, bins=20)
                extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
                plt.imshow(heatmap.T, extent=extent, origin='lower')
                plt.xlabel("Time")
                plt.ylabel(user_data_type.capitalize())
                plt.show()
            else:
                print(invalid_type_err)
        elif command in ('exit', 'e', 'quit', 'q'):
            quit_program = True
        else:
            print(invalid_command_err)


if __name__ == "__main__":
    main()
