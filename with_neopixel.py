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
    """
    Decorator to provide a NeoPixel context to pattern functions.
    Uses a mock implementation if the NeoPixel library is unavailable.
    """

    def wrapper(*args, **kwargs):
        time_limit = kwargs.get("time_limit", TIME_LIMIT)
        num_lights = kwargs.get("num_lights", NUM_LIGHTS)
        auto_write = kwargs.get("auto_write", False)

        with neopixel.NeoPixel(D18, num_lights, auto_write) as pixels:
            return func(pixels, *args, **kwargs)

    return wrapper
