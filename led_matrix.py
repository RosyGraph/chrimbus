import json


class LEDMatrix:
    def __init__(self, pixels, mapping=None, width=30, height=15):
        if mapping is None:
            with open("scaled_led_mapping_30x15.json") as f:
                self.mapping = json.load(f)
        else:
            self.mapping = mapping
        self.width = width
        self.height = height
        self.pixels = pixels

    def set_pixel(self, x, y, color):
        """Set the color of the LED closest to the given 2D position."""
        closest_idx = None
        closest_distance = float("inf")
        target = (x, y)

        for idx, coord in self.mapping.items():
            distance = (
                (coord[0] - target[0]) ** 2 + (coord[1] - target[1]) ** 2
            ) ** 0.5
            if distance < closest_distance:
                closest_distance = distance
                closest_idx = idx

        # Set the color for the closest LED
        if closest_idx is not None:
            self.pixels[int(closest_idx)] = color

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
