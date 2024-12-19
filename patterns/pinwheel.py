import time

import neopixel

from constants import DATA_PIN, MAX_COLOR_VAL, NUM_LIGHTS, TIME_LIMIT
from led_matrix import LEDMatrix


def pinwheel(time_limit=TIME_LIMIT):
    start = time.time()
    red = (0, MAX_COLOR_VAL, 0)
    white = (MAX_COLOR_VAL, MAX_COLOR_VAL, MAX_COLOR_VAL)
    slopes = [s / 10 for s in range(-20, 21, 5)]

    regions = {
        "upper": lambda x, y, slope: y >= slope * (x - 0.5) + 0.5,
        "lower": lambda x, y, slope: y <= slope * (x - 0.5) + 0.5,
    }

    stop = False
    with neopixel.NeoPixel(DATA_PIN, NUM_LIGHTS, auto_write=False) as pixels:
        matrix = LEDMatrix(pixels=pixels)
        while not stop:
            for _, region_fn in regions.items():
                for slope in slopes:
                    for i, (x, y) in matrix.mapping.items():
                        pixels[i] = red if region_fn(x, y, slope) else white
                    pixels.show()
                    time.sleep(0.2)
                    elapsed = time.time() - start
                    if elapsed > time_limit * 60:
                        stop = True
                        break
                if stop:
                    break
