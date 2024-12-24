import math
import time

from led_matrix import LEDMatrix
from with_neopixel import with_neopixel

# Constants
TIME_LIMIT = 5  # minutes
MAX_COLOR_VAL = 255

# Colors for the drumstick
DRUMSTICK_COLORS = {
    "cooked_skin": (150, 100, 50),  # Golden brown
    "highlight": (200, 150, 100),  # Light golden
    "shadow": (100, 50, 25),  # Dark brown
    "bone_end": (220, 220, 200),  # Off-white
}


@with_neopixel
def chicken_drumstick(pixels, time_limit=TIME_LIMIT):
    """
    Creates an animated chicken drumstick pattern using LED lights.
    The drumstick rotates slightly and has a "sizzling" effect.
    """
    start = time.time()
    matrix = LEDMatrix(pixels=pixels)

    # Find center of the display
    x_coords = [x for x, _ in matrix.mapping.values()]
    y_coords = [y for _, y in matrix.mapping.values()]
    center_x = (max(x_coords) + min(x_coords)) / 2
    center_y = (max(y_coords) + min(y_coords)) / 2

    while True:
        angle = time.time() * 0.5  # Slow rotation

        for i, (x, y) in matrix.mapping.items():
            # Calculate distance from center
            dx = x - center_x
            dy = y - center_y
            distance = math.sqrt(dx**2 + dy**2)

            # Create drumstick shape
            is_in_drumstick = False

            # Rotate coordinates
            rot_x = dx * math.cos(angle) - dy * math.sin(angle)
            rot_y = dx * math.sin(angle) + dy * math.cos(angle)

            # Define drumstick shape using rotated coordinates
            if (rot_x**2 / 4 + rot_y**2) < 3:  # Main body of drumstick
                is_in_drumstick = True
                color = DRUMSTICK_COLORS["cooked_skin"]

                # Add highlight effect
                if abs(rot_y) < 0.5 and rot_x > 0:
                    color = DRUMSTICK_COLORS["highlight"]

                # Add shadow effect
                if abs(rot_y) < 0.5 and rot_x < 0:
                    color = DRUMSTICK_COLORS["shadow"]

            # Bone end
            elif -2 < rot_x < -1 and abs(rot_y) < 0.5:
                is_in_drumstick = True
                color = DRUMSTICK_COLORS["bone_end"]

            # Add sizzling effect
            if is_in_drumstick:
                sizzle = math.sin(time.time() * 10 + distance * 5) * 20
                color = tuple(
                    min(max(c + int(sizzle), 0), MAX_COLOR_VAL) for c in color
                )
                pixels[i] = color
            else:
                pixels[i] = (0, 0, 0)  # Turn off pixels outside the drumstick

        pixels.show()
        time.sleep(0.03)

        elapsed = time.time() - start
        if elapsed > time_limit * 60:
            break
