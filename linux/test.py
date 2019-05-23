#!/usr/bin/python3

import os, sys

bt = '0105 0609 01a1 0485 0175 0895 0705 e019 e729 0015 0125 0281 0175 0895 0c05 cd09 b609 b509 b409 b309 230a 0a02 0224 4009 0015 0125 0281 0595 0175 0805 0119 0529 0291 0195 0375 0391 0695 0875 0015 ff26 0500 1907 2900 81ff c000 0105 0509 01a1 0285 0905 0109 0209 0909 0409 0509 0a09 0709 0809 0015 0125 0175 0895 0281 0705 6609 8009 0905 0c09 1009 0d09 0e09 0f09 0705 8109 0015 0125 0175 0895 0281 0105 0015 0725 3b46 9501 7501 6504 0914 8139 7542 9501 8104 0501 1501 2600 00ff 3009 3109 3209 3509 0495 0875 0281 0205 0015 ff26 0900 09c4 95c5 7502 8108 c002'


def dump_bt_report(raw_data):
    bts = raw_data.split(" ")
    result = []
    for _bt in bts:
        result.append(_bt[2:])
        result.append(_bt[0:2])
    report = ' '.join(result)
    os.system('echo "' + report + '" | xxd -r -p | hidrd-convert -o spec ')


def str_2_hex(_str):
    if len(_str) == 0:
        return None
    _byte = bytearray()
    for _s in _str.split(' '):
        _byte.append(int(_s, 16))
    return _byte


if __name__ == '__main__':
    # dump_bt_report(bt)
    path = sys.argv[1]
    with open(path, 'wb') as hidraw:
        while True:
            _read = input('read bytes : ')
            ret = str_2_hex(_read)
            if ret:
                hidraw.write(ret)
                hidraw.flush()
