class Product:
    """
    Class to define a product name, amount, and price
    """

    def __init__(self, name, amount, price):
        self.name: str = name
        self.amount: int = amount
        self.price: float = price

    def get_price(self, amount) -> float:
        full_price = amount * self.price
        print(full_price, "prijs")
        if 10 <= amount <= 99:
            return full_price - (full_price * 0.1)
        elif amount >= 100:
            return full_price - (full_price * 0.2)
        else:
            return full_price

    def make_purchase(self, amount) -> None:
        self.amount -= amount


def main():
    toothbrushes = Product("Toothbrush", 100, 5)
    print(toothbrushes.amount)
    print(toothbrushes.get_price(10))
    print(toothbrushes.get_price(100))
    toothbrushes.make_purchase(10)
    print(toothbrushes.amount)


if __name__ == "__main__":
    main()
