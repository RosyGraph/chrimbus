import json
import math

ASPECT_RATIO = 1.365


def load_v0_mapping():
    with open("geometry/v0_led_mapping.json", "r") as f:
        return json.load(f)


def load_normalized_v0_mapping():
    with open("geometry/v0_led_mapping_normalized.json", "r") as f:
        return json.load(f)


def calculate_aspect_ratio():
    v0_mapping = load_v0_mapping()
    x_coords = {x for x, _ in v0_mapping.values()}
    y_coords = {y for _, y in v0_mapping.values()}
    min_x, max_x = min(x_coords), max(x_coords)
    dx = max_x - min_x
    min_y, max_y = min(y_coords), max(y_coords)
    dy = max_y - min_y
    return dx/dy


def norm(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)


def cum_dist(mapping):
    mapping_arr = list(mapping.values())
    cum_distances = [0]
    for i in range(len(mapping) - 1):
        d = norm(*mapping_arr[i], *mapping_arr[i+1])
        cum_distances.append(cum_distances[-1] + d)
    return cum_distances


def main():
    mapping = load_normalized_v0_mapping()
    c = cum_dist(mapping)
    num_lights = len(mapping)
    mapping_arr = list(mapping.values())
    target_distance = c[-1] / (250-1)
    new_mapping = []
    i = 0
    for j in range(250):
        dj = j * target_distance
        while dj > c[i+1] and i < len(c)-2:
            i += 1
        t = (dj - c[i]) / (c[i+1] - c[i])
        new_x = mapping_arr[i][0] + t*(mapping_arr[i+1][0] - mapping_arr[i][0])
        new_y = mapping_arr[i][1] + t*(mapping_arr[i+1][1] - mapping_arr[i][1])
        new_mapping.append([new_x, new_y])
    new_mapping = {str(i): t for i, t in enumerate(new_mapping)}
    with open("geometry/v1_led_mapping.synthetic.json", "w") as f:
        json.dump(new_mapping, f)

main()
