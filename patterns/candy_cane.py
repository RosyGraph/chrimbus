import time

import neopixel

from constants import DATA_PIN, MAX_COLOR_VAL, NUM_LIGHTS, TIME_LIMIT


def candy_cane(time_limit=TIME_LIMIT):
    start = time.time()
    red_first = True
    with neopixel.NeoPixel(DATA_PIN, NUM_LIGHTS, auto_write=False) as pixels:
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
