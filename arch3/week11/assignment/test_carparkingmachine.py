from carparking import CarParkingMachine, DateTimeHelper


def test_check_in_single_parking_machine_only():
    # create new instances with id
    north = CarParkingMachine(id='North')
    south = CarParkingMachine(id='South')

    assert True is north.check_in(license_plate='MyTestPlate001')
    assert True is ('MyTestPlate001' in north.parked_cars)
    assert True is north.check_in(license_plate='MyTestPlate002')
    assert True is ('MyTestPlate002' in north.parked_cars)
    assert False is south.check_in(license_plate='MyTestPlate001')


def test_restore_state_json():
    # create new instance with the same id as earlier, same state
    north = CarParkingMachine(id='North')
    south = CarParkingMachine(id='South')

    assert True is ('MyTestPlate001' in north.parked_cars)
    assert True is ('MyTestPlate002' in north.parked_cars)

    north.check_out(license_plate='MyTestPlate001')
    assert False is ('MyTestPlate001' in north.parked_cars)
    north.check_out(license_plate='MyTestPlate002')
    assert False is ('MyTestPlate002' in north.parked_cars)

    assert True is south.check_in(license_plate='MyTestPlate002')
