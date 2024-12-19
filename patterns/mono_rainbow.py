import time

import neopixel

from constants import DATA_PIN, MAX_COLOR_VAL, NUM_LIGHTS, TIME_LIMIT


def mono_rainbow(time_limit=TIME_LIMIT):
    start = time.time()
    current_index = 2
    color = (0, 0, MAX_COLOR_VAL)
    with neopixel.NeoPixel(DATA_PIN, NUM_LIGHTS) as pixels:
        while True:
            next_index = (current_index + 1) % len(color)
            while color[next_index] < MAX_COLOR_VAL:
                color = tuple(
                    c + 1 if i == next_index else c for i, c in enumerate(color)
                )
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
