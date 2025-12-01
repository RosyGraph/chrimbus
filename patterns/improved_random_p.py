import random
import time

from constants import MAX_COLOR_VAL, TIME_LIMIT
from with_neopixel import with_neopixel


def randomly_shift_color(color):
    new_color = list(color[:])
    i = random.choice(range(len(color)))
    new_color[i] = max(0, min(new_color[i] + random.choice((0, 0, 0, -1, 1)), MAX_COLOR_VAL))
    return tuple(new_color)


@with_neopixel
def improved_random_p(pixels, time_limit=TIME_LIMIT):
    num_pixels = len(pixels)
    min_n = num_pixels // 3
    max_n = min_n * 2
    start = time.time()
    while True:
        n = random.randint(min_n, max_n)
        indices_to_perm = random.sample(list(range(num_pixels)), n)
        for i in indices_to_perm:
            pixels[i] = randomly_shift_color(pixels[i])
        pixels.show()
        time.sleep(0.1)
        elapsed = time.time() - start
        if elapsed > time_limit * 60:
            break
