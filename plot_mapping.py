import json
import matplotlib.pyplot as plt

with open("led_mapping.json") as f:
    mapping = json.load(f)

x_coords, y_coords = zip(*mapping.values())
plt.scatter(x_coords, y_coords)
plt.gca().invert_yaxis()  # Invert Y-axis for image coordinates
plt.title("LED Mapping")
plt.xlabel("X Coordinate")
plt.ylabel("Y Coordinate")
plt.show()
