side_a = int(input("Side a:\n"))
side_b = int(input("Side b:\n"))
side_c = int(input("Side c:\n"))

def triangle_kind(a, b, c):
    lst = [a, b, c] # om te checken of ze allemaal anders zijn

    if a == b == c:
        return "equilateral"
    elif len(lst) == len(set(lst)):
        return "scalene"
    else:
        return "isosceles"

kind = triangle_kind(side_a, side_b, side_c)
print(f"Your kind of triangle is: {kind}")
