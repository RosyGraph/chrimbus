import json
import math


class LEDMatrix:
    def __init__(self, pixels, mapping=None, width=1.0, height=1.0):
        if mapping is None:
            with open("corrected_led_mapping.json") as f:
                self.mapping = {int(k): v for k, v in json.load(f).items()}
        else:
            self.mapping = mapping
        self.width = width
        self.height = height
        self.pixels = pixels

    def set_pixel(x, y, color):
        """Set the LED closest to the given physical position [x, y]."""
        closest_idx = None
        closest_distance = float("inf")

        for idx, (led_x, led_y) in self.mapping.items():
            distance = ((led_x - x) ** 2 + (led_y - y) ** 2) ** 0.5
            if distance < closest_distance:
                closest_distance = distance
                closest_idx = idx

        if closest_idx is not None:
            self.pixels[closest_idx] = color

    def fill(self, color):
        """Fill all LEDs with a single color."""
        self.pixels.fill(color)
        self.pixels.show()

    def clear(self):
        """Turn off all LEDs."""
        self.fill((0, 0, 0))

    def show(self):
        """Display the updated LED matrix."""
        self.pixels.show()

    def set_region(self, x1, y1, x2, y2, color):
        """Set a rectangular region of LEDs to a specific color."""
        for idx, (x, y) in self.mapping.items():
            if x1 <= round(x) <= x2 and y1 <= round(y) <= y2:
                self.pixels[idx] = color
        self.pixels.show()

    def wave_effect(self, time_step):
        for idx, (x, y) in self.mapping.items():
            intensity = int((math.sin(x / 100.0 + time_step) + 1) * 127.5)
            color = (intensity, 0, 255 - intensity)
            self.pixels[idx] = color
        self.pixels.show()
