import json
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata

# Load LED mapping
with open("led_mapping.json") as f:
    led_mapping = json.load(f)

# Extract current positions
points = np.array(list(led_mapping.values()))
x_coords, y_coords = points[:, 0], points[:, 1]

# Define the target rectangular space
TARGET_WIDTH, TARGET_HEIGHT = 60, 45
grid_x, grid_y = np.linspace(min(x_coords), max(x_coords), TARGET_WIDTH), np.linspace(min(y_coords), max(y_coords), TARGET_HEIGHT)
grid_x, grid_y = np.meshgrid(grid_x, grid_y)

# Interpolate the points to a rectangular grid
grid_z = griddata(points, np.arange(len(points)), (grid_x, grid_y), method='nearest')

# Plot the transformed grid
plt.figure(figsize=(8, 6))
plt.scatter(grid_x, grid_y, c='blue', label='Projected LEDs', s=10)
plt.gca().invert_yaxis()  # Match original coordinate system
plt.title("LED Projection to Rectangular Space")
plt.xlabel("Normalized X")
plt.ylabel("Normalized Y")
plt.legend()
plt.show()

# Save the transformed mapping for further use
projected_mapping = {
    f"led_{i}": (float(x), float(y))
    for i, (x, y) in enumerate(zip(grid_x.flatten(), grid_y.flatten()))
}

with open("projected_led_mapping.json", "w") as f:
    json.dump(projected_mapping, f)
print("Projected LED mapping saved to 'projected_led_mapping.json'")
