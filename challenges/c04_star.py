"""
-- Challenge 04: Star  --

The reindeer night-vision goggles have recently been upgraded to version 7.18 after the unfortunate accident involving an F-117A Nighthawk and a weather balloon during this year's Flight Agility Readiness Trial.
The goggles must be recalibrated against a high-contrast celestial reference point.

Illuminate the pixels in the shape of a bright star at the center of the display.
Precision matters; an indistinct blob will result in poor flight performance.

When the star is cut from light and hangs true in the darkness, the long winter sky will welcome the sleigh once more.
"""

import math
import numpy as np
import time

from constants import MAX_COLOR_VAL, TIME_LIMIT
from led_matrix import LEDMatrix
from with_neopixel import with_neopixel


def is_in_star(x: int, y: int):
    """
    TODO: implement
    """
    return False


@with_neopixel
def star(pixels, time_limit=TIME_LIMIT):
    yellow = (MAX_COLOR_VAL, MAX_COLOR_VAL, 0)  # Colors are G, R, B in [0, 255]
    # Instantiate the matrix helper
    # Without it, we would have to deal with pixel indices directly
    colors = [
        (MAX_COLOR_VAL, 0, MAX_COLOR_VAL),
        (MAX_COLOR_VAL, MAX_COLOR_VAL, 0),
        (0, MAX_COLOR_VAL, 0),
        (0, MAX_COLOR_VAL, MAX_COLOR_VAL),
        (MAX_COLOR_VAL, MAX_COLOR_VAL, MAX_COLOR_VAL),
    ]
    matrix = LEDMatrix(pixels=pixels)
    start = time.time()
    rho = (1 / 10 * (5 - 5**0.5)) ** 0.5
    r = 0.5 * (1 / 5 * (5 - 2 * (5**0.5))) ** 0.5
    inflections = np.linspace(0, np.pi * 2, num=11)[:-1]
    points = [a for i, a in enumerate(inflections) if i % 2 == 0]
    valleys = [a for i, a in enumerate(inflections) if i % 2 == 1]
    points_with_wrap = points + [np.pi * 2]
    num_frames = 500
    offset_angles = list(np.linspace(0, np.pi * 2, num=num_frames))
    frame = 0
    while True:
        pixels[:] = [
            (0, 0, 0) for _ in pixels
        ]
        for i, (x, y) in matrix.mapping.items():
            x_s, y_s = x - 0.5, y - 0.5
            r_ = (x_s**2 + y_s**2) ** 0.5
            theta = (math.atan2(y_s, x_s) + offset_angles[frame]) % (math.pi * 2)
            for point_idx in range(len(points)):
                if (
                    theta >= points[point_idx]
                    and theta <= valleys[point_idx]
                    and r_
                    <= (r / math.cos(points[(point_idx + 1) % len(points)] - theta))
                ):
                    pixels[i] = (
                        MAX_COLOR_VAL,
                        MAX_COLOR_VAL,
                        50,
                    )
            for valley_idx in range(len(valleys)):
                if (
                    theta >= valleys[valley_idx % len(valleys)]
                    and theta
                    <= points_with_wrap[(valley_idx + 1) % len(points_with_wrap)]
                    and r_
                    <= (
                        r / math.cos(theta - points_with_wrap[valley_idx])
                    )  # this statement
                ):
                    pixels[i] = (
                        MAX_COLOR_VAL,
                        MAX_COLOR_VAL,
                        50,
                    )
        frame = (frame + 1) % num_frames
        pixels.show()
        time.sleep(0.1)
        elapsed = time.time() - start
        if elapsed >= time_limit * 60:
            return
