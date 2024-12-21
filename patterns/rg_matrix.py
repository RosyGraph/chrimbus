import time

from constants import COLORS, TIME_LIMIT
from led_matrix import LEDMatrix
from with_neopixel import with_neopixel


@with_neopixel
def rg_matrix(pixels, time_limit=TIME_LIMIT):
    start = time.time()
    delay = 2
    matrix = LEDMatrix(
        pixels=pixels,
    )
    while True:
        for y in range(4):
            matrix.set_region(0, y / 4, 1, (y + 1) / 4, COLORS["red"])
            matrix.show()
            time.sleep(delay)
        if time.time() - start > time_limit * 60:
            break
        for y in range(4):
            matrix.set_region(0, y / 4, 1, (y + 1) / 4, COLORS["green"])
            matrix.show()
            time.sleep(delay)
        if time.time() - start > time_limit * 60:
            break
        for x in range(4):
            matrix.set_region(x / 4, 0, (x + 1) / 4, 1, COLORS["red"])
            matrix.show()
            time.sleep(delay)
        if time.time() - start > time_limit * 60:
            break
        for x in range(4):
            matrix.set_region(x / 4, 0, (x + 1) / 4, 1, COLORS["green"])
            matrix.show()
            time.sleep(delay)
        if time.time() - start > time_limit * 60:
            break
        for x in range(4):
            matrix.set_region(x / 4, 0, (x + 1) / 4, 1, COLORS["red"])
            matrix.set_region(0, x / 4, 1, (x + 1) / 4, COLORS["red"])
            matrix.show()
            time.sleep(delay)
        if time.time() - start > time_limit * 60:
            break
        for y in range(4):
            matrix.set_region(y / 4, 0, (y + 1) / 4, 1, COLORS["green"])
            matrix.set_region(0, y / 4, 1, (y + 1) / 4, COLORS["green"])
            matrix.show()
            time.sleep(delay)
        if time.time() - start > time_limit * 60:
            break
