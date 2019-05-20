# FuzeController
战斧F1手柄驱动(Linux/Windows)

### HID协议
1. 按键与摇杆数据(Input)

    Byte|Value|Note
    ----|-----|----
    0   |0x02 |ID
    1   |0xFF |Buttons<pre>0b:?<br>1b:?<br>2b:?<br>3b:LT<br>4b:?<br>5b:?<br>6b:?<br>7b:?</pre>
    2   |0x1F |Buttons<pre>0b:?<br>1b:?<br>2b:?<br>3b:?<br>4b:?</pre>
    3   |0x0F~0x8F |D-Pad<pre>0:Up<br>1:Up-Right<br>2:Right<br>3:Down-Right<br>4:Down<br>5:Down-Left<br>6:Left<br>7:Up-Right<br>8:Idle</pre>
    4   |0x00~0xFF |Left stick X<pre>uint8<br>default=0x80</pre>
    5   |0x00~0xFF |Left stick Y<pre>uint8<br>default=0x80</pre>
    6   |0x00~0xFF |Right stick X<pre>uint8<br>default=0x80</pre>
    7   |0x00~0xFF |Right stick Y<pre>uint8<br>default=0x80</pre>
    8   |0x00~0xFF |Left trigger<pre>uint8<br>default=0x00</pre>
    9   |0x00~0xFF |Right trigger<pre>uint8<br>default=0x00</pre>

2. 震动数据(Output)
    
    > TBD

### USB/Bluetooth
[USB-HID-Report](https://github.com/mumumusuc/FuzeController/blob/master/fuze_controller_hid_dump.txt)

[BT-HID-Report](?)(是否和usb-hid-report一样？)

### Linux驱动
> TBD

### Windows驱动
> TBD

### 其它
> TBD
