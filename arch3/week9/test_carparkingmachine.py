from carparking import CarParkingMachine, DateTimeHelper
from datetime import datetime, timedelta
from unittest.mock import MagicMock


# Test for a normal check-in with correct result (True)
def test_check_in_capacity_normal():
    parking_machine = CarParkingMachine()
    new_car = parking_machine.check_in("12-AA-BB", datetime.now())
    assert new_car is not False, "The car park is full!"


# Test for a check-in with maximum capacity reached (False)
def test_check_in_capacity_reached():
    # parking_machine = CarParkingMachine()
    # parking_machine.current_capacity = 10
    # new_car = parking_machine.check_in("12-AA-BB", datetime.now())
    # assert new_car is False, "The car park should be full!"

    carpackingmachine = CarParkingMachine(capacity=2)
    carpackingmachine.check_in(license_plate='XXX')
    carpackingmachine.check_in(license_plate='YYY')

    assert False == carpackingmachine.check_in(license_plate='ZZZ')


# Test for checking the correct parking fees
def test_parking_fee(monkeypatch):
    # Assert that parking time 2h10m, gives correct parking fee
    # Assert that parking time 24h, gives correct parking fee
    # Assert that parking time 30h == 24h max, gives correct parking fee
    parking_machine = CarParkingMachine()
    # maak alle data om mee te checken
    datetime_now = datetime.now()
    datetime_2hours = datetime_now + timedelta(hours=2, minutes=10)
    datetime_24hours = datetime_now + timedelta(hours=24)
    datetime_30hours = datetime_now + timedelta(hours=30)

    # check alle autos in op dezelfde tijd
    parking_machine.check_in("12-AA-BB", datetime_now)
    parking_machine.check_in("34-CC-DD", datetime_now)
    parking_machine.check_in("56-EE-FF", datetime_now)

    # gebruik magicmock om de tijd te veranderen van de get_datetime_now
    # method die in CarParkingMachine wordt gebruikt om de huidige datum
    # te krijgen
    DateTimeHelper.get_now = MagicMock(return_value=datetime_2hours)
    hour2_fee = parking_machine.get_parking_fee("12-AA-BB")

    DateTimeHelper.get_now = MagicMock(return_value=datetime_24hours)
    hour24_fee = parking_machine.get_parking_fee("34-CC-DD")

    DateTimeHelper.get_now = MagicMock(return_value=datetime_30hours)
    hour30_fee = parking_machine.get_parking_fee("56-EE-FF")

    # check alle waardes of die kloppen
    assert hour2_fee == 7.5, f"2 hour 10 min ({hour2_fee}) does not equal 7.5"
    assert hour24_fee == 60, f"24 hours ({hour2_fee}) does not equal 60"
    assert hour30_fee == hour24_fee, f"30 and 24 hours ({hour2_fee}) should be equal"


# Test for validating check-out behaviour
def test_check_out():
    # Assert that {license_plate} is in parked_cars
    # Assert that correct parking fee is provided when checking-out {license_plate}
    # Aseert that {license_plate} is no longer in parked_cars
    parking_machine = CarParkingMachine()
    parking_machine.check_in("12-AA-BB", datetime.now())

    assert parking_machine.check_out("12-AA-BB") != 0, "Car not found"

    assert parking_machine.check_out("12-AA-BB") == 0, "Car is found"

    parking_machine.check_in("12-AA-BB", datetime.now())
    assert parking_machine.check_out("12-AA-BB") == 60.0, "Car parking fee isn't correct"
