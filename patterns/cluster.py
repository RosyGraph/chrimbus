import colorsys
import random
import time
from collections import defaultdict

from constants import MAX_COLOR_VAL, TIME_LIMIT
from led_matrix import LEDMatrix
from with_neopixel import with_neopixel


def hue_to_rgb(hue):
    rgb = colorsys.hsv_to_rgb(hue, 1, 1)
    red, green, blue = [int(c * MAX_COLOR_VAL) for c in rgb]
    return (green, red, blue)


def euclidean_distance(x1, y1, x2, y2):
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5


@with_neopixel
def cluster(pixels, time_limit=TIME_LIMIT):
    start = time.time()
    matrix = LEDMatrix(pixels=pixels)

    # Number of clusters
    k = 3

    # Generate hues for clusters
    hues = {hue_to_rgb(i / k): [] for i in range(k)}

    # Randomly initialize cluster centers
    starting_coords = random.sample(list(matrix.mapping.items()), k)
    for hue, coord in zip(hues.keys(), starting_coords):
        hues[hue].append(coord)

    # Track claimed LEDs
    claimed_leds = set()

    while True:
        for hue, coords in hues.items():
            new_coords = []

            # Grow each cluster
            for i, (x, y) in coords:
                pixels[i] = hue  # Set LED color
                pixels.show()
                time.sleep(0.05)

                # Find the closest unclaimed LED
                closest_leds = sorted(
                    [
                        (idx, (nx, ny))
                        for idx, (nx, ny) in matrix.mapping.items()
                        if idx not in claimed_leds
                    ],
                    key=lambda tup: euclidean_distance(x, y, *tup[1]),
                )

                # Add one of the closest LEDs to the cluster
                for idx, (nx, ny) in closest_leds:
                    if idx not in claimed_leds:
                        claimed_leds.add(idx)
                        new_coords.append((idx, (nx, ny)))
                        break

            # Add the newly claimed LEDs to the cluster
            hues[hue].extend(new_coords)

        # Update the LED matrix
        pixels.show()
        time.sleep(0.5)  # Adjust for faster/slower updates
        if len(claimed_leds) == len(matrix.mapping):
            k += 1
            hues = {hue_to_rgb(i / k): [] for i in range(k)}
            starting_coords = random.sample(list(matrix.mapping.items()), k)
            for hue, coord in zip(hues.keys(), starting_coords):
                hues[hue].append(coord)
            claimed_leds = set()
            pixels.fill((0, 0, 0))

        # Check time limit
        elapsed = time.time() - start
        if elapsed > time_limit * 60:
            break
