import math
import time

import neopixel

from constants import DATA_PIN, MAX_COLOR_VAL, NUM_LIGHTS, TIME_LIMIT
from led_matrix import LEDMatrix
from math_helpers import periodic_skewed_exponential


def rainbow_wave(time_limit=TIME_LIMIT):
    start = time.time()
    with neopixel.NeoPixel(DATA_PIN, NUM_LIGHTS, auto_write=False) as pixels:
        matrix = LEDMatrix(pixels=pixels)
        period = 2 * math.pi
        while True:
            for i, (x, y) in matrix.mapping.items():
                bound_t = (time.time()) % period
                intensity = periodic_skewed_exponential(bound_t + period * y)
                green_intensity = int(MAX_COLOR_VAL * ((math.cos(bound_t) + 1) / 2) * x)
                red_intensity = int(MAX_COLOR_VAL * (1 - intensity))
                blue_intensity = int(MAX_COLOR_VAL * intensity)
                pixels[i] = (green_intensity, red_intensity, blue_intensity)
            pixels.show()

            elapsed = time.time() - start
            if elapsed > time_limit * 60:
                break
