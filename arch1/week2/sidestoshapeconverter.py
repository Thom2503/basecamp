shapes = {3 : "Driehoek", 4 : "Vierhoek", 5 : "Vijfhoek", 6 : "Zeshoek", 7 : "Zevenhoek",
          8 : "Achthoek", 9 : "Negenhoek", 10 : "Tienhoek"}

sides = int(input("Number of sides: \n"))
if sides < 3 or sides > 10:
    print(f"Shape is not found with {sides} number of sides")
else:
    print(f"The shape with {sides} sides is {shapes[sides]}")
