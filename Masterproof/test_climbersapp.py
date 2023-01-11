from datetime import datetime
from climber import Climber as Climber
from mountain import Mountain as Mountain
from expedition import Expedition as Expedition


# Test to check if the age of a climber is correct based on the date_of_birth
def test_age_of_climber():
    Thom = Climber(1, "Thom", "Veldhuis", "Netherlands", datetime(2003, 3, 25))
    assert Thom.get_age() == 19, "Leeftijd van iemand geboren op 25 maart 2003"


# Test to check if the amount of expeditions for a specific climber is returned correctly
def test_amount_of_expeditions_of_climber():
    # test data
    # 137|Josiah|Battson|Guatemala|1949-12-02 00:00:00
    Josiah = Climber(137, "Josiah", "Battson", "Guatemala", datetime(1949, 12, 25))
    josiah_expeditions = Josiah.get_expeditions()
    assert josiah_expeditions[0].id == 7


# Test to check the difference in height and prommence of a mountain
def test_height_difference_mountain():
    Putha = Mountain(73, "Putha Hiunchuli", "Nepal", 94, 7246, 1151, "Dhaulagiri Himalaya")
    assert Putha.height_difference() == 6095


# Test to check if the amount of expeditions for a specific mountain is returned correctly
def test_amount_of_expeditions_of_mountain():
    # test data
    # 73|Putha Hiunchuli|Nepal|94|7246|1151|Dhaulagiri Himalaya
    Putha = Mountain(73, "Putha Hiunchuli", "Nepal", 94, 7246, 1151, "Dhaulagiri Himalaya")
    putha_expeditions = Putha.get_expeditions()
    assert len(putha_expeditions) == 1


# Test to check if the returned date matches the specified format for that expedition date
def test_expedition_date_conversion():
    # test data
    # 1|The journey of Momhil Sar|65|Pakistan|1965-08-18 00:00:00|Indonesia|1308|1
    Momhil = Expedition(1, "The Journey to Momhil Sar", 65, "Pakistan", datetime(1965, 8, 18), "Indonesia", 1308, True)
    assert Momhil.convert_date("%Y-%m-%d") == "1965-08-18"


# Test to check if the duration is converted from 1H19 to the specified format
def test_expedition_duration_conversion():
    Momhil = Expedition(1, "The Journey to Momhil Sar", 65, "Pakistan", datetime(1965, 8, 18), "Indonesia", 1308, True)
    assert Momhil.convert_duration("%H:%M") == "21:48", "1308 minuten is 21 uur and 48 minuten"


# Test to check the amount of climbers on a specified expedition
def test_amount_of_climbers_on_expedition():
    Momhil = Expedition(1, "The Journey to Momhil Sar", 65, "Pakistan", datetime(1965, 8, 18), "Indonesia", 1308, True)
    assert len(Momhil.get_climbers()) == 13, "De eerste expedition moet 13 climbers hebben"


# Test to validate if the given mountain of a specified expedition is correct
def test_mountain_on_expedition():
    pass
