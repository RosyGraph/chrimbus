import time
import random
from constants import TIME_LIMIT, MAX_COLOR_VAL
from led_matrix import LEDMatrix
from with_neopixel import with_neopixel


@with_neopixel
def matrix_rain(pixels, time_limit=TIME_LIMIT):
    matrix = LEDMatrix(pixels=pixels)

    # Initialize all LEDs to off
    pixels.fill((0, 0, 0))
    pixels.show()

    class Drop:
        def __init__(self, x):
            self.x = x
            self.y = 0.0  # Start at bottom
            self.speed = random.uniform(0.2, 0.8)
            self.length = random.uniform(0.2, 0.4)  # Trail length
            self.brightness = random.uniform(0.5, 1.0)

    # Create initial drops
    drops = [Drop(random.random()) for _ in range(8)]

    start = time.time()

    while True:
        current_time = time.time()
        dt = 0.05  # Slower update rate for more visible movement

        # Update drops
        for drop in drops:
            # Move drop up
            drop.y += drop.speed * dt

            # Reset drop if it goes off screen
            if drop.y - drop.length > 1:
                drop.y = 0.0
                drop.x = random.random()  # New random x position
                drop.speed = random.uniform(0.2, 0.8)
                drop.brightness = random.uniform(0.5, 1.0)

        # Randomly add new drops
        if random.random() < 0.1 and len(drops) < 12:
            drops.append(Drop(random.random()))

        # Update LED colors
        for i, (x, y) in matrix.mapping.items():
            max_intensity = 0

            # Check each drop's contribution to this LED
            for drop in drops:
                # Calculate distance from drop head
                dist_to_head = y - drop.y

                # If LED is within drop's trail
                if (abs(x - drop.x) < 0.1 and  # Close enough horizontally
                        dist_to_head <= 0 and  # Below or at head
                        dist_to_head > -drop.length):  # Above tail

                    # Intensity falls off along the trail
                    intensity = (1 + dist_to_head / drop.length) * drop.brightness
                    max_intensity = max(max_intensity, intensity)

            # Set LED color (green with varying intensity)
            if max_intensity > 0:
                green = int(MAX_COLOR_VAL * max_intensity)
                # Add slight glow effect with dim white
                white = int(MAX_COLOR_VAL * max_intensity * 0.2)
                pixels[i] = (green, white, white)  # GRB format
            else:
                pixels[i] = (0, 0, 0)

        pixels.show()
        time.sleep(dt)

        elapsed = time.time() - start
        if elapsed > time_limit * 60:
            break