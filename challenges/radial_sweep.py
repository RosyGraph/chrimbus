"""
-- Challenge 06: Polar Radar --

After the recent near-collision during the Flight Agility Readiness Trial, the North Pole Aerosleigh Command requires a functional radar-like sweep display to track reindeer flight patterns in real time.

Your task is to illuminate a rotating radial sweep centered on the display.
The sweep should rotate smoothly around the center, like the beam of an old-world radar.
HINT: https://docs.python.org/3/library/math.html#math.atan2

When the beam turns uninterrupted, the sleigh will once again master the sky.
"""

import random
import time

from constants import MAX_COLOR_VAL, TIME_LIMIT
from led_matrix import LEDMatrix
from with_neopixel import with_neopixel


@with_neopixel
def radial_sweep(pixels, time_limit=TIME_LIMIT):
    start = time.time()
    matrix = LEDMatrix(pixels=pixels)
    while True:
        # TODO: Implement radial sweep pattern here
        time.sleep(0.02)  # With no delay between loops, the visualizer will crash
        if time.time() - start > time_limit * 60:
            break
