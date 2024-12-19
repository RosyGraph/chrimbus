import random
import time

import neopixel

from constants import DATA_PIN, MAX_COLOR_VAL, NUM_LIGHTS, TIME_LIMIT
from math_helpers import rotate


def constipated(time_limit=TIME_LIMIT):
    start = time.time()
    movement_choices = [-3, -5, 3, 5, 8, 10]
    with neopixel.NeoPixel(DATA_PIN, NUM_LIGHTS, auto_write=False) as pixels:
        light_blue = (MAX_COLOR_VAL - 150, MAX_COLOR_VAL - 150, MAX_COLOR_VAL)
        light_pink = (MAX_COLOR_VAL - 100, MAX_COLOR_VAL, MAX_COLOR_VAL - 100)
        num_snakes = 2
        snake_len = 7
        pixels.fill(light_blue)
        pixels[:snake_len] = [light_pink] * snake_len
        halfway = len(pixels) // num_snakes
        pixels[halfway : halfway + snake_len] = [light_pink] * snake_len
        pixels.show()
        while True:
            next_move = random.choice(movement_choices)
            for _ in range(abs(next_move)):
                pixels[:] = rotate(pixels, reverse=next_move < 0)
                pixels.show()
                time.sleep(0.03)
            elapsed = time.time() - start
            if elapsed > time_limit * 60:
                break
