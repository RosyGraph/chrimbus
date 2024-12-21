import time

from constants import COLORS, TIME_LIMIT
from with_neopixel import with_neopixel


@with_neopixel
def strobe(pixels, time_limit=TIME_LIMIT):
    start = time.time()
    pixels.fill(COLORS["green"])
    while True:
        for color in COLORS.values():
            for i, _ in enumerate(pixels):
                pixels[i] = color
                time.sleep(0.03)
        elapsed = time.time() - start
        if elapsed > time_limit * 60:
            break
