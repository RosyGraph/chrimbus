import argparse
import subprocess
import time

import neopixel

from constants import DATA_PIN, MAX_COLOR_VAL, NUM_LIGHTS, TIME_LIMIT
from pattern_definition import PATTERNS


def get_cpu_temperature():
    temp = subprocess.check_output(["vcgencmd", "measure_temp"]).decode("utf-8")
    return float(temp.split("=")[1].split("'")[0])


def parade(time_limit=TIME_LIMIT):
    while True:
        for pattern, fn in PATTERNS.items():
            print(f"displaying {pattern}...")
            temperature = get_cpu_temperature()
            print(f"internal temperature: {temperature}'C")
            if temperature > 70:
                print("internal temperature too high. shutting down...")
                exit()
            fn(time_limit=time_limit)


def diagnostic():
    time.sleep(3)
    with neopixel.NeoPixel(DATA_PIN, NUM_LIGHTS, auto_write=False) as pixels:
        for i, _ in enumerate(pixels):
            pixels.fill((0, 0, 0))
            pixels[i] = (MAX_COLOR_VAL, MAX_COLOR_VAL, MAX_COLOR_VAL)
            pixels.show()
            time.sleep(0.5)


def clear():
    with neopixel.NeoPixel(DATA_PIN, NUM_LIGHTS, auto_write=False) as pixels:
        pixels.fill((0, 0, 0))
        pixels.show()


if __name__ == "main":
    parser = argparse.ArgumentParser(prog="Christmas Lights")
    parser.add_argument(
        "-p", "--pattern", choices=list(PATTERNS) + ["parade"], default="white"
    )
    parser.add_argument("-c", "--clear", action="store_true")
    parser.add_argument("-d", "--diagnostic", action="store_true")
    parser.add_argument("-t", "--time", type=float, default=TIME_LIMIT)
    args = parser.parse_args()
    if args.clear:
        clear()
    if args.diagnostic:
        diagnostic()
    if args.pattern == "parade":
        parade(time_limit=args.time)
    else:
        PATTERNS[args.pattern](time_limit=args.time)
