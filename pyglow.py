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
RED_3 = 12
ORANGE_1 = 1
ORANGE_2 = 7
ORANGE_3 = 13
YELLOW_1 = 2
YELLOW_2 = 8
YELLOW_3 = 14
GREEN_1 = 3
GREEN_2 = 9
GREEN_3 = 15
BLUE_1 = 4
BLUE_2 = 10
BLUE_3 = 16
WHITE_1 = 5
WHITE_2 = 11
WHITE_3 = 17

RING_RED = [RED_1, RED_2, RED_3]
RING_ORANGE = [ORANGE_1, ORANGE_2, ORANGE_3]
RING_YELLOW = [YELLOW_1, YELLOW_2, YELLOW_3]
RING_GREEN = [GREEN_1, GREEN_2, GREEN_3]
RING_BLUE = [BLUE_1, BLUE_2, BLUE_3]
RING_WHITE = [WHITE_1, WHITE_2, WHITE_3]

ARM_1 = [RED_1, ORANGE_1, YELLOW_1, GREEN_1, BLUE_1, WHITE_1]
ARM_2 = [RED_2, ORANGE_2, YELLOW_2, GREEN_2, BLUE_2, WHITE_2]
ARM_3 = [RED_3, ORANGE_3, YELLOW_3, GREEN_3, BLUE_3, WHITE_3]

LED_ADDRS = [ 0x01, 0x02, 0x03, 0x04, 0x0F, 0x0D,
              0x07, 0x08, 0x09, 0x06, 0x05, 0x0A,
              0x12, 0x11, 0x10, 0x0E, 0x0C, 0x0B ]

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
        self.all_off()

    def write_i2c(self, reg, value):
        if not isinstance(value, list):
            value = [value]
        self.bus.write_i2c_block_data(I2C_ADDR, reg, value)

    def update_leds(self, values):
        self.write_i2c(CMD_SET_PWM_VALUES, values)
        self.update()

    def update(self):
        self.bus.write_byte_data(I2C_ADDR, CMD_UPDATE, 0xFF)

    def set(self, leds, intensity=DEFAULT_INTENSITY):
        if not isinstance(leds, list):
            leds = [leds]
        for led in leds:
            self.bus.write_byte_data(I2C_ADDR, LED_ADDRS[led], intensity)

    def all_off(self):
        self.current = self._zerolist()
        self.update_leds(self.current)

    def turn_off(self, leds):
        self.set(leds, 0x00)
        self.update()

    def light(self, leds, intensity=DEFAULT_INTENSITY):
        if not isinstance(leds, list):
            leds = [leds]
        self.all_off()
        self.set(leds, intensity)
        self.update()

    def fade_in(self, leds, intensity=DEFAULT_INTENSITY,
                speed=DEFAULT_FADE_SPEED, step=DEFAULT_FADE_STEP):
        cur_inten = 0x00
        while cur_inten <= intensity:
            self.light(leds, cur_inten)
            cur_inten += step
            if cur_inten > 0xFF:
                break
            time.sleep(speed)

    def fade_out(self, leds, intensity=DEFAULT_INTENSITY,
                 speed=DEFAULT_FADE_SPEED, step=DEFAULT_FADE_STEP):
        while intensity >= 0x00:
            self.light(leds, intensity)
            intensity -= step
            if intensity < 0x00:
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
                self.turn_off(leds_start)
                break
            if cur_inten_up >= 0xFF:
                self.set(leds_end, 0xFF)
                self.update()
                break
            self.set(leds_start, cur_inten_down)
            self.set(leds_end, cur_inten_up)
            self.update()
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
        time.sleep(1)
        p.light([GREEN_1, RED_3, BLUE_2, ORANGE_1])
        time.sleep(1)
        p.light(ARM_1)
        time.sleep(0.3)
        p.light(ARM_1 + ARM_2)
        time.sleep(0.3)
        p.light(ARM_1 + ARM_2 + ARM_3)
        time.sleep(1)
        p.all_off()
        p.light(ARM_1)
        time.sleep(1)
        p.light(ARM_2)
        time.sleep(1)
        p.light(ARM_3)
        time.sleep(1)
        p.all_off()
        p.fade_in(RING_RED, 0xFF)
        p.crossfade(RING_RED, RING_ORANGE, 0x80)
        p.crossfade(RING_ORANGE, RING_YELLOW, 0x80)
        p.crossfade(RING_YELLOW, RING_GREEN, 0x80)
        p.crossfade(RING_GREEN, RING_BLUE, 0x80)
        p.crossfade(RING_BLUE, RING_WHITE, 0x80)
        p.fade_out(RING_WHITE, 0xFF)
        p.light(RING_GREEN, 0XFF)
        time.sleep(2)
        p.crossfade(RING_GREEN, RING_YELLOW, 0xFF, 0.005)
        p.crossfade(RING_YELLOW, RING_ORANGE, 0xFF, 0.005)
        p.crossfade(RING_ORANGE, RING_RED, 0xFF, 0.005)
        time.sleep(2)
        p.crossfade(RING_RED, RING_ORANGE, 0xFF, 0.005)
        p.crossfade(RING_ORANGE, RING_YELLOW, 0xFF, 0.005)
        p.crossfade(RING_YELLOW, RING_GREEN, 0xFF, 0.005)
        time.sleep(1)
        p.all_off()
    except KeyboardInterrupt:
        p.all_off()
