import math
import time

import neopixel

from constants import DATA_PIN, MAX_COLOR_VAL, NUM_LIGHTS
from led_matrix import LEDMatrix
from math_helpers import periodic_skewed_exponential


def skewed_wave(time_limit):
    start = time.time()
    with neopixel.NeoPixel(DATA_PIN, NUM_LIGHTS, auto_write=False) as pixels:
        matrix = LEDMatrix(pixels=pixels)
        period = 2 * math.pi
        while True:
            for i, (x, y) in matrix.mapping.items():
                bound_t = (time.time() * 0.3) % period
                intensity = periodic_skewed_exponential(bound_t + period * y)
                green_intensity = int(MAX_COLOR_VAL * intensity)
                red_intensity = MAX_COLOR_VAL
                blue_intensity = int(MAX_COLOR_VAL * intensity)
                pixels[i] = (green_intensity, red_intensity, blue_intensity)
            pixels.show()

            elapsed = time.time() - start
            if elapsed > time_limit * 60:
                break
