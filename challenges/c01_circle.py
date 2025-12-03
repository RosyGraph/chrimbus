"""
-- Challenge 01: Nose So Bright --

The Chrimbus reindeer handlers have discovered that Rudolf's famous nose has dimmed.
Without its brilliant glow, the reindeer cannot guide Santa's sleigh through the foggy night sky.
In order to restore its radiant shine, the elves require a perfect red circle projected onto the window grid.

Your task is to illuminate a circle centered on the display.
Use the pixel coordinates provided by LEDMatrix.

Once the circle is correctly displayed, the elves will be able to recalibrate Rudolf's nose, and the sleigh can take flight once more.
"""

import time

from constants import MAX_COLOR_VAL, TIME_LIMIT
from led_matrix import LEDMatrix
from with_neopixel import with_neopixel


def get_pixel_intensity(x: int, y: int):
    """
    Equation of a circle is (x - h)^2 + (y - k)^2 = r^2
    where (h, k) is the center and r is the radius.

    (x - h)^2 + (y - k)^2 <= 0.4^2
    (x - 0.5)^2 + (y - 0.5)^2 <= 0.4^2
    """
    h = 0.5
    k = 0.5
    r = 0.35
    lhs = (x - h) ** 2 + (y - k) ** 2
    if lhs > r**2:
        return (0, 0, 0)
    b = int((r**2 - lhs) * 2000)
    return (0, MAX_COLOR_VAL, b)


@with_neopixel
def circle(pixels, time_limit=TIME_LIMIT):
    """Shows a red circle for `time_limit` seconds"""
    # Instantiate the matrix helper
    # Without it, we would have to deal with pixel indices directly
    matrix = LEDMatrix(pixels=pixels)
    start = time.time()
    while True:
        for led_idx, (x, y) in matrix.mapping.items():
            pixels[led_idx] = get_pixel_intensity(x, y)
        pixels.show()
        time.sleep(1)
        if start - time.time() >= time_limit:
            break
