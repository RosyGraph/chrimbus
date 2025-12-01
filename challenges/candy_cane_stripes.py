"""
-- Challenge 03: Candy Cane Alignment --

The candy engineers have misplaced the diagram for the traditional diagonal candy-cane striping pattern.
Without it, confectionery production has ground to a halt.

Illuminte pixels to produce diagonal, alternating stripes across the grid.
Choose any width you like, provided the pattern is consistent across the display.

Only when the stripes appear will the peppermint peace be restored.
"""

import math
import time

from constants import MAX_COLOR_VAL, TIME_LIMIT
from led_matrix import LEDMatrix
from with_neopixel import with_neopixel


def is_in_stripes(x: int, y: int):
    """
    TODO: implement
    """
    return False


@with_neopixel
def candy_cane_stripes(pixels, time_limit=TIME_LIMIT):
    red = (0, MAX_COLOR_VAL, 0)  # Colors are G, R, B in [0, 255]
    # Instantiate the matrix helper
    # Without it, we would have to deal with pixel indices directly
    matrix = LEDMatrix(pixels=pixels)
    for led_idx, (x, y) in matrix.mapping.items():
        if is_in_stripes(x, y):
            pixels[led_idx] = red
    pixels.show()
    time.sleep(time_limit)
