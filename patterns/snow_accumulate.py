import time
import random
from constants import TIME_LIMIT, MAX_COLOR_VAL
from led_matrix import LEDMatrix
from with_neopixel import with_neopixel


@with_neopixel
def snow_accumulate(pixels, time_limit=TIME_LIMIT):
    matrix = LEDMatrix(pixels=pixels)

    # Initialize all LEDs to off
    pixels.fill((0, 0, 0))
    pixels.show()

    class Flake:
        def __init__(self, x):
            self.x = x
            self.y = 0.0  # Start at bottom
            self.speed = random.uniform(0.2, 0.8)
            self.length = random.uniform(0.2, 0.4)  # Trail length
            self.brightness = random.uniform(0.5, 1.0)
            self.collided_time = 0.0

        @property
        def is_expired(self):
            if not self.collided_time:
                return False
            return time.time() - self.collided_time > 5.0

        @property
        def is_collided(self):
            return self.collided_time > 0.0

    # Create initial flakes
    flakes = []
    accumulated_leds = set()

    start = time.time()
    while True:
        dt = 0.005  # Slower update rate for more visible movement

        non_collided_flakes = [flake for flake in flakes if not flake.is_collided]
        # Randomly add new flakes if we have space
        if random.random() < 0.05 and len(non_collided_flakes) < 4:
            flakes.append(Flake(random.random()))

        # Update flakes
        active_flakes = []
        for flake in flakes:
            # Move flake down
            flake.y += flake.speed * dt

            if not flake.is_collided:
                # Find closest LED to flake head for collision detection
                closest_idx = None
                closest_dist = float("inf")
                for idx, (lx, ly) in matrix.mapping.items():
                    if abs(lx - flake.x) < 0.1:
                        dist = ((lx - flake.x) ** 2 + (ly - flake.y) ** 2) ** 0.5
                        if dist < closest_dist:
                            closest_dist = dist
                            closest_idx = idx

                hit_bottom = flake.y > 1.0
                hit_snow = closest_idx in accumulated_leds and closest_dist < 0.08
                if hit_bottom or hit_snow or flake.collided_time:
                    # Determine impact point
                    y_impact = flake.y if not hit_bottom else 1.0

                    # Use direct iteration to find the settle point
                    target_idx = find_settle_idx(
                        matrix, accumulated_leds, flake.x, y_impact
                    )
                    if target_idx is not None:
                        accumulated_leds.add(target_idx)

                    if not flake.collided_time:
                        flake.collided_time = time.time()

            if not flake.is_expired:
                active_flakes.append(flake)

        flakes = active_flakes

        # Update LED colors
        for i, (x, y) in matrix.mapping.items():
            if i in accumulated_leds:
                pixels[i] = (MAX_COLOR_VAL, MAX_COLOR_VAL, MAX_COLOR_VAL)
                continue

            max_intensity = 0

            # Check each flake's contribution to this LED
            for flake in flakes:
                # Calculate distance from flake head
                dist_to_head = y - flake.y

                # If LED is within flake's trail
                if (
                    abs(x - flake.x) < 0.08  # Close enough horizontally
                    and dist_to_head <= 0  # Below or at head
                    and dist_to_head > -flake.length
                ):  # Above tail
                    # Intensity falls off along the trail
                    intensity = (1 + dist_to_head / flake.length) * flake.brightness
                    max_intensity = max(max_intensity, intensity)

            # Set LED color (white with varying intensity)
            if max_intensity > 0:
                white_val = int(MAX_COLOR_VAL * max_intensity)
                pixels[i] = (white_val, white_val, white_val)  # GRB format
            else:
                pixels[i] = (0, 0, 0)

        pixels.show()
        time.sleep(dt)

        # Clear accumulated if it gets too full (optional safety)
        if len(accumulated_leds) > len(matrix.mapping) * 0.9:
            accumulated_leds.clear()

        elapsed = time.time() - start
        if elapsed > time_limit * 60:
            break


def find_settle_idx(matrix, accumulated_leds, flake_x, y_impact):
    """Find the best LED to accumulate at by direct iteration."""
    epsilon = 0.1

    # Phase 1: Search for nearest available LED BELOW or AT the impact line
    target_idx = None
    min_dist = float("inf")
    for idx, (lx, ly) in matrix.mapping.items():
        if idx not in accumulated_leds and ly >= y_impact - epsilon:
            dist = ((lx - flake_x) ** 2 + (ly - y_impact) ** 2) ** 0.5
            if dist < min_dist:
                min_dist = dist
                target_idx = idx

    if target_idx is not None:
        return target_idx

    # Phase 2: Search for nearest available LED ABOVE the impact line
    min_dist = float("inf")
    for idx, (lx, ly) in matrix.mapping.items():
        if idx not in accumulated_leds and ly < y_impact - epsilon:
            dist = ((lx - flake_x) ** 2 + (ly - y_impact) ** 2) ** 0.5
            if dist < min_dist:
                min_dist = dist
                target_idx = idx

    return target_idx
