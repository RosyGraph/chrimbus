import json
from pathlib import Path

import av

import bitstring
import numpy as np

from constants import NUM_LIGHTS

def load_led_positions():
    try:
        with open("../corrected_led_mapping.json", "r") as f:
            mapping = json.load(f)

        positions = []
        for i in range(NUM_LIGHTS):
            if str(i) in mapping:
                positions.append(tuple(mapping[str(i)]))
            else:
                positions.append((-1, -1))

        return positions
    except Exception as e:
        print(f"Error loading LED positions: {e}")
        return [(-1, -1)] * NUM_LIGHTS

def get_region_color(frame, x, y, width, height, region_size=0.05):
    if x < 0 or y < 0 or x > 1 or y > 1:
        return (0, 0, 0)

    region_width = int(width * region_size)
    region_height = int(height * region_size)

    center_x = int(x * (width - 1))
    center_y = int(y * (height - 1))

    x_start = max(0, center_x - region_width // 2)
    x_end = min(width, center_x + region_width // 2)
    y_start = max(0, center_y - region_height // 2)
    y_end = min(height, center_y + region_height // 2)

    try:
        region = frame[y_start:y_end, x_start:x_end]
        mean_color = np.mean(region, axis=(0, 1))
        r, g, b = [min(255, int((val / 255.0) * 255)) for val in mean_color]
        return (g, r, b)
    except Exception as e:
        print(f"Error calculating region color: {e}")
        return (0, 0, 0)




def preprocess_video(video_path, output_path, led_positions=None):
    if led_positions is None:
        led_positions = load_led_positions()

    container = av.open(video_path)
    stream = container.streams.video[0]
    fps = float(stream.average_rate)

    frame_bits = bitstring.BitArray()

    try:
        frame_bits.append(bitstring.pack('floatle:32', fps))
        num_frames_pos = len(frame_bits)
        frame_bits.append(bitstring.pack('uintle:32', 0))
        frame_bits.append(bitstring.pack('uintle:16', NUM_LIGHTS))

        frame_count = 0
        previous_frame_colors = None

        for frame in container.decode(video=0):
            np_frame = frame.to_ndarray(format='rgb24')
            height, width = np_frame.shape[:2]

            current_frame_colors = []
            for x, y in led_positions:
                g, r, b = get_region_color(np_frame, x, y, width, height)
                current_frame_colors.append((g, r, b))

            if previous_frame_colors is None:
                for g, r, b in current_frame_colors:
                    frame_bits.append(bitstring.pack('uint:8', g))
                    frame_bits.append(bitstring.pack('uint:8', r))
                    frame_bits.append(bitstring.pack('uint:8', b))
            else:
                changes = []
                for i, (curr, prev) in enumerate(zip(current_frame_colors, previous_frame_colors)):
                    if curr != prev:
                        changes.append((i, curr))

                frame_bits.append(bitstring.pack('uint:8', len(changes)))

                for led_index, (g, r, b) in changes:
                    frame_bits.append(bitstring.pack('uint:8', led_index))
                    frame_bits.append(bitstring.pack('uint:8', g))
                    frame_bits.append(bitstring.pack('uint:8', r))
                    frame_bits.append(bitstring.pack('uint:8', b))

            previous_frame_colors = current_frame_colors
            frame_count += 1

        frame_bits[num_frames_pos:num_frames_pos + 32] = bitstring.pack('uintle:32', frame_count)

        with open(output_path, 'wb') as f:
            frame_bits.tofile(f)

        original_size = os.path.getsize(video_path)
        compressed_size = os.path.getsize(output_path)
        compression_ratio = original_size / compressed_size

        print(f"Processed {frame_count} frames at {fps} fps")
        print(f"Original size: {original_size / 1024:.2f}KB")
        print(f"Compressed size: {compressed_size / 1024:.2f}KB")
        print(f"Compression ratio: {compression_ratio:.2f}x")

    finally:
        container.close()


if __name__ == "__main__":
    import os

    project_root = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    video_path = project_root / "video_player" / "grinch.mp4"
    output_path = project_root / "video_player" / "grinch.led"

    print(f"Processing video from: {video_path}")
    print(f"Saving output to: {output_path}")

    preprocess_video(str(video_path), str(output_path))

