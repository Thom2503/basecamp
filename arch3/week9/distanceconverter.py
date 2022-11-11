class Converter:
    """
    a Class to convert all kinds of numbers

    The user will pass a length and a unit
    when declaring an object from the class—for example, c = Converter(9,'inches').
    The possible units are inches, feet, yards, miles,
    kilometers, meters, centimeters, and millimeters.
    """

    def __init__(self, metric, unit):
        self.metric: float | int = metric
        self.unit: str = unit

        # maak de "master" variables aan om makkelijk mee te
        # kunnen rekenen
        self.master_centimeter = self.convert_to_master()

    def convert_to_master(self) -> int | float:
        """
        Functie om het getal wat omgerekend moet worden
        naar 1 "master" getal te converten, en in dit geval
        is dat inches.

        @param object self - dit object

        @return int|float - het "master" getal
        """
        if self.unit == "kilometers":
            return self.metric * 100000
        elif self.unit == "meters":
            return self.metric * 100
        elif self.unit == "millimeters":
            return self.metric * 0.1
        elif self.unit == "miles":
            return self.metric * 160934.4
        elif self.unit == "yards":
            return self.metric * 91.44
        elif self.unit == "feet":
            return self.metric * 30.48
        elif self.unit == "inches":
            return self.metric * 2.54
        else:
            return self.metric

    def inches(self):
        if self.unit == "inches":
            return self.metric
        return self.master_centimeter / 2.54

    def feet(self):
        if self.unit == "feet":
            return self.metric
        return self.master_centimeter / 30.48

    def yards(self):
        if self.unit == "yards":
            return self.metric
        return self.master_centimeter / 91.44

    def miles(self):
        if self.unit == "miles":
            return self.metric
        return self.master_centimeter / 160934.4

    def kilometers(self):
        if self.unit == "kilometers":
            return self.metric
        return self.master_centimeter / 100000

    def meters(self):
        if self.unit == "meters":
            return self.metric
        return self.master_centimeter / 100

    def centimeters(self):
        if self.unit == "centimeters":
            return self.metric
        return self.master_centimeter

    def millimeters(self):
        if self.unit == "millimeters":
            return self.metric
        return self.master_centimeter * 10


def main():
    c = Converter(9, "inches")
    print(c.feet())
    print(c.yards())


if __name__ == "__main__":
    main()
