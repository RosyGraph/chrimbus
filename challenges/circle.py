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
    return False


@with_neopixel
def circle(pixels, time_limit=TIME_LIMIT):
    """Shows a red circle for `time_limit` seconds"""
    red = (0, MAX_COLOR_VAL, 0)  # Colors are G, R, B in [0, 255]
    # Instantiate the matrix helper
    # Without it, we would have to deal with pixel indices directly
    matrix = LEDMatrix(pixels=pixels)
    for led_idx, (x, y) in matrix.mapping.items():
        if is_in_circle(x, y):
            pixels[led_idx] = red
    pixels.show()
    time.sleep(time_limit)
