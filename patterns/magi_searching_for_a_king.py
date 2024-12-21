import time

from constants import MAX_COLOR_VAL, NUM_LIGHTS, TIME_LIMIT
from led_matrix import LEDMatrix
from with_neopixel import with_neopixel


@with_neopixel
def magi_searching_for_a_king(pixels, time_limit=TIME_LIMIT):
    start = time.time()
    purple = (MAX_COLOR_VAL, 0, MAX_COLOR_VAL)
    yellow = (MAX_COLOR_VAL, MAX_COLOR_VAL, 0)

    matrix = LEDMatrix(pixels=pixels)

    top_right_index = None
    min_dist = float("inf")
    for i, (x, y) in matrix.mapping.items():
        dist = ((x - 1.0) ** 2 + (y - 0.0) ** 2) ** 0.5
        if dist < min_dist:
            min_dist = dist
            top_right_index = i

    bottom_pixels = [(i, (x, y)) for i, (x, y) in matrix.mapping.items() if y > 0.9]
    bottom_pixels.sort(key=lambda p: p[1][0])

    magi_length = 3
    start_idx = 0
    total_bottom = len(bottom_pixels)

    while True:
        for i in range(NUM_LIGHTS):
            pixels[i] = purple

        """
        Matthew 2:2
        Where is he who has been born king of the Jews? For we saw his star when it rose and have come to worship
        him.
        """
        if top_right_index is not None:
            pixels[top_right_index] = yellow
        # Calculate the indices of the three Magi
        for offset in range(magi_length):
            idx = (start_idx + offset) % total_bottom
            magi_pixel_index = bottom_pixels[idx][0]
            pixels[magi_pixel_index] = yellow
        pixels.show()
        time.sleep(0.1)
        # Shift Magi
        start_idx = (start_idx + 1) % total_bottom
        elapsed = time.time() - start
        if elapsed > time_limit * 60:
            break
