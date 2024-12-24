import time
from constants import TIME_LIMIT, MAX_COLOR_VAL
from led_matrix import LEDMatrix
from with_neopixel import with_neopixel

@with_neopixel
def static_drumstick(pixels, time_limit=TIME_LIMIT):
    matrix = LEDMatrix(pixels=pixels)
    # Initialize all LEDs to off
    pixels.fill((0, 0, 0))

    def is_on_outline(x, y):
        # Define drumstick shape
        # Main meat part
        if abs(x - 0.7) < 0.2 and abs(y - 0.6) < 0.15:
            return True
        # Bone part
        if 0.2 <= x <= 0.5 and abs(y - 0.5) < 0.05:
            return True
        return False

    # Set pixels for drumstick outline
    for i, (x, y) in matrix.mapping.items():
        if is_on_outline(x, y):
            # Golden brown color (GRB format)
            pixels[i] = (180, 140, 60)  # G, R, B
        else:
            pixels[i] = (0, 0, 0)

    pixels.show()
    
    start = time.time()
    while True:
        elapsed = time.time() - start
        if elapsed > time_limit * 60:
            break
        time.sleep(0.1)  # Small delay to prevent busy waiting
