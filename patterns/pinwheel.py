import time

from constants import MAX_COLOR_VAL, TIME_LIMIT
from led_matrix import LEDMatrix
from with_neopixel import with_neopixel


@with_neopixel
def pinwheel(pixels, time_limit=TIME_LIMIT):
    start = time.time()
    red = (0, MAX_COLOR_VAL, 0)
    white = (MAX_COLOR_VAL, MAX_COLOR_VAL, MAX_COLOR_VAL)
    slopes = [s / 10 for s in range(-20, 21, 5)]

    regions = {
        "upper": lambda x, y, slope: y >= slope * (x - 0.5) + 0.5,
        "lower": lambda x, y, slope: y <= slope * (x - 0.5) + 0.5,
    }

    stop = False
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
