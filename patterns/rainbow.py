import time

import neopixel

from constants import DATA_PIN, MAX_COLOR_VAL, NUM_LIGHTS, TIME_LIMIT


class Color:
    def __init__(self):
        self.green = MAX_COLOR_VAL
        self.red = 0
        self.blue = 0
        self.color_loop = ("green", "red", "blue")
        self.current_color_idx = 0

    @property
    def current_color(self):
        return self.color_loop[self.current_color_idx]

    @property
    def next_color(self):
        return self.color_loop[(self.current_color_idx + 1) % len(self.color_loop)]

    @property
    def current_color_value(self):
        return getattr(self, self.current_color)

    @property
    def next_color_value(self):
        return getattr(self, self.next_color)

    def __iter__(self):
        return self

    def __next__(self):
        if self.current_color_value == 0:
            self.current_color_idx = (self.current_color_idx + 1) % len(self.color_loop)
            setattr(self, self.next_color, 1)
        elif self.current_color_value > self.next_color_value:
            setattr(self, self.next_color, self.next_color_value + 1)
        elif self.next_color_value == MAX_COLOR_VAL:
            setattr(self, self.current_color, self.current_color_value - 1)
        return (self.green, self.red, self.blue)


def rainbow(time_limit=TIME_LIMIT):
    start = time.time()
    colors = [Color() for _ in range(NUM_LIGHTS)]
    for i, color in enumerate(colors):
        for j in range(i * 2):
            next(color)
    with neopixel.NeoPixel(DATA_PIN, NUM_LIGHTS, auto_write=False) as pixels:
        while True:
            pixels[:] = [next(c) for c in colors]
            pixels.show()
            elapsed = time.time() - start
            if elapsed > time_limit * 60:
                break
