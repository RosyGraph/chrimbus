import json


def scale_mapping(mapping, target_width, target_height):
    """
    Scale the LED mapping to a target width and height.
    """
    scaled_mapping = {}
    min_x = min(coord[0] for coord in mapping.values())
    max_x = max(coord[0] for coord in mapping.values())
    min_y = min(coord[1] for coord in mapping.values())
    max_y = max(coord[1] for coord in mapping.values())

    for idx, (x, y) in mapping.items():
        # Scale x and y to the target grid
        scaled_x = round((x - min_x) / (max_x - min_x) * (target_width - 1))
        scaled_y = round((y - min_y) / (max_y - min_y) * (target_height - 1))
        scaled_mapping[idx] = (scaled_x, scaled_y)

    return scaled_mapping


with open("transformed_led_mapping.json") as f:
    led_mapping = json.load(f)

# Scale the mapping to 30x15
scaled_mapping = scale_mapping(led_mapping, target_width=30, target_height=15)

# Save the scaled mapping
with open("scaled_led_mapping_30x15.json", "w") as f:
    json.dump(scaled_mapping, f)
