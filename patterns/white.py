import time

from constants import MAX_COLOR_VAL, TIME_LIMIT
from with_neopixel import with_neopixel


@with_neopixel
def white(pixels, time_limit=TIME_LIMIT):
    start = time.time()
    value = int(MAX_COLOR_VAL)
    while True:
        pixels[:] = [(value, value, value)] * len(pixels)
        pixels.show()
        elapsed = time.time() - start
        if elapsed > time_limit * 60:
            break
