import time

from constants import COLORS, TIME_LIMIT
from math_helpers import rotate
from with_neopixel import with_neopixel


@with_neopixel
def rg_chase(pixels, time_limit=TIME_LIMIT):
    start = time.time()
    pixels[:] = [
        COLORS["red"] if i % 20 < 10 else COLORS["green"] for i, _ in enumerate(pixels)
    ]
    while True:
        pixels[:] = rotate(pixels)
        pixels.show()
        time.sleep(0.03)
        elapsed = time.time() - start
        if elapsed > time_limit * 60:
            break
