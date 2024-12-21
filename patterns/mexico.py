import random
import time

from constants import MAX_COLOR_VAL, TIME_LIMIT
from with_neopixel import with_neopixel


@with_neopixel
def mexico(pixels, time_limit=TIME_LIMIT):
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

    while True:
        pixels[:] = [map_p() for _ in pixels]
        pixels.show()
        time.sleep(0.3)
        elapsed = time.time() - start
        if elapsed > time_limit * 60:
            break
