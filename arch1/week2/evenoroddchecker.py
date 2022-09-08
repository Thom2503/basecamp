number = int(input("Enter a number:\n"))

is_even = lambda n : n % 2 == 0

print("even") if is_even(number) == True else print("odd")
