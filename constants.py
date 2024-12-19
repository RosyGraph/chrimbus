import board

NUM_LIGHTS = 150
DATA_PIN = board.D18
MAX_COLOR_VAL = 255
TIME_LIMIT = float("inf")

COLORS = {
    "red": (0, MAX_COLOR_VAL, 0),
    "blue": (0, 0, MAX_COLOR_VAL),
    "green": (MAX_COLOR_VAL, 0, 0),
}
