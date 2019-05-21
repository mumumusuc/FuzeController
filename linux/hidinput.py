#!/usr/bin/python3

import uinput
import sys
from evdev import ecodes


class Js(object):
    def __init__(self, value):
        self.value = value

    def get_value(self, code, attr):
        pass


class Button(Js):
    def get_value(self, code, attr):
        return 0


class Axes(Js):
    def get_value(self, code, attr):
        if code == ecodes.ABS_X:
            return self.value[0]
        if code == ecodes.ABS_Y:
            return self.value[1]
        if code == ecodes.ABS_RX:
            return self.value[2]
        if code == ecodes.ABS_RY:
            return self.value[3]
        if code == ecodes.ABS_Z:
            return self.value[4]
        if code == ecodes.ABS_RZ:
            return self.value[5]
        return 0


class Hat(Js):
    def get_value(self, code, attr):
        if self.value == 0x0:
            return 1 if code == ecodes.ABS_HAT0Y else 0
        if self.value == 0x1:
            return 1 if code == ecodes.ABS_HAT0X or code == ecodes.ABS_HAT0Y else 0
        if self.value == 0x2:
            return 1 if code == ecodes.ABS_HAT0X else 0
        if self.value == 0x3:
            return 1 if code == ecodes.ABS_HAT0X else -1 if code == ecodes.ABS_HAT0Y else 0
        if self.value == 0x4:
            return -1 if code == ecodes.ABS_HAT0Y else 0
        if self.value == 0x5:
            return -1 if code == ecodes.ABS_HAT0X or code == ecodes.ABS_HAT0Y else 0
        if self.value == 0x6:
            return -1 if code == ecodes.ABS_HAT0X else 0
        if self.value == 0x7:
            return -1 if code == ecodes.ABS_HAT0X else 1 if code == ecodes.ABS_HAT0Y else 0
        return 0


def parse_input_report(dev, input):
    buttons = Button(input[1] | (input[2] << 8))
    dev.emit_buttons(buttons)
    hat = Hat(input[3] & 0x0F)
    dev.emit_hats(hat)
    axes = Axes((input[4], input[5], input[6], input[7], input[8], input[9]))
    dev.emit_axes(axes)
    dev.emit()
    print(buttons.value, hat.value, axes.value)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.stderr.write('Need hidraw path.\n Usage :\n sudo python3 hidinput.py \"/dev/hidraw*\"\n')
        exit(-1)
    hid_path = sys.argv[1]
    with open(hid_path, 'rb') as hid_dev:
        print("open hidraw file : ", hid_path)
        udev = uinput.create_uinput_device("xpad")
        while True:
            buf = hid_dev.read(10)
            if buf[0] == 0x02:
                parse_input_report(udev, buf)
