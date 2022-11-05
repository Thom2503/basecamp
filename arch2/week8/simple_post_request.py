import requests
import time
import random

KEY = "K3_PB1rRLsF9BdqL98dMQQ"  # TOP SNEAKY SNEAKY
NODE_ID = 26


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


def generate_random_data():
    temp_data = {
        'temperature': round(22 + (random.random() * 4 - 2), 10),
        'pressure': round(1013.25 + (random.random() * 10 - 5), 10),
        'humidity': round(40 + (random.random() * 10 - 5), 10),
        'timestamp': round(time.time())
    }

    return temp_data


for _ in range(5):
    # print(generate_random_data())
    upload_data(generate_random_data())
    time.sleep(1.5)

# upload_data(temp_data)
