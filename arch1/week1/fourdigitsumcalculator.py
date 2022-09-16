number = input("Enter a 4 digit number you want the sum of:\n")

sum = 0
for i in number:
    sum += int(i)

print(f"{number[0]}+{number[1]}+{number[2]}+{number[3]}={sum}")
