import time

import neopixel

from constants import DATA_PIN, NUM_LIGHTS, TIME_LIMIT


def strobe(time_limit=TIME_LIMIT):
    start = time.time()
    with neopixel.NeoPixel(DATA_PIN, NUM_LIGHTS) as pixels:
        pixels.fill(COLORS["green"])
        while True:
            for color in COLORS.values():
                for i, _ in enumerate(pixels):
                    pixels[i] = color
                    time.sleep(0.03)
            elapsed = time.time() - start
            if elapsed > time_limit * 60:
                break
