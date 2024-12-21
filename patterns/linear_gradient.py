import colorsys
import time

from constants import MAX_COLOR_VAL, TIME_LIMIT
from led_matrix import LEDMatrix
from with_neopixel import with_neopixel


@with_neopixel
def linear_gradient(pixels, time_limit=TIME_LIMIT):
    start = time.time()
    matrix = LEDMatrix(pixels=pixels)
    while True:
        for i, (x, _) in matrix.mapping.items():
            hue = (x + time.time() * 0.5) % 1
            saturation = 1
            value = 1.0
            rgb = colorsys.hsv_to_rgb(hue, saturation, value)
            red, green, blue = [int(c * MAX_COLOR_VAL) for c in rgb]
            pixels[i] = (green, red, blue)
        pixels.show()
        elapsed = time.time() - start
        if elapsed > time_limit * 60:
            break
