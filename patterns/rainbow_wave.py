import math
import time

from constants import MAX_COLOR_VAL, TIME_LIMIT
from led_matrix import LEDMatrix
from math_helpers import periodic_skewed_exponential
from with_neopixel import with_neopixel


@with_neopixel
def rainbow_wave(pixels, time_limit=TIME_LIMIT):
    start = time.time()
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
