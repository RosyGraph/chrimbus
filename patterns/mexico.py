import random
import time

import neopixel

from constants import DATA_PIN, MAX_COLOR_VAL, NUM_LIGHTS, TIME_LIMIT


def mexico(time_limit=TIME_LIMIT):
    start = time.time()
    white = (MAX_COLOR_VAL, MAX_COLOR_VAL, MAX_COLOR_VAL)
    green = (MAX_COLOR_VAL, 0, 0)
    red = (0, MAX_COLOR_VAL, 0)

    def map_p():
        rv = random.random()
        if rv < 0.1:
            return green
        if rv < 0.2:
            return red
        return white

    with neopixel.NeoPixel(DATA_PIN, NUM_LIGHTS, auto_write=False) as pixels:
        while True:
            pixels[:] = [map_p() for _ in pixels]
            pixels.show()
            time.sleep(0.3)
            elapsed = time.time() - start
            if elapsed > time_limit * 60:
                break
