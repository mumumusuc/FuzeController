#!/usr/bin/python3

import os
import time
from evdev import UInput, UInputError, ecodes, util
from collections import namedtuple

absInfoUsesValue = hasattr(util, "resolve_ecodes_dict")
DEFAULT_A2D_DEADZONE = 50
DEFAULT_AXIS_OPTIONS = (0, 0, 255, 0, 5)
DEFAULT_MOUSE_SENSITIVTY = 0.8
DEFAULT_MOUSE_DEADZONE = 5
DEFAULT_SCROLL_REPEAT_DELAY = .250  # Seconds to wait before continual scrolling
DEFAULT_SCROLL_DELAY = .035  # Seconds to wait between scroll events
BUTTON_MODIFIERS = ("+", "-")
_mappings = {}
UInputMapping = namedtuple("UInputMapping",
                           "name bustype vendor product version "
                           "axes axes_options buttons hats keys mouse "
                           "mouse_options")


def parse_button(attr):
    if attr[0] in BUTTON_MODIFIERS:
        modifier = attr[0]
        attr = attr[1:]
    else:
        modifier = None

    return (attr, modifier)


def create_mapping(name, description, bustype=0, vendor=0, product=0,
                   version=0, axes={}, axes_options={}, buttons={},
                   hats={}, keys={}, mouse={}, mouse_options={}):
    axes = {getattr(ecodes, k): v for k, v in axes.items()}
    axes_options = {getattr(ecodes, k): v for k, v in axes_options.items()}
    buttons = {getattr(ecodes, k): parse_button(v) for k, v in buttons.items()}
    hats = {getattr(ecodes, k): v for k, v in hats.items()}
    mouse = {getattr(ecodes, k): parse_button(v) for k, v in mouse.items()}

    mapping = UInputMapping(description, bustype, vendor, product, version,
                            axes, axes_options, buttons, hats, keys, mouse,
                            mouse_options)
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
    """Finds the next available js device name."""
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
        self.evdev_dev = None
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
        self.device = UInput(
            name=layout.name,
            events=events,
            bustype=layout.bustype,
            vendor=layout.vendor,
            product=layout.product,
            version=layout.version)
        self.layout = layout
        print("create ", self.js_dev, self.device)

    def write_event(self, ev_type, code, value):
        last_value = self._write_cache.get(code)
        if last_value != value:
            self.device.write(ev_type, code, value)
            self._write_cache[code] = value

    def reset(self):
        pass

    def emit_buttons(self, code, value):
        # self.write_event(ecodes.EV_KEY, code, value)
        pass

    def emit_axes(self, code, value):
        # self.write_event(ecodes.EV_ABS, code, value)
        pass

    def emit_hats(self):
        # self.write_event(ecodes.EV_ABS, code, value)
        pass

    def emit(self):
        self.device.syn()


if __name__ == '__main__':
    create_uinput_device("xpad")
    while True:
        time.sleep(1)
