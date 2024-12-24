import random
import time

from constants import MAX_COLOR_VAL, TIME_LIMIT
from led_matrix import LEDMatrix
from with_neopixel import with_neopixel


@with_neopixel
def meteor(pixels, time_limit=TIME_LIMIT):
    matrix = LEDMatrix(pixels=pixels)

    # Initialize all LEDs to off
    pixels.fill((0, 0, 0))
    pixels.show()

    class Drop:
        def __init__(self, x):
            self.x = x
            self.y = 0.0  # Start at bottom
            self.speed = random.uniform(0.2, 0.8)
            self.length = random.uniform(0.4, 0.8)  # Trail length
            self.brightness = random.uniform(0.5, 1.0)

    # Create initial drops
    drops = [Drop(random.random()) for _ in range(8)]

    start = time.time()

    pixels.fill((0, 0, MAX_COLOR_VAL))
    while True:
        dt = 0.05  # Slower update rate for more visible movement

        # Update drops
        for drop in drops:
            # Move drop down and to the left
            drop.y += drop.speed * dt
            drop.x -= drop.speed * dt * 2

            # Reset drop if it goes off screen
            if drop.y - drop.length > 1:
                drop.y = 0.0
                drop.x = random.random() * 3  # New random x position
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
                if (
                    abs(x - drop.x * 2) < 0.1  # Close enough horizontally
                    and dist_to_head <= 0  # Below or at head
                    and dist_to_head > -drop.length
                ):  # Above tail
                    # Intensity falls off along the trail
                    intensity = (1 + dist_to_head / drop.length) * drop.brightness
                    max_intensity = max(max_intensity, intensity)

            # Set LED color (green with varying intensity)
            if max_intensity > 0:
                yellow = int(MAX_COLOR_VAL * max_intensity)
                # Add slight glow effect with dim white
                white = MAX_COLOR_VAL - yellow
                pixels[i] = (yellow, yellow, white)  # GRB format
            else:
                pixels[i] = (MAX_COLOR_VAL // 2, MAX_COLOR_VAL // 2, MAX_COLOR_VAL)

        pixels.show()
        time.sleep(dt)

        elapsed = time.time() - start
        if elapsed > time_limit * 60:
            break
