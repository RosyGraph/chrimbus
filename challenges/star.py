"""
-- Challenge 04: Star  --

The reindeer night-vision goggles have recently been upgraded to version 7.18 after the unfortunate accident involving an F-117A Nighthawk and a weather balloon during this year's Flight Agility Readiness Trial.
The goggles must be recalibrated against a high-contrast celestial reference point.

Illuminate the pixels in the shape of a bright star at the center of the display.
Precision matters; an indistinct blob will result in poor flight performance.

When the star is cut from light and hangs true in the darkness, the long winter sky will welcome the sleigh once more.
"""

import math
import time

from constants import MAX_COLOR_VAL, TIME_LIMIT
from led_matrix import LEDMatrix
from with_neopixel import with_neopixel


def is_in_star(x: int, y: int):
    """
    TODO: implement
    """
    return False


@with_neopixel
def star(pixels, time_limit=TIME_LIMIT):
    red = (0, MAX_COLOR_VAL, 0)  # Colors are G, R, B in [0, 255]
    # Instantiate the matrix helper
    # Without it, we would have to deal with pixel indices directly
    matrix = LEDMatrix(pixels=pixels)
    for led_idx, (x, y) in matrix.mapping.items():
        if is_in_star(x, y):
            pixels[led_idx] = red
    pixels.show()
    time.sleep(time_limit)
