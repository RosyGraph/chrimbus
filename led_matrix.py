class LEDMatrix:
    def __init__(self, mapping, width, height, pixels):
        self.mapping = mapping  # A dictionary where keys are 1D indices and values are 2D (x, y) coordinates
        self.width = width
        self.height = height
        self.pixels = pixels

    def set_pixel(self, x, y, color):
        """Set the color of a specific LED based on its 2D position."""
        for idx, coord in self.mapping.items():
            print(f"idx: {idx}, coord: {coord}")
            if round(coord[0]) == x and round(coord[1]) == y:
                self.pixels[idx] = color
                break

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
