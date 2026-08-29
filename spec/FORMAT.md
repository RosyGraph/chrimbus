# Chrimbus Animation Format v1

A Chrimbus animation is a sequence of frames describing the state
of the 250-light display.

The structure and value constraints of an animation are defined by
[`animation.schema.json`](./animation.schema.json).

You can view a trivial, valid example in [`examples/basic.json`](./examples/basic.json).

## Pixels

Each frame contains 250 pixels. A pixel is represented as `[r, g, b]`, where
the three values represent red, green, and blue intensity respectively.
The lowest intensity is 0, and the highest intensity is 255.
Therefore, a pixel with `[0, 0, 0]` corresponds to an _unlit light_, while a
pixel with `[255, 255, 255]` corresponds to a _white light_.

Pixel position in the frame corresponds to the physical LED index in the
Chrimbus display.

## Playback

Frames are displayed sequentially at the rate specified by `fps`.
