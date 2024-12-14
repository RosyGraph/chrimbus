import json
import numpy as np
import matplotlib.pyplot as plt

# Load LED mapping
with open("led_mapping.json") as f:
    led_mapping = json.load(f)

# Extract current positions
points = np.array(list(led_mapping.values()))
x_coords, y_coords = points[:, 0], points[:, 1]

# Find bounding box
min_x, max_x = min(x_coords), max(x_coords)
min_y, max_y = min(y_coords), max(y_coords)

# Define target space
TARGET_WIDTH, TARGET_HEIGHT = 60, 45  # Rectangular space dimensions

# Transform each point to the rectangular space
transformed_mapping = {}
for i, (x, y) in enumerate(points):
    new_x = (x - min_x) / (max_x - min_x) * TARGET_WIDTH
    new_y = (y - min_y) / (max_y - min_y) * TARGET_HEIGHT
    transformed_mapping[i] = (new_x, new_y)

# Save the transformed mapping
with open("transformed_led_mapping.json", "w") as f:
    json.dump(transformed_mapping, f)

# Plot the transformed points
transformed_points = np.array(list(transformed_mapping.values()))
plt.figure(figsize=(8, 6))
plt.scatter(transformed_points[:, 0], transformed_points[:, 1], c='blue', label='Transformed LEDs', s=10)
plt.gca().invert_yaxis()  # Match original coordinate system
plt.title("LED Mapping to Rectangular Space")
plt.xlabel("Normalized X")
plt.ylabel("Normalized Y")
plt.legend()
plt.show()
