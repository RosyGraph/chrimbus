"""
-- Challenge 08: Spiral of the Evergreens --

The Arctic Elven Anthropologists have discovered a forgotten ritual within the North Pole's Chrimbus archives.
Beginning at the center, a single point of light emanates outward in a spiral pattern, growing and growing until it fills the window.

Animate a spiral that starts from the center of the display and expands outward.
Any type of spiral, logarithmic, Archimedean, or invetned will suffice.

Long ago, before the snow
Noone knows quite when or how
A point of light began to grow
To shine upon your brow

Round it spun, a trembling flow
The scholars argued why, why now?
It wound itself in spiral slow
To blind the ox and cow
"""

import random
import time

from constants import MAX_COLOR_VAL, TIME_LIMIT
from led_matrix import LEDMatrix
from with_neopixel import with_neopixel


@with_neopixel
def spiral(pixels, time_limit=TIME_LIMIT):
    start = time.time()
    matrix = LEDMatrix(pixels=pixels)
    while True:
        # TODO: Implement
        time.sleep(0.02)  # With no delay between loops, the visualizer will crash
        if time.time() - start > time_limit * 60:
            break
