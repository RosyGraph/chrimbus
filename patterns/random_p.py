import random
import time

from constants import MAX_COLOR_VAL, TIME_LIMIT
from with_neopixel import with_neopixel


def randomly_shift_color(color):
    new_color = list(color[:])
    i = random.choice(range(len(color)))
    new_color[i] = (new_color[i] + random.choice((1, 0, -1))) % MAX_COLOR_VAL
    return tuple(new_color)


@with_neopixel
def random_p(time_limit=TIME_LIMIT):
    start = time.time()
    while True:
        pixels[:] = list(map(randomly_shift_color, pixels))
        pixels.show()
        time.sleep(0.1)
        elapsed = time.time() - start
        if elapsed > time_limit * 60:
            break
