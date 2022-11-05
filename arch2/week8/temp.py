from sense_hat import SenseHat
import time
import random
import requests

"""
  Sense HAT Sensors Display
  Select Temperature, Pressure, or Humidity  with the Joystick
  to visualize the current sensor values on the LED.
  Note: Requires sense_hat 2.2.0 or later
"""

KEY = "K3_PB1rRLsF9BdqL98dMQQ"  # TOP SNEAKY SNEAKY

items = []

# de plekken waar de pixels geplaats moeten worden
# op de 8x8 matrix
numberPattern = [
    [2, 9, 11, 17, 19, 25, 27, 33, 35, 42],   # 0
    [2, 9, 10, 18, 26, 34, 41, 42, 43],       # 1
    [2, 9, 11, 19, 26, 33, 41, 42, 43],       # 2
    [1, 2, 11, 18, 27, 35, 41, 42],           # 3
    [3, 10, 11, 17, 19, 25, 26, 27, 35, 43],  # 4
    [1, 2, 3, 9, 17, 18, 27, 35, 41, 42],     # 5
    [2, 3, 9, 17, 18, 25, 27, 33, 35, 42],    # 6
    [1, 2, 3, 9, 11, 19, 26, 34, 42],         # 7
    [2, 9, 11, 18, 25, 27, 33, 35, 42],       # 8
    [2, 9, 11, 17, 19, 26, 27, 35, 43]        # 9
]

sense = SenseHat()
# de kleuren die getoont worden op de sense hat
green = (135, 233, 17)
red = (225, 24, 69)
blue = (0, 87, 233)
white = (255, 255, 255)

# de verschillende data punten
sensors = ["temp", "pressure", "humidity"]


def upload_data(data: dict) -> None:
    """
    Functie om de data te uploaden naar de server. Dit geeft een systemexit
    error als het fout gaat.

    @param dict data - de data die als json wordt verstuurd
    """
    url = f"https://api.basecampserver.tech/sensors?key={KEY}"

    try:
        resp = requests.post(url, json=data)
        resp.raise_for_status()
        print(f"uploaded data at: {data['timestamp']}")
    except requests.exceptions.HTTPError as err:
        print(SystemExit(err))


def display_two_digits(f_number: float, colour: str) -> None:
    """
    Functie om een getal van 2 getallen te maken en die te tonen
    dit kan een negatief getal zijn.

    @param float f_number - het getal om te tonen
    @param str   colour    - de kleur om te gebruiken
    """
    # check of het nummer een negatief nummer is
    # zodat in de hoek onder een - kan komen
    if f_number < 0:
        negative = True
        f_number = abs(f_number)
    else:
        negative = False
    # maak alle nummers een int die onder de tien is
    first_digit = int(int(f_number / 10) % 10)
    second_digit = int(f_number % 10)

    # maak de achtergrond
    pixels = [white for i in range(64)]
    # zoek het eerste getal in de lijst van combinaties
    # en maak die dan in een lijstje die in pixels veranderd wordt
    digit_glyph = numberPattern[first_digit]
    for i in range(0, len(digit_glyph)):
        pixels[digit_glyph[i]] = colour
    # zelfde als bij het eerste getal maar dan met de tweede en paar
    # plekjes opgeschoven
    digit_glyph = numberPattern[second_digit]
    for i in range(0, len(digit_glyph)):
        pixels[digit_glyph[i]+4] = colour

    # als het een negatief nummer is plaats de drie pixels voor de -
    if negative:
        pixels[56] = colour
        pixels[57] = colour
        pixels[58] = colour

    # als het meer dan 2 nummers zijn zet de laatste pixel dan naar de
    # kleur om dat aan te geven.
    if f_number > 99:
        pixels[63] = colour

    # toon het resultaat
    sense.set_pixels(pixels)


def update_screen(mode: str) -> None:
    """
    Functie om data te tonen op het schermpje en de items lijst te updaten
    met nieuwe data. Data is temperatuur, luchtdruk en luchtvochtigheid.

    @param str mode - wat je op het beeld moet zien
    """
    # haal alle nodige data uit de sensor.
    temp = sense.temp
    pressure = sense.pressure
    humidity = sense.humidity
    # om het getal te tonen van of temperatuur, luchtdruk en luchtvochtigheid
    if mode == "temp":
        display_two_digits(temp, red)
    elif mode == "pressure":
        display_two_digits(pressure, green)
    elif mode == "humidity":
        display_two_digits(humidity, blue)

    # maak een dictionary van de data om die te uploaden als json
    data = {
        "timestamp": round(time.time()),
        "temperature": temp,
        "humidity": humidity,
        "pressure": pressure
    }

    # voeg aan de lijst toe die naar de server wordt geupload
    items.append(data)
    upload_data(data)


while True:
    events = sense.stick.get_events()
    current_mode = sensors[random.randint(0, 2)]
    update_screen(current_mode)
    time.sleep(1.5)
