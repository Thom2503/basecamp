def check_triangle(a, b, c):
    """
    Functie om te checken of je met lengtes a, b, c een driehoek kan maken

    @param int a - lengte a
    @param int b - lengte b
    @param int c - lengte c

    @return bool - of je er een driehoek mee kan maken
    """
    # om te bij te houden of het correct is en ga er altijd vanuit dat het geen driehoek is
    lengths = [a, b, c]  # lijstje met de argumenten om sommen van alle combi's te maken
    # geef de sommen van alle combinaties van de argumenten om te kunnen checken of een van
    # alle argumenten gelijk of groter is dan de som van de andere twee
    sums = [x + y for id, x in enumerate(lengths) for y in lengths[id + 1:]]
    # loop door alle sommen heen om te checken of een gelijk of groter is dan een argument
    for x in sums:
        if (x <= a) or (x <= b) or (x <= c):
            return False

    return True


if __name__ == "__main__":
    first = int(input("First straw:\n"))
    second = int(input("Second straw:\n"))
    third = int(input("Third straw:\n"))
    # als het een driehoek kan zijn print possible anders print not possible
    is_possiple = "possible" if check_triangle(first, second, third) else "impossible"
    # print het resultaat of het een driehoek kan zijn
    print(is_possiple)
