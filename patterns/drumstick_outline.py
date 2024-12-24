import time
import random
from constants import TIME_LIMIT, MAX_COLOR_VAL
from led_matrix import LEDMatrix
from with_neopixel import with_neopixel

@with_neopixel
def drumstick_outline(pixels, time_limit=TIME_LIMIT):
    matrix = LEDMatrix(pixels=pixels)
    # Initialize all LEDs to off
    pixels.fill((0, 0, 0))
    pixels.show()

    class LightPoint:
        def __init__(self, position):
            self.position = position  # Position along the outline (0 to 1)
            self.speed = random.uniform(0.2, 0.8)
            self.brightness = random.uniform(0.5, 1.0)

    def get_outline_point(t):
        """Returns (x, y) coordinates for a point on the drumstick outline"""
        if t < 0.3:  # Top curve of drumstick
            x = t * 3
            y = 0.7 + 0.3 * (1 - (x - 0.45) ** 2)
        elif t < 0.5:  # Right side of meat
            progress = (t - 0.3) / 0.2
            x = 0.9
            y = 0.85 - progress * 0.3
        elif t < 0.7:  # Bottom curve
            progress = (t - 0.5) / 0.2
            x = 0.9 - progress * 0.3
            y = 0.55 - 0.3 * (1 - (progress - 0.5) ** 2)
        elif t < 0.85:  # Bone section
            progress = (t - 0.7) / 0.15
            x = 0.6 - progress * 0.4
            y = 0.5
        else:  # Connection back to start
            progress = (t - 0.85) / 0.15
            x = 0.2 + progress * 0.1
            y = 0.5 + progress * 0.2
        return x, y

    # Create initial light points
    points = [LightPoint(random.random()) for _ in range(6)]
    start = time.time()

    while True:
        dt = 0.05  # Update rate

        # Update points
        for point in points:
            # Move point along outline
            point.position = (point.position + point.speed * dt) % 1.0
            
            # Randomly refresh properties
            if random.random() < 0.02:
                point.brightness = random.uniform(0.5, 1.0)

        # Randomly add new points
        if random.random() < 0.1 and len(points) < 8:
            points.append(LightPoint(random.random()))

        # Update LED colors
        for i, (x, y) in matrix.mapping.items():
            max_intensity = 0
            
            # Check each point's contribution to this LED
            for point in points:
                outline_x, outline_y = get_outline_point(point.position)
                
                # Calculate distance from LED to outline point
                dist = ((x - outline_x) ** 2 + (y - outline_y) ** 2) ** 0.5
                
                # If LED is close enough to the point
                if dist < 0.15:
                    intensity = (1 - dist / 0.15) * point.brightness
                    max_intensity = max(max_intensity, intensity)

            # Set LED color (golden brown with varying intensity)
            if max_intensity > 0:
                gold = int(MAX_COLOR_VAL * max_intensity)
                red = int(MAX_COLOR_VAL * max_intensity * 0.8)
                blue = int(MAX_COLOR_VAL * max_intensity * 0.2)
                pixels[i] = (gold, red, blue)  # GRB format
            else:
                pixels[i] = (0, 0, 0)

        pixels.show()
        time.sleep(dt)
        
        elapsed = time.time() - start
        if elapsed > time_limit * 60:
            break
