import math
import time

from constants import MAX_COLOR_VAL, TIME_LIMIT
from led_matrix import LEDMatrix
from with_neopixel import with_neopixel


@with_neopixel
def rg_radial_gradient(pixels, time_limit=TIME_LIMIT):
    start = time.time()
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
