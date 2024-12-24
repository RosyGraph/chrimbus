import time
import random
from constants import TIME_LIMIT, MAX_COLOR_VAL
from led_matrix import LEDMatrix
from with_neopixel import with_neopixel


@with_neopixel
def dvd_bounce(pixels, time_limit=TIME_LIMIT):
    matrix = LEDMatrix(pixels=pixels)

    # Initialize position and velocity
    pos_x = 0.5  # Start in middle
    pos_y = 0.5
    vel_x = 0.3  # Velocity components
    vel_y = 0.2

    # Initialize color
    current_color = (MAX_COLOR_VAL, 0, 0)  # Start with red

    # Available colors (RGB)
    colors = [
        (MAX_COLOR_VAL, 0, 0),  # Red
        (0, MAX_COLOR_VAL, 0),  # Green
        (0, 0, MAX_COLOR_VAL),  # Blue
        (MAX_COLOR_VAL, MAX_COLOR_VAL, 0),  # Yellow
        (MAX_COLOR_VAL, 0, MAX_COLOR_VAL),  # Magenta
        (0, MAX_COLOR_VAL, MAX_COLOR_VAL),  # Cyan
    ]

    start = time.time()
    last_color_change = 0

    def get_new_color():
        new_color = random.choice(colors)
        while new_color == current_color:  # Ensure we get a different color
            new_color = random.choice(colors)
        return new_color

    while True:
        # Clear all pixels
        pixels.fill((0, 0, 0))

        # Update position
        pos_x += vel_x * 0.05  # Scale velocity for smoother movement
        pos_y += vel_y * 0.05

        # Check for bounces
        bounce_occurred = False
        if pos_x <= 0 or pos_x >= 1:
            vel_x = -vel_x
            bounce_occurred = True
        if pos_y <= 0 or pos_y >= 1:
            vel_y = -vel_y
            bounce_occurred = True

        # Keep position in bounds
        pos_x = max(0, min(1, pos_x))
        pos_y = max(0, min(1, pos_y))

        # Change color on bounce with a minimum time between changes
        current_time = time.time()
        if bounce_occurred and (current_time - last_color_change) > 0.5:
            current_color = get_new_color()
            last_color_change = current_time

        # Find the closest LED to current position and its neighbors
        closest_led = None
        min_dist = float('inf')
        neighbors = []

        for i, (x, y) in matrix.mapping.items():
            dist = ((x - pos_x) ** 2 + (y - pos_y) ** 2) ** 0.5
            if dist < min_dist:
                min_dist = dist
                closest_led = i
            if dist < 0.1:  # Add nearby LEDs for a larger "dot"
                neighbors.append((i, dist))

        # Light up the closest LED and its neighbors with intensity based on distance
        for i, dist in neighbors:
            intensity = 1 - (dist / 0.1)  # Linear falloff
            color = tuple(int(c * intensity) for c in current_color)
            pixels[i] = color

        # Always ensure the closest LED is at full brightness
        if closest_led is not None:
            pixels[closest_led] = current_color

        pixels.show()
        time.sleep(0.016)  # ~60fps

        elapsed = time.time() - start
        if elapsed > time_limit * 60:
            break