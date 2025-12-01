import json


def normalize_mapping(mapping):
    """
    Normalize the LED coordinates to a 0-1 range for both X and Y axes.
    """
    min_x = min(coord[0] for coord in mapping.values())
    max_x = max(coord[0] for coord in mapping.values())
    min_y = min(coord[1] for coord in mapping.values())
    max_y = max(coord[1] for coord in mapping.values())

    normalized_mapping = {}
    for idx, (x, y) in mapping.items():
        normalized_x = (x - min_x) / (max_x - min_x)
        normalized_y = (y - min_y) / (max_y - min_y)
        normalized_mapping[idx] = (normalized_x, normalized_y)

    return normalized_mapping


# Load your original mapping
with open("led_mapping.json") as f:
    raw_mapping = json.load(f)

# Normalize the mapping
normalized_mapping = normalize_mapping(raw_mapping)

# Save the normalized mapping
with open("normalized_led_mapping.json", "w") as f:
    json.dump(normalized_mapping, f)


# Extract normalized points
normalized_points = list(normalized_mapping.values())
x_coords, y_coords = zip(*normalized_points)
