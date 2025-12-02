"""
-- Challenge 02: Fir-tual Tree  --

To train rookie elves on safe ladder-climbing and tree-decorating techniques, the North Pole Workshop uses a virtual Chrimbus tree.
This year, due to an increase in new elf trainees, the workshop needs a larger virtual tree display.

Render a triangle region of pixels to represent the shape of a fir tree.

When the triangle is correctly displayed, the elves will be able to practice their decorating skills without the risk of harming a single pine needle.
"""

import math
import time

from constants import MAX_COLOR_VAL, TIME_LIMIT
from led_matrix import LEDMatrix
from with_neopixel import with_neopixel


def is_in_triangle(x: int, y: int):
    """
    Returns True if x, y is in the desired triangle
    TODO: implement
    """
    return False


@with_neopixel
def triangle(pixels, time_limit=TIME_LIMIT):
    red = (0, MAX_COLOR_VAL, 0)  # Colors are G, R, B in [0, 255]
    # Instantiate the matrix helper
    # Without it, we would have to deal with pixel indices directly
    matrix = LEDMatrix(pixels=pixels)
    start = time.time()
    while True:  # Patterns must run on an event loop to work with the visualizer
        for led_idx, (x, y) in matrix.mapping.items():
            if is_in_triangle(x, y):
                pixels[led_idx] = red
        pixels.show()
        time.sleep(1)  # 1 fps
        elapsed = (time.time() - start) * 60
        if elapsed >= time_limit:
            break
