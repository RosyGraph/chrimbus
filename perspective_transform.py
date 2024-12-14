import json

import cv2
import numpy as np


def apply_perspective_transform(mapping, matrix):
    """
    Apply a perspective transformation to all LED points.

    Args:
        mapping (dict): A dictionary of LED indices mapped to (x, y) positions.
        matrix (numpy.ndarray): The 3x3 perspective transformation matrix.

    Returns:
        dict: A new mapping with transformed (x, y) coordinates.
    """
    transformed_mapping = {}
    for idx, (x, y) in mapping.items():
        # Create a 1x1x3 array for the point (x, y, 1)
        src = np.array([[[x, y]]], dtype=np.float32)
        # Apply the perspective transformation
        dst = cv2.perspectiveTransform(src, matrix)
        # Extract the transformed point
        transformed_mapping[idx] = (dst[0][0][0], dst[0][0][1])
    return transformed_mapping


def renormalize_mapping(mapping):
    """
    Renormalize the LED coordinates to fit within [0, 1] for both X and Y.
    """
    # Extract all X and Y values
    x_coords = [coord[0] for coord in mapping.values()]
    y_coords = [coord[1] for coord in mapping.values()]

    # Find the min and max for both axes
    min_x, max_x = min(x_coords), max(x_coords)
    min_y, max_y = min(y_coords), max(y_coords)

    # Renormalize each point to fit in [0, 1]
    renormalized_mapping = {}
    for idx, (x, y) in mapping.items():
        renormalized_x = (x - min_x) / (max_x - min_x)
        renormalized_y = (y - min_y) / (max_y - min_y)
        renormalized_mapping[idx] = (renormalized_x, renormalized_y)

    return renormalized_mapping


# Define the ideal corners in normalized space
ideal_corners = {
    "top_left": [0, 0],
    "top_right": [1, 0],
    "bottom_left": [0, 1],
    "bottom_right": [1, 1],
}

# Parse the provided normalized mapping
with open("normalized_led_mapping.json") as f:
    led_mapping = {int(k): v for k, v in json.load(f).items()}

# Find the closest LED to each corner
corner_leds = {}
for corner_name, corner_pos in ideal_corners.items():
    min_distance = float("inf")
    closest_led = None
    for led_id, (x, y) in led_mapping.items():
        distance = np.sqrt((x - corner_pos[0]) ** 2 + (y - corner_pos[1]) ** 2)
        if distance < min_distance:
            min_distance = distance
            closest_led = (led_id, (x, y))
    corner_leds[corner_name] = closest_led

src_points = np.float32(
    [
        corner_leds["top_left"][1],
        corner_leds["top_right"][1],
        corner_leds["bottom_left"][1],
        corner_leds["bottom_right"][1],
    ]
)
dst_points = np.float32(
    [
        [0, 0],  # Ideal top-left
        [1, 0],  # Ideal top-right
        [0, 1],  # Ideal bottom-left
        [1, 1],  # Ideal bottom-right
    ]
)
perspective_matrix = cv2.getPerspectiveTransform(src_points, dst_points)
transformed_mapping = apply_perspective_transform(led_mapping, perspective_matrix)
renormalized_mapping = renormalize_mapping(transformed_mapping)
renormalized_mapping = {
    k: (float(v[0]), float(v[1])) for k, v in renormalized_mapping.items()
}

# Save the renormalized mapping to a JSON file
output_file = "corrected_led_mapping.json"
with open(output_file, "w") as f:
    json.dump(renormalized_mapping, f, indent=4)

print(f"Corrected LED mapping saved to {output_file}")
