import time

from constants import DATA_PIN, MAX_COLOR_VAL, NUM_LIGHTS, TIME_LIMIT
from with_neopixel import with_neopixel


@with_neopixel
def carnival(pixels, time_limit=TIME_LIMIT):
    start = time.time()
    start_idx = 0
    NUM_COLORS = 13
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
