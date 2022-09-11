years = int(input("What is your human age?\n"))

if years < 0:
    print("You can't use a negative number")
else:
    dog_years = 0
    # years + 1 is om het jaar een "volledig" jaar te maken
    for i in range(1, years + 1):
        # honden groeien in hun eerste 2 jaar 10,5 jaar
        if i == 1 or i == 2:
            dog_years += 10.5
        else:
            dog_years += 4
    print(f"{years} human years is equal to {dog_years} dog years.")
