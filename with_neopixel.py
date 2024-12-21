from functools import wraps

import neopixel

from constants import DATA_PIN, NUM_LIGHTS


def with_neopixel(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        with neopixel.NeoPixel(DATA_PIN, NUM_LIGHTS, auto_write=False) as pixels:
            return func(pixels, *args, **kwargs)

    return wrapper
