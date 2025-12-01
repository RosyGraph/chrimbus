import random
import time

from constants import MAX_COLOR_VAL, TIME_LIMIT
from with_neopixel import with_neopixel



@with_neopixel
def solid_red(pixels, time_limit=TIME_LIMIT):
    pixels.fill((0, MAX_COLOR_VAL, 0))
    pixels.show()
    time.sleep(time_limit * 60)
