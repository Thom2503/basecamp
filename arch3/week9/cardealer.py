class Vehicle(object):
    """
    Class to define a vehicle by type, brand, amount of wheels, colour,
    and if it's sold.
    """

    def __init__(self, brand, model, color, price):
        self.brand: str = brand
        self.model: str = model
        self.color: str = color
        self.price: float = price
        # niet geinitialiseerbare properties
        self.sold: bool = False
        self.sold_to: str = None

    def sell(self, Customer=None) -> None:
        self.sold = True
        if Customer is not None:
            self.sold_to = Customer

    def print(self) -> str:
        is_sold = "sold" if self.sold is True else "not sold"
        who = "to " + self.sold_to.name if self.sold_to is not None else ""
        sold_text = f"{is_sold} {who}"

        print(f"""The {self.brand} {self.model} in {self.color},
that costs: {self.price} euros. Is {sold_text}""")


class Customer:
    """
    Class to define a customer who can buy a car.
    """

    def __init__(self, name):
        self.name: str = name

    def print(self) -> str:
        print(f"The customer {self.name}")


class Car(Vehicle):
    """
    Child class of Vehicle to define a specific car
    """
    def __init__(self, brand, model, color, price):
        self.is_motorcycle = False
        Vehicle.__init__(self, brand, model, color, price)


class Motorcycle(Vehicle):
    """
    Child class of Vehicle to define a specific Motorcycle
    """
    def __init__(self, brand, model, color, price):
        self.is_motorcycle = True
        Vehicle.__init__(self, brand, model, color, price)


def main():
    Thom = Customer("Thom")

    ae86 = Car("Toyota", "AE86", "White", 12000.99)
    ae86.sell(Thom)
    ae86.print()

    benz = Car("Mercedes-Benz", "C-class", "Brown", 50000.00)
    benz.print()

    miata = Car("Mazda", "mx5", "Red", 6000.00)
    miata.sell()
    miata.print()

    porsche = Car("Porsche", "911", "Maroon", 60000.00)
    porsche.print()

    harley = Motorcycle("Harley & Davidson", "Motor", "Black", 25000.00)
    harley.print()


if __name__ == "__main__":
    main()
