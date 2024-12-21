# Chrimbus

Chrimbus is a repository for controlling the grid of Christmas lights set up in my window. The lights are controlled by a Raspberry Pi using [neopixels](https://github.com/adafruit/Adafruit_NeoPixel). The lights are mapped to a 2D grid based on their physical location in the window.

...include movie here...

## Getting Started

Assuming you do not have a Raspberry Pi set up with lights in the same configuration as mine, you can test patterns using the `visualizer` Python module (thanks to @joshua-lawrence). The visualizer module is programmed to display programs which are defined in `pattern_definition.py`. **If you wish to test your pattern using the visualizer, ensure your pattern is imported and listed in the `PATTERNS` dict**.

## Contributing

In order to control the lights, the neopixels library must be installed in the system python of the Raspberry Pi. For this reason, this project supports **only Python 3.7**. Please ensure your submitted patterns are compatible with this version.

Please do not include any patterns which are offensive or otherwise inappropriate as the lights are displayed publicly.

To submit a pattern, simply fork this repository and open a pull request. Your pattern should live in the `patterns/` directory.

## Pattern Authoring

There are many example patterns in the `patterns/` directory. You should model your pattern after these examples. Namely, the pattern should use the `@with_pixels` decorator to ensure compatibility with the visualizer.

### Setting pixel colors using indexing and slicing

Using the `@with_pixels` decorator allows you to set the color of each light (or pixel). The simplest example is `white.py`.

```python
@with_neopixel
def white(pixels, time_limit=TIME_LIMIT):
    start = time.time()
    value = int(MAX_COLOR_VAL)
    while True:
        pixels[:] = [(value, value, value)] * len(pixels)
        pixels.show()
        elapsed = time.time() - start
        if elapsed > time_limit * 60:
            break
```

Two subtle details are of note.

- Though we set each pixel, we do _not_ reassign the `pixels` variable. Rather, we reassign the slice of the `pixels` list.
- The tuple `(value, value, value)` is a tuple of three integers corresponding to (green, red, blue) values. **The tuples are NOT RGB; they are GRB.**

Setting individul pixels is also possible.

```python
from with_neopixel import with_neopixel


@with_neopixel
def strobe(pixels, time_limit=TIME_LIMIT):
    start = time.time()
    pixels.fill(COLORS["green"])
    while True:
        for color in COLORS.values():
            for i, _ in enumerate(pixels):
                pixels[i] = color
                time.sleep(0.03)
        elapsed = time.time() - start
        if elapsed > time_limit * 60:
            break
```

### Using the LEDMatrix class

The LEDMatrix class is a convenience class for mapping the physical location of the lights to their index in the `pixels` list. The primary usage of this class involves its `.mapping` dictionary. This dictionary uses the key as the light index and the value as a tuple of the $(x, y)$ coordinates on the window.

```python
import colorsys
from led_matrix import LEDMatrix


@with_neopixel
def linear_gradient(pixels, time_limit=TIME_LIMIT):
    start = time.time()
    matrix = LEDMatrix(pixels=pixels)
    while True:
        for i, (x, _) in matrix.mapping.items():
            hue = (x + time.time() * 0.5) % 1
            saturation = 1
            value = 1.0
            rgb = colorsys.hsv_to_rgb(hue, saturation, value)
            red, green, blue = [int(c * MAX_COLOR_VAL) for c in rgb]
            pixels[i] = (green, red, blue)
        pixels.show()
        elapsed = time.time() - start
        if elapsed > time_limit * 60:
            break
```
