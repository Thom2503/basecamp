from sense_hat import SenseHat
import time
import random

"""
  Sense HAT Sensors Display
  elect Temperature, Pressure, or Humidity  with the Joystick
  to visualize the current sensor values on the LED.
  Note: Requires sense_hat 2.2.0 or later
"""

items = []

sense = SenseHat()

green = (0, 255, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
white = (255, 255, 255)


def update_screen(mode):
    temp = sense.temp
    temp_value = temp / 2.5 + 16

    pressure = sense.pressure
    pressure_value = pressure / 20

    humidity = sense.humidity
    humidity_value = 64 * humidity / 100
    if mode == "temp":
        pixels = [red if i < temp_value else white for i in range(64)]

    elif mode == "pressure":
        pixels = [green if i < pressure_value else white for i in range(64)]

    elif mode == "humidity":
        pixels = [blue if i < humidity_value else white for i in range(64)]

    items.append({"timestamp": time.time(), "temperature": temp, "humidity": humidity, "pressure": pressure})
    sense.set_pixels(pixels)


sensors = ["temp", "pressure", "humidity"]

while True:
    events = sense.stick.get_events()
    current_mode = sensors[random.randint(0, 2)]
    update_screen(current_mode)
    print(items)
    time.sleep(1.5)
