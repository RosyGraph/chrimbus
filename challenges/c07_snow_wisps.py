"""
-- Challenge 07: The Wandering Wind (Advanced) --

The previous forecast promising a gentle snowfall has been revised by the Yuletide Arctic Meteorological Society.
A swift wind is now expected to stir the precipitation into long, restless trails.
Without understanding its pattern, the sprites cannot maintain safe conditions for Chrimbus Eve's aerial navigation.

Your task is to simulate snowflakes tossed by shifting wind.
Snow should drift primarily downward, but with varying sideways motion that changes over time.
The effect should suggest gusts, calm pauses, and wandering currents.

When the snow dances in wild and wandering patterns, the sprites will learn to guide it, and the sky will once again be ready for the reindeer to fly.
"""

import random
import time

from constants import MAX_COLOR_VAL, TIME_LIMIT
from led_matrix import LEDMatrix
from with_neopixel import with_neopixel


@with_neopixel
def snow_wisps(pixels, time_limit=TIME_LIMIT):
    start = time.time()
    matrix = LEDMatrix(pixels=pixels)
    while True:
        # TODO: Implement
        time.sleep(0.02)  # With no delay between loops, the visualizer will crash
        if time.time() - start > time_limit * 60:
            break
