class Bottle:

    def __init__(self, material, colour, capacity, has_cap):
        self.material: str = material
        self.colour: str = colour
        self.capacity: int = capacity
        self.has_cap: bool = has_cap
        self.amount_filled: int

    def fill(self, amount):
        self.amount_filled = amount

    def drink(self, amount):
        self.amount_filled = amount
