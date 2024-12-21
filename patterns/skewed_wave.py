import math
import time

from constants import MAX_COLOR_VAL
from led_matrix import LEDMatrix
from math_helpers import periodic_skewed_exponential
from with_neopixel import with_neopixel


@with_neopixel
def skewed_wave(pixels, time_limit):
    start = time.time()
    matrix = LEDMatrix(pixels=pixels)
    period = 2 * math.pi
    while True:
        for i, (_, y) in matrix.mapping.items():
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
