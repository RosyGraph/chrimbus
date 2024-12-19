import argparse
import subprocess
import time

import neopixel

from constants import DATA_PIN, MAX_COLOR_VAL, NUM_LIGHTS, TIME_LIMIT
from patterns.blue_to_white import blue_to_white
from patterns.candy_cane import candy_cane
from patterns.carnival import carnival
from patterns.chrimbus import chrimbus
from patterns.constipated import constipated
from patterns.linear_gradient import linear_gradient
from patterns.magi_searching_for_a_king import magi_searching_for_a_king
from patterns.mono_rainbow import mono_rainbow
from patterns.pinwheel import pinwheel
from patterns.radial_gradient import radial_gradient
from patterns.rainbow import rainbow
from patterns.random_p import random_p
from patterns.red_to_white import red_to_white
from patterns.rg_chase import rg_chase
from patterns.rg_matrix import rg_matrix
from patterns.skewed_wave import skewed_wave
from patterns.twinkly_snow import twinkly_snow

PATTERNS = {
    "magi_seraching_for_a_king": magi_searching_for_a_king,
    "skewed_wave": skewed_wave,
    "red_to_white": red_to_white,
    "blue_to_white": blue_to_white,
    "linear_gradient": linear_gradient,
    "radial_gradient": radial_gradient,
    "pinwheel": pinwheel,
    "rg_matrix": rg_matrix,
    "mono_rainbow": mono_rainbow,
    "rainbow": rainbow,
    "carnival": carnival,
    "chrimbus": chrimbus,
    "candy_cane": candy_cane,
    "random_p": random_p,
    "twinkly_snow": twinkly_snow,
    "rg_chase": rg_chase,
    "constipated": constipated,
}


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
