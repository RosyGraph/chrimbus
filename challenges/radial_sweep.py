import random
import time

from constants import MAX_COLOR_VAL, TIME_LIMIT
from led_matrix import LEDMatrix
from with_neopixel import with_neopixel


@with_neopixel
def radial_sweep(pixels, time_limit=TIME_LIMIT):
    start = time.time()
    matrix = LEDMatrix(pixels=pixels)
    while True:
        # TODO: Implement radial sweep pattern here
        time.sleep(0.02)  # With no delay between loops, the visualizer will crash
        if time.time() - start > time_limit * 60:
            break
