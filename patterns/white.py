import time

import neopixel

from constants import DATA_PIN, MAX_COLOR_VAL, NUM_LIGHTS, TIME_LIMIT


def white(intensity=1, time_limit=TIME_LIMIT):
    if intensity < 0 or intensity > 1:
        raise ValueError("Provide intensity in [0, 1]")
    start = time.time()
    value = int(MAX_COLOR_VAL * intensity)
    with neopixel.NeoPixel(DATA_PIN, NUM_LIGHTS, auto_write=False) as pixels:
        while True:
            pixels[:] = [(value, value, value)] * len(pixels)
            pixels.show()
            elapsed = time.time() - start
            if elapsed > time_limit * 60:
                break
