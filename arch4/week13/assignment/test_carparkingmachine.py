from carparking import CarParkingMachine, DateTimeHelper
from datetime import datetime, timedelta


def test_check_in():
    north = CarParkingMachine(id="North")

    north.check_in("12-AA-BB", datetime.now() - timedelta(hours=2))
    assert "12-AA-BB" in north.parked_cars.keys()


def test_restore_state():
    # create new instance with the same id as earlier, same state
    north = CarParkingMachine(id='North')

    assert "12-AA-BB" in north.parked_cars.keys(), "12 not found in parked_cars"
