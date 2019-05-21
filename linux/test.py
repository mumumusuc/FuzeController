#!/usr/bin/python3

import sys

if __name__ == '__main__':
    if len(sys.argv) < 2:
        exit(-1)
    hid_path = sys.argv[1]
    with open(hid_path, 'rb') as hid_dev:
        print("open hidraw file : ", hid_path)
        while True:
            buf = hid_dev.read(10)
            if buf[0] == 0x02:
                print('buttons [', hex(buf[1] | (buf[2] << 8)), ']\tD-Pad [', hex(buf[3]), ']')
