import colorsys
import math
import time

from constants import MAX_COLOR_VAL, TIME_LIMIT
from led_matrix import LEDMatrix
from with_neopixel import with_neopixel


@with_neopixel
def radial_gradient(pixels, time_limit=TIME_LIMIT):
    start = time.time()
    matrix = LEDMatrix(pixels=pixels)
    center = (matrix.width / 2, matrix.height / 2)
    r_max = math.sqrt((matrix.width / 2) ** 2 + (matrix.height / 2) ** 2)

    while True:
        for i, (x, y) in matrix.mapping.items():
            r = math.sqrt((x - center[0]) ** 2 + (y - center[1]) ** 2) / r_max
            hue = (r + time.time() * 0.5) % 1
            saturation = 1
            value = 1.0
            rgb = colorsys.hsv_to_rgb(hue, saturation, value)
            red, green, blue = [int(c * MAX_COLOR_VAL) for c in rgb]
            pixels[i] = (green, red, blue)
        pixels.show()
        elapsed = time.time() - start
        time.sleep(0.02)
        if elapsed > time_limit * 60:
            break
