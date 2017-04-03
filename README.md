# Linux userspace tools for the BlackWeb AYA mouse
### About
A userspace tool to customise the LED colour of the mouse natively under a Linux environment. Also supporting some other hardware based features such as mouse polling. It's possible this will work on other platforms too (bsd / osx).

The USB protocol was reverse engineered using wireshark and usbmon to capture USB control messages from a windows virtual machine.

### Current Features
* change LED color 
* change LED color mode (on, off, breathe, cycle)
* Hardware persistent settings
* Hardware mouse polling adjustment

#### Usage
```
./led_color.py <r> <g> <b>
```
for example, to set the mouse LED to green:
```
./led_color.py 0 255 0
```

#### Requirements
* Python 2.7.*
* PyUSB
