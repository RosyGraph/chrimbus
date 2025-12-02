"""
-- Challenge 02: Fir-tual Tree  --

To train rookie elves on safe ladder-climbing and tree-decorating techniques, the North Pole Workshop uses a virtual Chrimbus tree.
This year, due to an increase in new elf trainees, the workshop needs a larger virtual tree display.

Render a triangle region of pixels to represent the shape of a fir tree.

When the triangle is correctly displayed, the elves will be able to practice their decorating skills without the risk of harming a single pine needle.
"""

import math
import numpy as np
import time

from constants import MAX_COLOR_VAL, TIME_LIMIT
from led_matrix import LEDMatrix
from with_neopixel import with_neopixel


def is_in_triangle(x: int, y: int, f: float):
    """
    The equation for a triangle is given by
    max(-2y, y - x*sqrt(3), y + x*sqrt(3)) = r

    Rotation about angle phi
    x = x cos(phi) - y sin(phi)
    y = y sin(phi) + y cos(phi)
    """
    r = 0.5
    x_ = x - 0.5
    y_ = y - 0.55
    x_r = x_ * math.cos(f) - y_ * math.sin(f)
    y_r = x_ * math.sin(f) + y_ * math.cos(f)
    k = 3**0.5
    return max(2 * y_r, -y_r + x_r * k, -y_r - x_r * k) < r


@with_neopixel
def triangle(pixels, time_limit=TIME_LIMIT):
    matrix = LEDMatrix(pixels=pixels)
    start = time.time()
    steps = list(np.multiply(np.arctan(np.linspace(-1, 1, num=500)), 8))
    while True:
        for step in steps:
            for led_idx, (x, y) in matrix.mapping.items():
                if is_in_triangle(x, y, step):
                    g = int(max(min(MAX_COLOR_VAL, MAX_COLOR_VAL - 20 * step), 0) / 1.5)
                    print(g)
                    pixels[led_idx] = (MAX_COLOR_VAL, g, g)
                else:
                    pixels[led_idx] = (0, 0, 0)
            pixels.show()
            time.sleep(0.02)
        steps = list(reversed(steps))
        if start - time.time() * 60 >= time_limit:
            break
