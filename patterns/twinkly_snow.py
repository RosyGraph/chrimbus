import random
import time

from constants import MAX_COLOR_VAL, TIME_LIMIT
from with_neopixel import with_neopixel


@with_neopixel
def twinkly_snow(pixels, time_limit=TIME_LIMIT):
    start = time.time()
    white = (MAX_COLOR_VAL, MAX_COLOR_VAL, MAX_COLOR_VAL)
    light_blue = (MAX_COLOR_VAL - 150, MAX_COLOR_VAL - 150, MAX_COLOR_VAL)
    while True:
        pixels[:] = [light_blue if random.random() > 0.2 else white for _ in pixels]
        pixels.show()
        time.sleep(0.2)
        elapsed = time.time() - start
        if elapsed > time_limit * 60:
            break
