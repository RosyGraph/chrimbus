"""
BRAZIL
Author: Joe
"""

import math
import time

from constants import MAX_COLOR_VAL, TIME_LIMIT
from led_matrix import LEDMatrix
from with_neopixel import with_neopixel


def is_in_circle(x: int, y: int):
    """
    Returns True if x, y is in the desired
    TODO: implement
    """
    return 0.04 <= (x - 0.5) ** 2 + (y - 0.5) ** 2 <= 0.15


def is_in_center(x: int, y: int):
    """
    Returns True if x, y is in the desired
    TODO: implement
    """
    return (x - 0.5) ** 2 + (y - 0.5) ** 2 <= 0.04


@with_neopixel
def brazil(pixels, time_limit=TIME_LIMIT):
    """Shows a red circle for `time_limit` seconds"""
    green = (MAX_COLOR_VAL, 0, 0)  # Colors are G, R, B in [0, 255]
    blue = (0, 0, MAX_COLOR_VAL)
    yellow = (MAX_COLOR_VAL, MAX_COLOR_VAL, 0)
    # Instantiate the matrix helper
    # Without it, we would have to deal with pixel indices directly
    matrix = LEDMatrix(pixels=pixels)
    start = time.time()
    while True:  # Patterns must run on an event loop to work with the visualizer
        for led_idx, (x, y) in matrix.mapping.items():
            if is_in_circle(x, y):
                pixels[led_idx] = yellow
            elif is_in_center(x, y):
                pixels[led_idx] = blue
            else:
                pixels[led_idx] = green
        pixels.show()
        time.sleep(1)  # 1fps
        elapsed = (time.time() - start) * 60
        if elapsed >= time_limit:
            break
