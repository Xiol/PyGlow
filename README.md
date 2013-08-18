PyGlow
======

Python class for the awesome Pimoroni PiGlow for the Raspberry Pi:

http://shop.pimoroni.com/products/piglow

Based on the helpful example from their repo:

https://github.com/pimoroni/piglow

See the bottom of `pyglow.py` for a usage example, but basically:

    # You'll want to import everything so you gain easy
    # access to the constants
    from pyglow import *
    import time

    p = PyGlow()   # Pass 0 if you have an old RPi
    p.init()
    p.light(RM_1)
    time.sleep(0.3)
    p.light(ARM_1 + ARM_2)
    time.sleep(0.3)
    p.light(ARM_1 + ARM_2 + ARM_3)
    time.sleep(1)
    p.all_off()
    p.fade_in(RING_RED, 0xFF)
    p.crossfade(RING_RED, RING_ORANGE, 0xFF)
    p.crossfade(RING_ORANGE, RING_YELLOW, 0xFF)
    p.crossfade(RING_YELLOW, RING_GREEN, 0xFF)
    p.fade_out(RING_GREEN, 0xFF)
    p.all_off()

`pyglow.py` contains other constants you can use to light up individual LEDs, rings of LEDs or an arm of the spiral. `.light()` takes a secondary argument for the intensity of the LED, e.g.

    p.light(RING_GREEN, 0xFF)  # Light up green ring at full brightness

You can fade in and out with `.fade_in()` and `.fade_out()`, e.g.:

    p.fade_in(RING_RED, 0xFF, 0.02, 0x05)

This will fade in the ring of red LEDs up to maximum brightness (0xFF) with a speed of 0x05 every 0.02 seconds. The intensity, speed and step are optional and defaults can be set by overriding `DEFAULT_FADE_SPEED`, `DEFAULT_FADE_STEP` and `DEFAULT_INTENSITY` (which also affects `.light()` if you don't pass an intensity to that!).

`.fade_out()` is the reverse - taking LED intensity down from the specified value to 0x00.

Crossfading will let you take a set of LEDs down from a specified intensity while bringing another set of LEDs up to the same intensity at the same time. You'll want to `.fade_in()` before using this:

    p.fade_in(RING_RED, 0xFF)
    p.crossfade(RING_RED, RING_YELLOW, 0xFF, 0.02, 0x05)
    p.fade_out(RING_YELLOW, 0xFF)

This will crossfade between the red and yellow rings to/from maximum intensity at 0x05 every 0.02 seconds. Intensity, speed and step are optional.
