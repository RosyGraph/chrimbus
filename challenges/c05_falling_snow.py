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

_STEP_SIZE = 0.01


class Snowflake:
    def __init__(self):
        self.x = random.random()
        self.y = 0

    def fall(self):
        self.y += _STEP_SIZE


def fade(g: int, r: int, b: int, decay=8):
    return (max(g - decay, 0), max(r - decay, 0), max(b - decay, 0))


@with_neopixel
def falling_snow(pixels, time_limit=TIME_LIMIT):
    start = time.time()
    matrix = LEDMatrix(pixels=pixels)
    initial_num_flakes = 5
    flakes = [Snowflake() for _ in range(initial_num_flakes)]
    while True:
        to_remove = set()
        pixels[:] = [fade(g, r, b) for (g, r, b) in pixels]
        for i, flake in enumerate(flakes):
            flake.fall()
            matrix.set_pixel(
                flake.x, flake.y, (MAX_COLOR_VAL, MAX_COLOR_VAL, MAX_COLOR_VAL)
            )
            if flake.y >= 1:
                to_remove.add(i)
        pixels.show()
        flakes = [f for i, f in enumerate(flakes) if i not in to_remove]
        if random.random() > 0.65:
            flakes.append(Snowflake())

        time.sleep(0.06)  # With no delay between loops, the visualizer will crash
        if time.time() - start > time_limit * 60:
            break
