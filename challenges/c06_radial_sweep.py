"""
-- Challenge 06: Polar Radar --

After the recent near-collision during the Flight Agility Readiness Trial, the North Pole Aerosleigh Command requires a functional radar-like sweep display to track reindeer flight patterns in real time.

Your task is to illuminate a rotating radial sweep centered on the display.
The sweep should rotate smoothly around the center, like the beam of an old-world radar.
HINT: https://docs.python.org/3/library/math.html#math.atan2

When the beam turns uninterrupted, the sleigh will once again master the sky.
"""

import numpy as np
import math
import time

from constants import MAX_COLOR_VAL, TIME_LIMIT
from led_matrix import LEDMatrix
from with_neopixel import with_neopixel


@with_neopixel
def radial_sweep(pixels, time_limit=TIME_LIMIT):
    start = time.time()
    matrix = LEDMatrix(pixels=pixels)
    sweep_positions = np.linspace(0, 2 * np.pi, num=200)
    while True:
        for pos in sweep_positions:
            print(pos)
            for i, (x, y) in matrix.mapping.items():
                x_s, y_s = x - 0.5, y - 0.5
                theta = math.atan2(y_s, x_s) % (math.pi * 2)
                r_ = (x_s**2 + y_s**2) ** 0.5
                if r_ > 0.5:
                    continue
                lo, hi = pos, pos + 0.1
                if theta > lo and theta < hi:
                    pixels[i] = (MAX_COLOR_VAL, MAX_COLOR_VAL, MAX_COLOR_VAL)
                else:
                    g, r, b = pixels[i]
                    pixels[i] = (max(0, g - 5), max(0, r - 5), max(0, b - 5))
            pixels.show()
            time.sleep(0.01)
        if time.time() - start > time_limit * 60:
            break
