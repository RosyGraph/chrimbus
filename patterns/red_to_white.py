import math
import time

from constants import MAX_COLOR_VAL, TIME_LIMIT
from led_matrix import LEDMatrix
from with_neopixel import with_neopixel


@with_neopixel
def red_to_white(pixels, time_limit=TIME_LIMIT):
    start = time.time()
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
