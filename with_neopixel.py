import sys
from unittest.mock import MagicMock

from constants import NUM_LIGHTS, TIME_LIMIT
from mocks import MockNeoPixelModule, MockPin

try:
    import neopixel
    from board import D18
except ImportError:
    mock_board = MagicMock()
    D18 = MockPin.D18
    sys.modules["board"] = mock_board

    neopixel = MockNeoPixelModule()


def with_neopixel(func):
    def wrapper(*args, **kwargs):
        time_limit = kwargs.get("time_limit", TIME_LIMIT)  # Default time_limit to 10 minutes
        num_lights = kwargs.get(
            "num_lights", NUM_LIGHTS
        )  # Use NUM_LIGHTS from constants
        auto_write = kwargs.get("auto_write", False)

        # Create the NeoPixel instance
        with neopixel.NeoPixel(D18, num_lights, auto_write=auto_write) as pixels:
            return func(pixels, *args, **kwargs)

    return wrapper
