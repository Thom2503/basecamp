from urllib.request import urlopen
import json

url = "https://api.basecampserver.tech/sensors?node_id=26"
url = urlopen(url).read()

data = json.loads(url)
for _ in data:
    for key, value in _.items():
        print(key, value)
