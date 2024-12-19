import math
import time

import neopixel

from constants import DATA_PIN, MAX_COLOR_VAL, NUM_LIGHTS, TIME_LIMIT
from led_matrix import LEDMatrix


def rg_radial_gradient(time_limit=TIME_LIMIT):
    start = time.time()
    with neopixel.NeoPixel(DATA_PIN, NUM_LIGHTS, auto_write=False) as pixels:
        matrix = LEDMatrix(pixels=pixels)
        center = (matrix.width / 2, matrix.height / 2)
        r_max = math.sqrt((matrix.width / 2) ** 2 + (matrix.height / 2) ** 2)

        while True:
            for i, (x, y) in matrix.mapping.items():
                r = math.sqrt((x - center[0]) ** 2 + (y - center[1]) ** 2) / r_max
                time_offset = (time.time() * 0.5) % 1
                r_shifted = (r + time_offset) % 1
                red_intensity = int(MAX_COLOR_VAL * (1 - r_shifted))
                green_intensity = int(MAX_COLOR_VAL * r_shifted)
                pixels[i] = (green_intensity, red_intensity, 0)
            pixels.show()
            elapsed = time.time() - start
            if elapsed > time_limit * 60:
                break
