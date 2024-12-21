import time

from constants import MAX_COLOR_VAL, TIME_LIMIT
from with_neopixel import with_neopixel


@with_neopixel
def candy_cane(pixels, time_limit=TIME_LIMIT):
    start = time.time()
    red_first = True
    while True:
        pixels[red_first::2] = [(0, MAX_COLOR_VAL, 0)] * (len(pixels) // 2)
        pixels[not red_first :: 2] = [
            (MAX_COLOR_VAL - 100, MAX_COLOR_VAL, MAX_COLOR_VAL - 100)
        ] * (len(pixels) // 2)
        pixels.show()
        red_first = not red_first
        time.sleep(1)
        elapsed = time.time() - start
        if elapsed > time_limit * 60:
            break
