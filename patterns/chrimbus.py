import time

from constants import COLORS, TIME_LIMIT
from with_neopixel import with_neopixel


@with_neopixel
def chrimbus(pixels, time_limit=TIME_LIMIT):
    start = time.time()
    red_first = True
    while True:
        pixels[red_first::2] = [COLORS["red"]] * (len(pixels) // 2)
        pixels[not red_first :: 2] = [COLORS["green"]] * (len(pixels) // 2)
        pixels.show()
        red_first = not red_first
        time.sleep(1)
        elapsed = time.time() - start
        if elapsed > time_limit * 60:
            break
