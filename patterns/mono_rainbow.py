import time

from constants import MAX_COLOR_VAL, TIME_LIMIT
from with_neopixel import with_neopixel


@with_neopixel
def mono_rainbow(pixels, time_limit=TIME_LIMIT):
    start = time.time()
    current_index = 2
    color = (0, 0, MAX_COLOR_VAL)
    while True:
        next_index = (current_index + 1) % len(color)
        while color[next_index] < MAX_COLOR_VAL:
            color = tuple(c + 1 if i == next_index else c for i, c in enumerate(color))
            pixels.fill(color)
            time.sleep(0.01)
        while color[current_index] > 0:
            color = tuple(
                c - 1 if i == current_index else c for i, c in enumerate(color)
            )
            pixels.fill(color)
            time.sleep(0.01)
        current_index = next_index
        elapsed = time.time() - start
        if elapsed > time_limit * 60:
            break
