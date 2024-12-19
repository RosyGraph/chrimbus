import random
import time

import neopixel

from constants import DATA_PIN, MAX_COLOR_VAL, NUM_LIGHTS, TIME_LIMIT


def twinkly_snow(time_limit=TIME_LIMIT):
    start = time.time()
    white = (MAX_COLOR_VAL, MAX_COLOR_VAL, MAX_COLOR_VAL)
    light_blue = (MAX_COLOR_VAL - 150, MAX_COLOR_VAL - 150, MAX_COLOR_VAL)
    with neopixel.NeoPixel(DATA_PIN, NUM_LIGHTS, auto_write=False) as pixels:
        while True:
            pixels[:] = [light_blue if random.random() > 0.2 else white for _ in pixels]
            pixels.show()
            time.sleep(0.2)
            elapsed = time.time() - start
            if elapsed > time_limit * 60:
                break
