import time

import neopixel

from constants import DATA_PIN, MAX_COLOR_VAL, NUM_LIGHTS, TIME_LIMIT


def carnival(time_limit=TIME_LIMIT):
    start = time.time()
    start_idx = 0
    NUM_COLORS = 13
    with neopixel.NeoPixel(DATA_PIN, NUM_LIGHTS, auto_write=False) as pixels:
        while True:
            for i in range(start_idx % NUM_COLORS, len(pixels), NUM_COLORS):
                pixels[i] = (0, 0, MAX_COLOR_VAL)
            for i in range((start_idx + 1) % NUM_COLORS, len(pixels), NUM_COLORS):
                pixels[i] = (MAX_COLOR_VAL // 2, 0, MAX_COLOR_VAL)
            for i in range((start_idx + 2) % NUM_COLORS, len(pixels), NUM_COLORS):
                pixels[i] = (MAX_COLOR_VAL, 0, MAX_COLOR_VAL)
            for i in range((start_idx + 3) % NUM_COLORS, len(pixels), NUM_COLORS):
                pixels[i] = (MAX_COLOR_VAL, 0, 0)
            for i in range((start_idx + 4) % NUM_COLORS, len(pixels), NUM_COLORS):
                pixels[i] = (MAX_COLOR_VAL, MAX_COLOR_VAL // 2, 0)
            for i in range((start_idx + 5) % NUM_COLORS, len(pixels), NUM_COLORS):
                pixels[i] = (0, MAX_COLOR_VAL, 0)
            for i in range((start_idx + 6) % NUM_COLORS, len(pixels), NUM_COLORS):
                pixels[i] = (0, MAX_COLOR_VAL, MAX_COLOR_VAL // 2)
            for i in range((start_idx + 7) % NUM_COLORS, len(pixels), NUM_COLORS):
                pixels[i] = (0, 0, MAX_COLOR_VAL)
            for i in range((start_idx + 8) % NUM_COLORS, len(pixels), NUM_COLORS):
                pixels[i] = (MAX_COLOR_VAL // 2, 0, MAX_COLOR_VAL)
            for i in range((start_idx + 9) % NUM_COLORS, len(pixels), NUM_COLORS):
                pixels[i] = (MAX_COLOR_VAL, 0, 0)
            for i in range((start_idx + 10) % NUM_COLORS, len(pixels), NUM_COLORS):
                pixels[i] = (MAX_COLOR_VAL, MAX_COLOR_VAL // 2, 0)
            for i in range((start_idx + 11) % NUM_COLORS, len(pixels), NUM_COLORS):
                pixels[i] = (0, MAX_COLOR_VAL, 0)
            for i in range((start_idx + 12) % NUM_COLORS, len(pixels), NUM_COLORS):
                pixels[i] = (0, MAX_COLOR_VAL, MAX_COLOR_VAL // 2)
            pixels.show()
            time.sleep(0.5)
            start_idx += 1
            elapsed = time.time() - start
            if elapsed > time_limit * 60:
                break
