"""
-- Challenge 05: Silent Snowfall --

The forecast promised a gentle snowfall for Chrimbus Eve, but the storm sprites have forgotten how snow is supposed to fall.
They need a demonstration.

Simulate snow drifting from the top of the display downwards.
Flakes that reach the bottom should disappear.

When the snow falls softly without end, the sprites will remember their purpose.
"""

import random
import time

from constants import MAX_COLOR_VAL, TIME_LIMIT
from led_matrix import LEDMatrix
from with_neopixel import with_neopixel


@with_neopixel
def falling_snow(pixels, time_limit=TIME_LIMIT):
    start = time.time()
    matrix = LEDMatrix(pixels=pixels)
    while True:
        # TODO: Implement falling snow effect here
        time.sleep(0.02)  # With no delay between loops, the visualizer will crash
        if time.time() - start > time_limit * 60:
            break
