import random
import time

from constants import MAX_COLOR_VAL, TIME_LIMIT
from led_matrix import LEDMatrix
from with_neopixel import with_neopixel


def manhattan_distance(food_position, coords):
    x, y = coords
    return abs(x - food_position[0]) + abs(y - food_position[1])


def is_tree(x, y):
    x = x * 10
    y = 10 - (y * 10)
    return (
        (x > 1)
        and (x < 9)
        and (y > 1)
        and (y < 9)
        and (y < 2 * x - 1)
        and (y < -2 * x + 19)
    )


@with_neopixel
def tree(pixels, time_limit=TIME_LIMIT):
    start = time.time()
    matrix = LEDMatrix(pixels=pixels)
    pixels.fill((0, 0, 0))
    tree_coords = [(i, (x, y)) for i, (x, y) in matrix.mapping.items() if is_tree(x, y)]
    highest_tree = min(tree_coords, key=lambda tup: tup[1][1])
    closest_leds = sorted(
        [(i, (x, y)) for i, (x, y) in matrix.mapping.items()],
        key=lambda tup: manhattan_distance(highest_tree[1], tup[1]),
    )[:3]
    tree_coords = [
        tup
        for tup in tree_coords
        if tup[0] not in closest_leds and tup[0] != highest_tree[0]
    ]
    for i, _ in closest_leds:
        pixels[i] = (MAX_COLOR_VAL, MAX_COLOR_VAL, 0)
    pixels[highest_tree[0]] = (MAX_COLOR_VAL, MAX_COLOR_VAL, 0)
    ornaments_coords = [(i, (x, y)) for i, (x, y) in tree_coords if i % 5 == 0]
    for i, _ in ornaments_coords:
        pixels[i] = (0, MAX_COLOR_VAL, 0)
    tree_coords = [(i, (x, y)) for i, (x, y) in tree_coords if i % 5 != 0]
    lights_coords = []
    while True:
        for i, _ in tree_coords:
            pixels[i] = (MAX_COLOR_VAL, 0, 0)
        if random.random() > 0.5 or not lights_coords:
            lights_coords.append(random.choice(tree_coords))
        if len(lights_coords) > 5 or random.random() < 0.2:
            lights_coords = lights_coords[1:]
        for i, _ in lights_coords:
            intensity = (time.time() * i) % 1
            value = int(MAX_COLOR_VAL * intensity)
            pixels[i] = (value, value, value)
        pixels.show()
        time.sleep(0.1)
        elapsed = time.time() - start
        if elapsed > time_limit * 60:
            break
