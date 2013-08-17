#!/usr/bin/env python
import time
from smbus import SMBus

CMD_ENABLE_OUTPUT = 0x00
CMD_ENABLE_LEDS = 0x13
CMD_SET_PWM_VALUES = 0x01
CMD_UPDATE = 0x16
I2C_ADDR = 0x54

RED_1 = 0
RED_2 = 6
RED_3 = 17
ORANGE_1 = 1
ORANGE_2 = 7
ORANGE_3 = 16
YELLOW_1 = 2
YELLOW_2 = 8
YELLOW_3 = 15
GREEN_1 = 3
GREEN_2 = 5
GREEN_3 = 13
BLUE_1 = 4
BLUE_2 = 11
BLUE_3 = 14
WHITE_1 = 9
WHITE_2 = 10
WHITE_3 = 12

RING_RED = [RED_1, RED_2, RED_3]
RING_ORANGE = [ORANGE_1, ORANGE_2, ORANGE_3]
RING_YELLOW = [YELLOW_1, YELLOW_2, YELLOW_3]
RING_GREEN = [GREEN_1, GREEN_2, GREEN_3]
RING_BLUE = [BLUE_1, BLUE_2, BLUE_3]
RING_WHITE = [WHITE_1, WHITE_2, WHITE_3]

ARM_1 = [RED_1,ORANGE_1,YELLOW_1,GREEN_1,BLUE_1,WHITE_1]
ARM_2 = [RED_2,ORANGE_2,YELLOW_2,GREEN_2,BLUE_2,WHITE_2]
ARM_3 = [RED_3,ORANGE_3,YELLOW_3,GREEN_3,BLUE_3,WHITE_3]

DEFAULT_FADE_SPEED = 0.02
DEFAULT_FADE_STEP = 0x05
DEFAULT_INTENSITY = 0x50

class PyGlow:
    def __init__(self, i2c_bus=1):
        self.bus = SMBus(i2c_bus)
        self.current = self._zerolist()

    def init(self):
        self.write_i2c(CMD_ENABLE_OUTPUT, 0x01)
        self.write_i2c(CMD_ENABLE_LEDS, [0xFF, 0xFF, 0xFF])

    def write_i2c(self, reg, value):
        if not isinstance(value, list):
            value = [value]
        self.bus.write_i2c_block_data(I2C_ADDR, reg, value)

    def update_leds(self, values):
        self.write_i2c(CMD_SET_PWM_VALUES, values)
        self.write_i2c(CMD_UPDATE, 0xFF)

    def all_off(self):
        self.current = self._zerolist()
        self.update_leds(self.current)

    def light(self, leds, intensity=DEFAULT_INTENSITY):
        if not isinstance(leds, list):
            leds = [leds]
        self.current = [intensity if x in leds else 0x00 for x in range(18)]
        self.update_leds(self.current)

    def fade_in(self, leds, intensity=DEFAULT_INTENSITY,
                speed=DEFAULT_FADE_SPEED, step=DEFAULT_FADE_STEP):
        cur_inten = 0x00
        while cur_inten < intensity:
            self.light(leds, cur_inten)
            cur_inten += step
            if cur_inten >= 0xFF:
                break
            time.sleep(speed)

    def fade_out(self, leds, intensity=DEFAULT_INTENSITY,
                 speed=DEFAULT_FADE_SPEED, step=DEFAULT_FADE_STEP):
        while intensity > 0x00:
            self.light(leds, intensity)
            intensity -= step
            if intensity <= 0x00:
                break
            time.sleep(speed)

    def crossfade(self, leds_start, leds_end, intensity=DEFAULT_INTENSITY,
                     speed=DEFAULT_FADE_SPEED, step=DEFAULT_FADE_STEP):
        cur_inten_up = 0x00
        cur_inten_down = intensity
        while cur_inten_up < intensity:
            cur_inten_down -= step
            cur_inten_up += step
            if cur_inten_down <= 0x00:
                break
            if cur_inten_up >= 0xFF:
                break
            self.light(leds_start, cur_inten_down)
            self.light(leds_end, cur_inten_up)
            time.sleep(speed)

    def _zerolist(self):
        return [0x00 for x in range(18)]

if __name__ == '__main__':
    try:
        p = PyGlow()
        p.init()
        p.fade_in(GREEN_1, 0x80, 0.01)
        time.sleep(1)
        p.fade_out(GREEN_1, 0x80, 0.01)
        p.light(ARM_1)
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
    except KeyboardInterrupt:
        p.all_off()
