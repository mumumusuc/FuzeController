#!/usr/bin/python3

import os
import time
from evdev import UInput, UInputError, ecodes, util
from collections import namedtuple

_mappings = {}
absInfoUsesValue = hasattr(util, "resolve_ecodes_dict")
DEFAULT_AXIS_OPTIONS = (0, 0, 255, 0, 5)
UInputMapping = namedtuple("UInputMapping",
                           "name bustype vendor product version "
                           "axes axes_options buttons hats keys")


def create_mapping(name, description, bustype=0, vendor=0, product=0,
                   version=0, axes={}, axes_options={}, buttons={},
                   hats={}, keys={}):
    axes = {getattr(ecodes, k): v for k, v in axes.items()}
    axes_options = {getattr(ecodes, k): v for k, v in axes_options.items()}
    buttons = {getattr(ecodes, k): v for k, v in buttons.items()}
    hats = {getattr(ecodes, k): v for k, v in hats.items()}

    mapping = UInputMapping(description, bustype, vendor, product, version,
                            axes, axes_options, buttons, hats, keys)
    _mappings[name] = mapping


create_mapping(
    "xpad", "Microsoft X-Box 360 pad",
    # Bus type,      vendor, product, version
    ecodes.BUS_USB, 1118, 654, 272,
    # Axes
    {
        "ABS_X": "left_analog_x",
        "ABS_Y": "left_analog_y",
        "ABS_RX": "right_analog_x",
        "ABS_RY": "right_analog_y",
        "ABS_Z": "l2_analog",
        "ABS_RZ": "r2_analog"
    },
    # Axes settings
    {},
    # Buttons
    {
        "BTN_START": "button_options",
        "BTN_MODE": "button_ps",
        "BTN_SELECT": "button_share",
        "BTN_A": "button_cross",
        "BTN_B": "button_circle",
        "BTN_X": "button_square",
        "BTN_Y": "button_triangle",
        "BTN_TL": "button_l1",
        "BTN_TR": "button_r1",
        "BTN_THUMBL": "button_l3",
        "BTN_THUMBR": "button_r3"
    },
    # Hats
    {
        "ABS_HAT0X": ("dpad_left", "dpad_right"),
        "ABS_HAT0Y": ("dpad_up", "dpad_down")
    }
)


def next_joystick_device():
    for i in range(100):
        dev = "/dev/input/js{0}".format(i)
        if not os.path.exists(dev):
            return dev


def create_uinput_device(mapping):
    try:
        mapping = _mappings[mapping]
        device = UInputDevice(mapping)
    except UInputError as err:
        print(err)
    return device


class UInputDevice(object):
    def __init__(self, layout):
        self.js_dev = None
        self.device = None
        self.layout = None
        self._cache = {}
        self.create_device(layout)
        self.reset()

    def create_device(self, layout):
        events = {ecodes.EV_ABS: [], ecodes.EV_KEY: [], ecodes.EV_REL: []}
        if layout.axes or layout.buttons or layout.hats:
            self.js_dev = next_joystick_device()
        for name in layout.axes:
            params = layout.axes_options.get(name, DEFAULT_AXIS_OPTIONS)
            if not absInfoUsesValue:
                params = params[1:]
            events[ecodes.EV_ABS].append((name, params))
        for name in layout.buttons:
            events[ecodes.EV_KEY].append(name)
        for name in layout.hats:
            params = (0, -1, 1, 0, 0)
            if not absInfoUsesValue:
                params = params[1:]
            events[ecodes.EV_ABS].append((name, params))
        self.device = UInput(name=layout.name,
                             events=events,
                             bustype=layout.bustype,
                             vendor=layout.vendor,
                             product=layout.product,
                             version=layout.version)
        self.layout = layout
        print("create joystick [%s]@%s" % (self.device.name, self.js_dev))

    def write_event(self, ev_type, code, value):
        last_value = self._cache.get(code)
        if last_value != value:
            self.device.write(ev_type, code, value)
            self._cache[code] = value

    def reset(self):
        pass

    def emit_buttons(self, buttons):
        for code, attr in self.layout.buttons.items():
            value = buttons.get_value(code, attr)
            self.write_event(ecodes.EV_KEY, code, value)

    def emit_axes(self, axes):
        for code, attr in self.layout.axes.items():
            value = axes.get_value(code, attr)
            self.write_event(ecodes.EV_ABS, code, value)

    def emit_hats(self, hats):
        for code, attr in self.layout.hats.items():
            value = hats.get_value(code, attr)
            self.write_event(ecodes.EV_ABS, code, value)

    def emit(self):
        self.device.syn()


if __name__ == '__main__':
    test = {ecodes.ABS_HAT0X: 8}
    print('get value %s : ' % ecodes.ABS_HAT0X, test[ecodes.ABS_HAT0X])
    create_uinput_device("xpad")
    while True:
        time.sleep(1)
