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

class PyGlow:
    def __init__(self, i2c_bus=1):
        self.bus = SMBus(i2c_bus)
        self.current = [0x00 for x in range(18)]

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
        self.update_leds([0x00 for x in range(18)])

    def light(self, leds, intensity=0x50):
        if not isinstance(leds, list):
            leds = [leds]
        self.current = [intensity if x in leds else 0x00 for x in range(18)]
        self.update_leds(self.current)

if __name__ == '__main__':
    try:
        p = PyGlow()
        p.init()
        p.light(BLUE_1)
        time.sleep(1)
        p.light(ARM_1)
        time.sleep(1)
        p.light(RING_RED, 0xFF)
        time.sleep(0.4)
        p.light(RING_ORANGE, 0x80)
        time.sleep(0.4)
        p.light(RING_YELLOW, 0x40)
        time.sleep(0.4)
        p.light(RING_GREEN, 0x10)
        time.sleep(1)
        p.all_off()
    except KeyboardInterrupt:
        p.all_off()
