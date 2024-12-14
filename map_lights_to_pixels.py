import json
import os

import cv2

FRAME_DIR = "frames"  # Directory where extracted frames are stored
NUM_LIGHTS = 150  # Number of LEDs in your setup


def find_brightest_pixel(frame_path):
    """Find the brightest pixel in a given frame."""
    frame = cv2.imread(frame_path, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, _, _, max_loc = cv2.minMaxLoc(gray)  # Get (x, y) of brightest pixel
    return max_loc


def map_leds():
    """Map LEDs to their 2D positions based on frame analysis."""
    mapping = {}
    for i in range(NUM_LIGHTS):
        frame_path = os.path.join(FRAME_DIR, f"frame{i:03d}.png")
        if not os.path.exists(frame_path):
            print(f"Frame {i} not found!")
            continue
        position = find_brightest_pixel(frame_path)
        mapping[i] = position
    return mapping


if __name__ == "__main__":
    led_mapping = map_leds()
    # Save the mapping to a file
    with open("led_mapping.json", "w") as f:
        json.dump(led_mapping, f)
    print("LED mapping saved to led_mapping.json")
