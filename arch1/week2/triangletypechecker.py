side_a = int(input("Side a:\n"))
side_b = int(input("Side b:\n"))
side_c = int(input("Side c:\n"))

def triangle_kind(a, b, c):
    if a == b == c:
        return "equilateral"
    elif a != b != c:
        return "scalene"
    else:
        return "isosceles"

kind = triangle_kind(side_a, side_b, side_c)
print(f"Your kind of triangle is: {kind}")
