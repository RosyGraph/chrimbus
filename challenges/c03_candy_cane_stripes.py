"""
-- Challenge 03: Candy Cane Alignment --

The candy engineers have misplaced the diagram for the traditional diagonal candy-cane striping pattern.
Without it, confectionery production has ground to a halt.

Illuminte pixels to produce diagonal, alternating stripes across the grid.
Choose any width you like, provided the pattern is consistent across the display.

Only when the stripes appear will the peppermint peace be restored.
"""

import numpy as np
import time

from constants import MAX_COLOR_VAL, TIME_LIMIT
from led_matrix import LEDMatrix
from with_neopixel import with_neopixel


def is_in_stripes(x: int, y: int):
    """
    TODO: implement
    """
    return x == y


@with_neopixel
def candy_cane_stripes(pixels, time_limit=TIME_LIMIT):
    red = (0, MAX_COLOR_VAL, 0)  # Colors are G, R, B in [0, 255]
    # Instantiate the matrix helper
    # Without it, we would have to deal with pixel indices directly
    matrix = LEDMatrix(pixels=pixels)
    start = time.time()
    grid_d = 7
    x_space = list(np.linspace(0, 1, num=grid_d))
    d = x_space[1] - x_space[0]
    color_space = list(np.linspace(0, MAX_COLOR_VAL, num=MAX_COLOR_VAL)) + list(
        np.linspace(MAX_COLOR_VAL, 0, num=MAX_COLOR_VAL)
    )
    while True:
        for frame in color_space:
            pixels[:] = [
                (MAX_COLOR_VAL, MAX_COLOR_VAL - int(frame), MAX_COLOR_VAL - int(frame))
                for _ in pixels
            ]
            for i, (x, y) in matrix.mapping.items():
                offsets = [o * d for o in range(-grid_d, grid_d, 2)]
                if any(x - offset < y and x - offset > y - d for offset in offsets):
                    pixels[i] = red
            frame = int(not frame)
            pixels.show()
            time.sleep(0.01)
            elapsed = time.time() - start
            if elapsed >= time_limit * 60:
                return
