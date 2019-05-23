# FuzeController
战斧F1手柄驱动(Linux/Windows)

### HID协议
1. 按键与摇杆数据(Input)

    Byte|Value|Note
    ----|-----|----
    0   |0x02 |ReportID
    1   |0x00 |Buttons<pre>0b:A<br>1b:B<br>2b:LT<br>3b:X<br>4b:Y<br>5b:RT<br>6b:LB<br>7b:RB</pre>
    2   |0x00 |Buttons<pre>0b:FUZE(hold)<br>1b:-<br>2b:MENU<br>3b:VIEW<br>4b:FUZE(release)<br>5b:L3<br>6b:R3<br>7b:-<br><br>* FUZE键长按约1s触发bit0,释放时触发bit4</pre>
    3   |0x0F |D-Pad(低4位)<pre>0:Up<br>1:Up-Right<br>2:Right<br>3:Down-Right<br>4:Down<br>5:Down-Left<br>6:Left<br>7:Up-Left<br>F:Idle</pre>
    4   |0x00~0xFF |Left stick X<pre>uint8<br>default=0x80</pre>
    5   |0x00~0xFF |Left stick Y<pre>uint8<br>default=0x80</pre>
    6   |0x00~0xFF |Right stick X<pre>uint8<br>default=0x80</pre>
    7   |0x00~0xFF |Right stick Y<pre>uint8<br>default=0x80</pre>
    8   |0x00~0xFF |Left trigger<pre>uint8<br>default=0x00<br>threshold=0x40</pre>
    9   |0x00~0xFF |Right trigger<pre>uint8<br>default=0x00<br>threshold=0x40</pre>

    *由@[sentisk](https://github.com/sentisk)提供*
    
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
# sudo apt install python3-pip python3-hidapi
# pip3 install evdev

# sudo python3 hidinput.py 
```

### Windows驱动
> TBD

### 其它
[ds4drv](https://github.com/chrippa/ds4drv)
