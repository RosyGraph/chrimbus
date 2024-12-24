import colorsys
import random
import time

from constants import MAX_COLOR_VAL, TIME_LIMIT
from led_matrix import LEDMatrix
from with_neopixel import with_neopixel


def manhattan_distance_to_food(food_position, coords):
    x, y = coords
    return abs(x - food_position[0]) + abs(y - food_position[1])


def generate_color(snake_hue):
    sysc = colorsys.hsv_to_rgb(snake_hue, 1, 1)
    snake_color = [int(c * MAX_COLOR_VAL) for c in sysc]
    return snake_color


@with_neopixel
def snake(pixels, time_limit=TIME_LIMIT):
    start = time.time()
    resolution = 20
    domain = [i / resolution for i in range(resolution)]
    snake_len = 1
    snake_hue = 0
    food_hue = 0.5
    food_color = generate_color(food_hue)
    midpoint = resolution // 2
    initial_y = domain[midpoint]
    snake_head_coord = (domain[midpoint], initial_y)
    food_position = (domain[-1], domain[-1])
    matrix = LEDMatrix(pixels=pixels)
    while True:
        if snake_len > 5:
            snake_hue += 0.1
            snake_len = 1
            food_hue = (snake_hue + 0.5) % 1
            food_color = generate_color(food_hue)
        pixels.fill((0, 0, 0))
        # find the 4 closest LEDs to food
        closest_leds = sorted(
            [(i, (x, y)) for i, (x, y) in matrix.mapping.items()],
            key=lambda tup: manhattan_distance_to_food(food_position, tup[1]),
        )[:1]
        for i, _ in closest_leds:
            pixels[i] = food_color
        # draw the snake
        snake_leds = sorted(
            [(i, (x, y)) for i, (x, y) in matrix.mapping.items()],
            key=lambda tup: manhattan_distance_to_food(snake_head_coord, tup[1]),
        )[:snake_len]
        for i, coord in enumerate(snake_leds):
            led_idx, _ = coord
            pixels[led_idx] = generate_color(snake_hue=snake_hue + (i * 0.05))
        # move the snake
        x_dist = abs(snake_head_coord[0] - food_position[0])
        y_dist = abs(snake_head_coord[1] - food_position[1])
        total_dist = x_dist + y_dist
        if total_dist < 0.1:
            snake_len += 1
            while total_dist < 0.1:
                food_position = (random.choice(domain), random.choice(domain))
                x_dist = abs(snake_head_coord[0] - food_position[0])
                y_dist = abs(snake_head_coord[1] - food_position[1])
                total_dist = x_dist + y_dist
        if x_dist >= y_dist:
            sgn = 1 if snake_head_coord[0] < food_position[0] else -1
            snake_head_coord = (snake_head_coord[0] + sgn * 0.1, snake_head_coord[1])
        elif y_dist >= x_dist:
            sgn = 1 if snake_head_coord[1] < food_position[1] else -1
            snake_head_coord = (snake_head_coord[0], snake_head_coord[1] + sgn * 0.1)
        pixels.show()
        time.sleep(0.1)
        if time.time() - start > time_limit * 60:
            break
