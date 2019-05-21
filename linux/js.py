#!/usr/bin/python3

import array
from fcntl import ioctl


def get_js_name(js_dev):
    buf = array.array('u', ['\0'] * 16)
    ret = ioctl(js_dev, 0x80006a13 + (0x10000 * len(buf)), buf)
    return buf.tostring()[0:ret]


def get_js_num(js_dev):
    buf = array.array('B', [0])
    ioctl(js_dev, 0x80016a11, buf)
    num_axis = buf[0]
    ioctl(js_dev, 0x80016a12, buf)
    num_buttons = buf[0]
    return num_buttons, num_axis


if __name__ == '__main__':
    with open('/dev/input/js0', 'rb') as dev:
        js_name = get_js_name(dev)
        print(js_name)
        btn, axis = get_js_num(dev)
        print(btn, axis)
