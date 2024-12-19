import time

import neopixel

from constants import COLORS, DATA_PIN, NUM_LIGHTS, TIME_LIMIT
from math_helpers import rotate


def rg_chase(time_limit=TIME_LIMIT):
    start = time.time()
    with neopixel.NeoPixel(DATA_PIN, NUM_LIGHTS, auto_write=False) as pixels:
        pixels[:] = [
            COLORS["red"] if i % 20 < 10 else COLORS["green"]
            for i, _ in enumerate(pixels)
        ]
        while True:
            pixels[:] = rotate(pixels)
            pixels.show()
            time.sleep(0.03)
            elapsed = time.time() - start
            if elapsed > time_limit * 60:
                break
