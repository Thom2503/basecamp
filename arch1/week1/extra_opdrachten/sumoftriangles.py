sum = 0

for i in range(0, 2):
    height = int(input("What is the height?\n"))
    base   = int(input("What is the base?\n"))

    area = (height * base) / 2
    sum += area

print(f"The sum of the two traingle areas is {sum}")
