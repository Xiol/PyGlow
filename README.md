PyGlow
======

Python class for the awesome Pimoroni PiGlow for the Raspberry Pi:

http://shop.pimoroni.com/products/piglow

Based on the helpful example from their repo:

https://github.com/pimoroni/piglow

See the bottom of `pyglow.py` for a usage example, but basically:

    import pyglow
    import time

    p = pyglow.PyGlow()   # Pass 0 if you have an old RPi
    p.init()
    p.light(pyglow.RING_RED)
    time.sleep(2)
    p.all_off()

`pyglow.py` contains other constants you can use to light up individual LEDs, rings of LEDs or an arm of the spiral. `.light()` takes a secondary argument for the intensity of the, e.g.

   p.light(pyglow.RING_GREEN, 0xFF)  # Light up green ring at full brightness
