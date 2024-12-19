import math
import time

import neopixel

from constants import DATA_PIN, MAX_COLOR_VAL, NUM_LIGHTS, TIME_LIMIT
from led_matrix import LEDMatrix


def red_to_white(time_limit=TIME_LIMIT):
    start = time.time()
    with neopixel.NeoPixel(DATA_PIN, NUM_LIGHTS, auto_write=False) as pixels:
        matrix = LEDMatrix(pixels=pixels)
        center = (matrix.width / 2, matrix.height / 2)
        r_max = math.sqrt((matrix.width / 2) ** 2 + (matrix.height / 2) ** 2)

        while True:
            for i, (x, y) in matrix.mapping.items():
                r = math.sqrt((x - center[0]) ** 2 + (y - center[1]) ** 2) / r_max
                time_factor = (math.sin(time.time()) + 1) / 2
                green_intensity = int(MAX_COLOR_VAL * r * time_factor)
                red_intensity = max(
                    MAX_COLOR_VAL // 2, int(MAX_COLOR_VAL * (1 - r) * time_factor)
                )
                blue_intensity = int(MAX_COLOR_VAL * r * time_factor)
                pixels[i] = (green_intensity, red_intensity, blue_intensity)
            pixels.show()
            time.sleep(0.01)

            elapsed = time.time() - start
            if elapsed > time_limit * 60:
                break
