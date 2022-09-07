gizmo_weight  = 112
widget_weight = 75

gizmos  = int(input("How many gizmos did you order?\n"))
widgets = int(input("How many widgets did you order?\n"))

total_weight = (gizmos * gizmo_weight) + (widgets * widget_weight)

print(f"The Total Weight of the Order: {total_weight}")
