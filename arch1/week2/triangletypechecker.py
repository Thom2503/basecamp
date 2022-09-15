sides = input("Sides:\n")

def triangle_kind(a, b, c):
    lst = [a, b, c] # om te checken of ze allemaal anders zijn

    if a == b == c:
        return "equilateral"
    elif len(lst) == len(set(lst)):
        return "scalene"
    else:
        return "isosceles"

sides = "".join(filter(lambda c : "0" <= c <= "9", sides))
kind = triangle_kind(sides[0], sides[1], sides[2])
print(f"Your kind of triangle is: {kind}")
