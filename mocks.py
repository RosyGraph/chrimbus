class MockPin:
    D18 = "D18"


class MockNeoPixel:
    """Mock implementation of NeoPixel that works for both direct use and context manager"""

    _instance = None

    def __new__(cls, pin, num_lights, auto_write=False):
        if cls._instance is None:
            cls._instance = super(MockNeoPixel, cls).__new__(cls)
            cls._instance.num_lights = num_lights
            cls._instance.auto_write = auto_write
            cls._instance._pixels = [(0, 0, 0)] * num_lights
            cls._instance._callback = None
        return cls._instance

    def __init__(self, pin, num_lights, auto_write=False):
        # These values are kept for reference but not reset due to singleton pattern
        self.num_lights = num_lights
        self.auto_write = auto_write

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.fill((0, 0, 0))
        self.show()

    def __len__(self):
        return self.num_lights

    def __setitem__(self, idx, color):
        if isinstance(idx, slice):
            start = idx.start if idx.start is not None else 0
            stop = idx.stop if idx.stop is not None else len(self)
            step = idx.step if idx.step is not None else 1

            if isinstance(color, list):
                for i, pos in enumerate(range(start, stop, step)):
                    if pos < len(self):
                        if len(color[min(i, len(color) - 1)]) == 3:
                            c = color[min(i, len(color) - 1)]
                            self._pixels[pos] = (c[0], c[1], c[2])
            else:
                for pos in range(start, stop, step):
                    if pos < len(self):
                        if len(color) == 3:
                            self._pixels[pos] = (color[0], color[1], color[2])
        else:
            if len(color) == 3:
                self._pixels[idx] = (color[0], color[1], color[2])

        if self.auto_write:
            self.show()

    def show(self):
        if self._callback:
            self._callback(self._pixels)

    def fill(self, color):
        if len(color) == 3:
            color = (color[0], color[1], color[2])  # Convert RGB to GRB
        self._pixels = [color] * self.num_lights
        if self.auto_write:
            self.show()


class MockNeoPixelModule:
    def NeoPixel(self, pin, num_lights, auto_write=False):
        return MockNeoPixel(pin, num_lights, auto_write)
