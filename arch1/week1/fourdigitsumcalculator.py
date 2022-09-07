import textwrap

number = input("Enter a 4 digit number you want the sum of:\n")

numbers = textwrap.wrap(number, 1)
sum = 0
for i in numbers:
    sum += int(i)

print(f"Sum: {sum}")
