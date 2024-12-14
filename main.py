import argparse
import random
import subprocess
import time

import board
import neopixel

from led_matrix import LEDMatrix

NUM_LIGHTS = 150
DATA_PIN = board.D18
MAX = 255
TIME_LIMIT = 0.5
COLORS = {"red": (0, MAX // 4, 0), "blue": (0, 0, MAX // 4), "green": (MAX // 4, 0, 0)}
PATTERNS = [
    # "strobe",
    "matrix_demo",
    "mono_rainbow",
    "rainbow",
    "carnival",
    "chrimbus",
    "candy_cane",
    "random_p",
    # "white",
    "twinkly_snow",
    "rg_chase",
    "constipated",
    # "mexico"
]


def get_cpu_temperature():
    temp = subprocess.check_output(["vcgencmd", "measure_temp"]).decode("utf-8")
    return float(temp.split("=")[1].split("'")[0])


def rotate(l, reverse=False):
    if reverse:
        return l[1:] + l[:1]
    return l[-1:] + l[:-1]


class Color:
    def __init__(self):
        self.green = MAX
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
        elif self.next_color_value == MAX:
            setattr(self, self.current_color, self.current_color_value - 1)
        return (self.green, self.red, self.blue)


def linspace(start, stop, num=NUM_LIGHTS):
    if num < 2:
        return [start] if num == 1 else []
    step = (stop - start) / (num - 1)
    return [int(start + step) * i for i in range(num)]


def strobe():
    start = time.time()
    with neopixel.NeoPixel(DATA_PIN, NUM_LIGHTS) as pixels:
        pixels.fill(COLORS["green"])
        while True:
            for color in COLORS.values():
                for i, _ in enumerate(pixels):
                    pixels[i] = color
                    time.sleep(0.03)
            elapsed = time.time() - start
            if elapsed > TIME_LIMIT * 60:
                break


def rg_chase():
    start = time.time()
    with neopixel.NeoPixel(DATA_PIN, NUM_LIGHTS, auto_write=False) as pixels:
        pixels[:] = [
            COLORS["red"] if i % 20 < 10 else COLORS["green"]
            for i, _ in enumerate(pixels)
        ]
        while True:
            pixels[:] = rotate(pixels)
            pixels.show()
            time.sleep(0.03)
            elapsed = time.time() - start
            if elapsed > TIME_LIMIT * 60:
                break


def get_random_value(v):
    offset_choices = (1, 0, -1)
    return abs(v + random.choice(offset_choices)) % MAX


def randomly_shift_color(color):
    new_color = list(color[:])
    i = random.choice(range(len(color)))
    new_color[i] = (new_color[i] + random.choice((1, 0, -1))) % MAX
    return tuple(new_color)


def random_p():
    start = time.time()
    color = (0, 0, MAX)
    with neopixel.NeoPixel(DATA_PIN, NUM_LIGHTS) as pixels:
        while True:
            pixels[:] = list(map(randomly_shift_color, pixels))
            pixels.show()
            time.sleep(0.1)
            elapsed = time.time() - start
            if elapsed > TIME_LIMIT * 60:
                break


def rainbow():
    start = time.time()
    colors = [Color() for _ in range(NUM_LIGHTS)]
    for i, color in enumerate(colors):
        for j in range(i * 2):
            next(color)
    with neopixel.NeoPixel(DATA_PIN, NUM_LIGHTS, auto_write=False) as pixels:
        base_value = MAX - len(pixels)
        while True:
            pixels[:] = [next(c) for c in colors]
            pixels.show()
            elapsed = time.time() - start
            if elapsed > TIME_LIMIT * 60:
                break


def mono_rainbow():
    start = time.time()
    current_index = 2
    color = (0, 0, MAX)
    with neopixel.NeoPixel(DATA_PIN, NUM_LIGHTS) as pixels:
        while True:
            next_index = (current_index + 1) % len(color)
            while color[next_index] < MAX:
                color = tuple(
                    c + 1 if i == next_index else c for i, c in enumerate(color)
                )
                pixels.fill(color)
                time.sleep(0.01)
            while color[current_index] > 0:
                color = tuple(
                    c - 1 if i == current_index else c for i, c in enumerate(color)
                )
                pixels.fill(color)
                time.sleep(0.01)
            current_index = next_index
            elapsed = time.time() - start
            if elapsed > TIME_LIMIT * 60:
                break


def carnival():
    start = time.time()
    start_idx = 0
    NUM_COLORS = 13
    with neopixel.NeoPixel(DATA_PIN, NUM_LIGHTS, auto_write=False) as pixels:
        while True:
            for i in range(start_idx % NUM_COLORS, len(pixels), NUM_COLORS):
                pixels[i] = (0, 0, MAX)
            for i in range((start_idx + 1) % NUM_COLORS, len(pixels), NUM_COLORS):
                pixels[i] = (MAX // 2, 0, MAX)
            for i in range((start_idx + 2) % NUM_COLORS, len(pixels), NUM_COLORS):
                pixels[i] = (MAX, 0, MAX)
            for i in range((start_idx + 3) % NUM_COLORS, len(pixels), NUM_COLORS):
                pixels[i] = (MAX, 0, 0)
            for i in range((start_idx + 4) % NUM_COLORS, len(pixels), NUM_COLORS):
                pixels[i] = (MAX, MAX // 2, 0)
            for i in range((start_idx + 5) % NUM_COLORS, len(pixels), NUM_COLORS):
                pixels[i] = (0, MAX, 0)
            for i in range((start_idx + 6) % NUM_COLORS, len(pixels), NUM_COLORS):
                pixels[i] = (0, MAX, MAX // 2)
            for i in range((start_idx + 7) % NUM_COLORS, len(pixels), NUM_COLORS):
                pixels[i] = (0, 0, MAX)
            for i in range((start_idx + 8) % NUM_COLORS, len(pixels), NUM_COLORS):
                pixels[i] = (MAX // 2, 0, MAX)
            for i in range((start_idx + 9) % NUM_COLORS, len(pixels), NUM_COLORS):
                pixels[i] = (MAX, 0, 0)
            for i in range((start_idx + 10) % NUM_COLORS, len(pixels), NUM_COLORS):
                pixels[i] = (MAX, MAX // 2, 0)
            for i in range((start_idx + 11) % NUM_COLORS, len(pixels), NUM_COLORS):
                pixels[i] = (0, MAX, 0)
            for i in range((start_idx + 12) % NUM_COLORS, len(pixels), NUM_COLORS):
                pixels[i] = (0, MAX, MAX // 2)
            pixels.show()
            time.sleep(0.5)
            start_idx += 1
            elapsed = time.time() - start
            if elapsed > TIME_LIMIT * 60:
                break


def candy_cane():
    start = time.time()
    red_first = True
    with neopixel.NeoPixel(DATA_PIN, NUM_LIGHTS, auto_write=False) as pixels:
        while True:
            pixels[red_first::2] = [(0, MAX, 0)] * (len(pixels) // 2)
            pixels[not red_first :: 2] = [(MAX - 100, MAX, MAX - 100)] * (
                len(pixels) // 2
            )
            pixels.show()
            red_first = not red_first
            time.sleep(1)
            elapsed = time.time() - start
            if elapsed > TIME_LIMIT * 60:
                break


def chrimbus():
    start = time.time()
    red_first = True
    with neopixel.NeoPixel(DATA_PIN, NUM_LIGHTS, auto_write=False) as pixels:
        while True:
            pixels[red_first::2] = [COLORS["red"]] * (len(pixels) // 2)
            pixels[not red_first :: 2] = [COLORS["green"]] * (len(pixels) // 2)
            pixels.show()
            red_first = not red_first
            time.sleep(1)
            elapsed = time.time() - start
            if elapsed > TIME_LIMIT * 60:
                break


def white(intensity=1):
    if intensity < 0 or intensity > 1:
        raise ValueError("Provide intensity in [0, 1]")
    start = time.time()
    value = int(MAX * intensity)
    with neopixel.NeoPixel(DATA_PIN, NUM_LIGHTS, auto_write=False) as pixels:
        while True:
            pixels[:] = [(value, value, value)] * len(pixels)
            pixels.show()
            elapsed = time.time() - start
            if elapsed > TIME_LIMIT * 60:
                break


def twinkly_snow():
    start = time.time()
    white = (MAX, MAX, MAX)
    light_blue = (MAX - 150, MAX - 150, MAX)
    with neopixel.NeoPixel(DATA_PIN, NUM_LIGHTS, auto_write=False) as pixels:
        while True:
            pixels[:] = [light_blue if random.random() > 0.2 else white for _ in pixels]
            pixels.show()
            time.sleep(0.2)
            elapsed = time.time() - start
            if elapsed > TIME_LIMIT * 60:
                break


def mexico():
    start = time.time()
    white = (MAX, MAX, MAX)
    blue = (0, 0, MAX)
    green = (MAX, 0, 0)
    red = (0, MAX, 0)

    def map_p():
        rv = random.random()
        if rv < 0.1:
            return green
        if rv < 0.2:
            return red
        return white

    with neopixel.NeoPixel(DATA_PIN, NUM_LIGHTS, auto_write=False) as pixels:
        while True:
            pixels[:] = [map_p() for _ in pixels]
            pixels.show()
            time.sleep(0.3)
            elapsed = time.time() - start
            if elapsed > TIME_LIMIT * 60:
                break


def constipated():
    start = time.time()
    movement_choices = [-3, -5, 3, 5, 8, 10]
    with neopixel.NeoPixel(DATA_PIN, NUM_LIGHTS, auto_write=False) as pixels:
        light_blue = (MAX - 150, MAX - 150, MAX)
        light_pink = (MAX - 100, MAX, MAX - 100)
        num_snakes = 2
        snake_len = 7
        pixels.fill(light_blue)
        pixels[:snake_len] = [light_pink] * snake_len
        halfway = len(pixels) // num_snakes
        pixels[halfway : halfway + snake_len] = [light_pink] * snake_len
        pixels.show()
        while True:
            next_move = random.choice(movement_choices)
            for _ in range(abs(next_move)):
                pixels[:] = rotate(pixels, reverse=next_move < 0)
                pixels.show()
                time.sleep(0.03)
            elapsed = time.time() - start
            if elapsed > TIME_LIMIT * 60:
                break


def matrix_demo():
    with neopixel.NeoPixel(DATA_PIN, NUM_LIGHTS, auto_write=False) as pixels:
        matrix = LEDMatrix(
            pixels=pixels,
        )
        for i in range(100):
            matrix.set_pixel(i / 100, 0, (255, 0, 0))
            matrix.show()
            time.sleep(0.1)


def parade():
    while True:
        for pattern in PATTERNS:
            print(f"displaying {pattern}...")
            temperature = get_cpu_temperature()
            print(f"internal temperature: {temperature}'C")
            if temperature > 70:
                print("internal temperature too high. shutting down...")
                exit()
            eval(f"{pattern}()")


def diagnostic():
    time.sleep(3)
    with neopixel.NeoPixel(DATA_PIN, NUM_LIGHTS, auto_write=False) as pixels:
        for i, _ in enumerate(pixels):
            pixels.fill((0, 0, 0))
            pixels[i] = (MAX, MAX, MAX)
            pixels.show()
            time.sleep(0.5)


def clear():
    with neopixel.NeoPixel(DATA_PIN, NUM_LIGHTS, auto_write=False) as pixels:
        pixels.fill((0, 0, 0))
        pixels.show()


if __name__ == "main":
    parser = argparse.ArgumentParser(prog="Christmas Lights")
    parser.add_argument(
        "-p", "--pattern", choices=PATTERNS + ["parade"], default="white"
    )
    parser.add_argument("-c", "--clear", action="store_true")
    parser.add_argument("-d", "--diagnostic", action="store_true")
    args = parser.parse_args()
    if args.clear:
        clear()
    if args.diagnostic:
        diagnostic()
    else:
        eval(f"{args.pattern}()")
