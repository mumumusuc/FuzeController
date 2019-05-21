# FuzeController
战斧F1手柄驱动(Linux/Windows)

### HID协议
1. 按键与摇杆数据(Input)

    Byte|Value|Note
    ----|-----|----
    0   |0x02 |ID
    1   |0xFF |Buttons<pre>0b:?<br>1b:?<br>2b:?<br>3b:LT<br>4b:?<br>5b:?<br>6b:?<br>7b:?</pre>
    2   |0x1F |Buttons<pre>0b:?<br>1b:?<br>2b:?<br>3b:?<br>4b:?</pre>
    3   |0x0F? |D-Pad<pre>0:Up<br>1:Up-Right<br>2:Right<br>3:Down-Right<br>4:Down<br>5:Down-Left<br>6:Left<br>7:Up-Left<br>8:Idle</pre>
    4   |0x00~0xFF |Left stick X<pre>uint8<br>default=0x80</pre>
    5   |0x00~0xFF |Left stick Y<pre>uint8<br>default=0x80</pre>
    6   |0x00~0xFF |Right stick X<pre>uint8<br>default=0x80</pre>
    7   |0x00~0xFF |Right stick Y<pre>uint8<br>default=0x80</pre>
    8   |0x00~0xFF |Left trigger<pre>uint8<br>default=0x00</pre>
    9   |0x00~0xFF |Right trigger<pre>uint8<br>default=0x00</pre>

    *上述表格并不完整，需要有设备的朋友帮助测试按键关系。*
    >Linux下可以使用 
    <br>`# hexdump /dev/hidraw* | tee log.txt` 
    <br>或者[test.py](https://github.com/mumumusuc/FuzeController/blob/master/linux/test.py) 
    <br>`# python3 test.py "/dev/hidraw*" | tee log.txt`
    <br>观察每个按键“按下-松开”后的数值变化来确认手柄按键顺序,输出数据将记录在log.txt。
    
2. 震动数据(Output)
    
    > TBD

### USB/Bluetooth
[USB-HID-Report](https://github.com/mumumusuc/FuzeController/blob/master/fuze_controller_hid_dump.txt)

[BT-HID-Report](?)(是否和usb-hid-report一样？)

### Linux驱动

![转为Xbox手柄使用](https://github.com/mumumusuc/FuzeController/blob/master/images/xpad.png)

测试时请使用hidinput.py,会使用Uinput创建Xbox手柄设备,使用jstest-gtk或者Steam下测试识别是否正常。
    
```
// python依赖
# sudo apt install python3-pip
# pip3 install evdev

// 确认hid设备
# ls -al /dev/hidraw*
> crw-rw----+ 1 root root 244, 2 5月  21 17:36 /dev/hidraw2

# sudo python3 hidinput.py "/dev/hidraw2"
```

### Windows驱动
> TBD

### 其它
[ds4drv](https://github.com/chrippa/ds4drv)
