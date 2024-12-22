import argparse
import subprocess
import time

from constants import MAX_COLOR_VAL, TIME_LIMIT
from pattern_definition import PATTERNS
from with_neopixel import with_neopixel


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


@with_neopixel
def diagnostic(pixels):
    time.sleep(3)
    for i, _ in enumerate(pixels):
        pixels.fill((0, 0, 0))
        pixels[i] = (MAX_COLOR_VAL, MAX_COLOR_VAL, MAX_COLOR_VAL)
        pixels.show()
        time.sleep(0.5)


@with_neopixel
def clear(pixels):
    pixels.fill((0, 0, 0))
    pixels.show()


if __name__ == "main":
    parser = argparse.ArgumentParser(prog="Christmas Lights")
    parser.add_argument(
        "-p", "--pattern", choices=list(PATTERNS) + ["parade"], default="chrimbus"
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
