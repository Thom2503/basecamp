tip_percent = 15 / 100 # is 0.15 == 15%
tax_percent = 21 / 100 # zelfde als tip

cost_of_meal = float(input(""))

tip = tip_percent * cost_of_meal
tax = tax_percent * cost_of_meal

total = cost_of_meal + tax + tip

print(f"Tax: {format(tax, 'g')} , Tip: {format(tip, 'g')} , Total: {format(total, 'g')}")
