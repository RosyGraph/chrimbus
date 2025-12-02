"""
-- Challenge 01: Nose So Bright --

The Chrimbus reindeer handlers have discovered that Rudolf's famous nose has dimmed.
Without its brilliant glow, the reindeer cannot guide Santa's sleigh through the foggy night sky.
In order to restore its radiant shine, the elves require a perfect red circle projected onto the window grid.

Your task is to illuminate a circle centered on the display.
Use the pixel coordinates provided by LEDMatrix.

Once the circle is correctly displayed, the elves will be able to recalibrate Rudolf's nose, and the sleigh can take flight once more.
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
    return False


@with_neopixel
def circle(pixels, time_limit=TIME_LIMIT):
    """Shows a red circle for `time_limit` seconds"""
    red = (0, MAX_COLOR_VAL, 0)  # Colors are G, R, B in [0, 255]
    # Instantiate the matrix helper
    # Without it, we would have to deal with pixel indices directly
    matrix = LEDMatrix(pixels=pixels)
    start = time.time()
    while True:  # Patterns must run on an event loop to work with the visualizer
        for led_idx, (x, y) in matrix.mapping.items():
            if is_in_circle(x, y):
                pixels[led_idx] = red
        pixels.show()
        time.sleep(1)  # 1fps
        elapsed = (time.time() - start) * 60
        if elapsed >= time_limit:
            break
