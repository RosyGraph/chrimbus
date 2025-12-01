import colorsys
import random
import time
from datetime import datetime

from constants import MAX_COLOR_VAL, TIME_LIMIT
from led_matrix import LEDMatrix
from with_neopixel import with_neopixel


def hue_to_rgb(hue):
    rgb = colorsys.hsv_to_rgb(hue, 1, 1)
    red, green, blue = [int(c * MAX_COLOR_VAL) for c in rgb]
    return (green, red, blue)


def euclidean_distance(x1, y1, x2, y2):
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5


@with_neopixel
def nye(pixels, time_limit=TIME_LIMIT):
    matrix = LEDMatrix(pixels=pixels)
    start = time.time()

    pixels.fill((0, 0, 0))
    while True:
        now = datetime.now()
        if now.hour != 0:
            if now.minute < 55:
                # sunrise
                for i, (x, y) in matrix.mapping.items():
                    if random.random() < 0.1:
                        pixels[i] = (MAX_COLOR_VAL, MAX_COLOR_VAL, 0)
                    else:
                        pixels[i] = (0, 0, 0)
                pixels.show()
                time.sleep(1)
            elif now.minute > 55:
                if now.minute < 59:
                    pixels.fill((MAX_COLOR_VAL, 0, 0))
                    pixels.show()
                    time.sleep(1)
                    pixels.fill((0, 0, 0))
                    pixels.show()
                    time.sleep(1)
                else:
                    if now.second < 50:
                        for i, (x, y) in matrix.mapping.items():
                            pixels[i] = (MAX_COLOR_VAL, MAX_COLOR_VAL, 0)
                            pixels.show()
                            time.sleep(0.1)
                    else:
                        y_coord = 1 - ((60 - now.second) / 10)
                        x_coord = 0.5
                        closest_leds = sorted(
                            [(i, (x, y)) for i, (x, y) in matrix.mapping.items()],
                            key=lambda tup: euclidean_distance(
                                x_coord, y_coord, *tup[1]
                            ),
                        )[:3]
                        for i, _ in closest_leds:
                            pixels[i] = (MAX_COLOR_VAL, MAX_COLOR_VAL, 0)
                        pixels.show()
                        time.sleep(0.1)
        else:
            for i, (x, y) in matrix.mapping.items():
                if random.random() < 0.1:
                    pixels[i] = (MAX_COLOR_VAL, MAX_COLOR_VAL, MAX_COLOR_VAL)
                else:
                    pixels[i] = (MAX_COLOR_VAL, MAX_COLOR_VAL, 0)
            pixels.show()
            time.sleep(0.1)
        elapsed = time.time() - start
        if elapsed > time_limit * 60:
            break
