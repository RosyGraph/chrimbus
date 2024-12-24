import bitstring
from with_neopixel import with_neopixel

@with_neopixel
def nightmare_video_pattern(pixels, time_limit=None):
    return video_pattern(pixels, time_limit, "./video_player/nightmare.led")


@with_neopixel
def grinch_video_pattern(pixels, time_limit=None):
    return video_pattern(pixels, time_limit, "./video_player/grinch.led")
  

@with_neopixel
def grinch_video_pattern(pixels, time_limit=None):
    return video_pattern(pixels, time_limit, "./video_player/grinch.led")
  

@with_neopixel
def up_video_pattern(pixels, time_limit=None):
    return video_pattern(pixels, time_limit, "./video_player/up.led")


@with_neopixel
def b_video_pattern(pixels, time_limit=None):
    return video_pattern(pixels, time_limit, "./video_player/b.led")


def video_pattern(pixels, time_limit=None, binary_path=None):
    import time

    try:
        bits = bitstring.BitArray(filename=binary_path)
        pos = 0

        # Read header
        fps = bits[pos:pos + 32].floatle
        pos += 32
        num_frames = bits[pos:pos + 32].uintle
        pos += 32
        num_leds = bits[pos:pos + 16].uintle
        pos += 16

        frame_delay = 1 / fps
        start_time = time.time()
        frame_count = 0

        current_colors = [(0, 0, 0)] * num_leds

        while True:
            data_pos = pos

            for i in range(num_leds):
                led_pos = data_pos + (i * 24)
                g = bits[led_pos:led_pos + 8].uint
                r = bits[led_pos + 8:led_pos + 16].uint
                b = bits[led_pos + 16:led_pos + 24].uint
                current_colors[i] = (g, r, b)
                pixels[i] = (g, r, b)

            pixels.show()
            data_pos += num_leds * 24

            for frame in range(1, num_frames):
                num_changes = bits[data_pos:data_pos + 8].uint
                data_pos += 8

                for _ in range(num_changes):
                    led_index = bits[data_pos:data_pos + 8].uint
                    data_pos += 8
                    g = bits[data_pos:data_pos + 8].uint
                    r = bits[data_pos + 8:data_pos + 16].uint
                    b = bits[data_pos + 16:data_pos + 24].uint
                    data_pos += 24

                    current_colors[led_index] = (g, r, b)
                    pixels[led_index] = (g, r, b)

                pixels.show()

                frame_count += 1
                elapsed = time.time() - start_time

                if time_limit and elapsed > time_limit * 60:
                    return

                current_frame_time = time.time() - start_time
                sleep_time = frame_delay * frame_count - current_frame_time
                if sleep_time > 0:
                    time.sleep(sleep_time)

            if time_limit:
                frame_count = 0

    except Exception as e:
        print(f"Error playing preprocessed video: {e}")
        import traceback
        traceback.print_exc()
