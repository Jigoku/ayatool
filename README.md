# Linux userspace tools for the BlackWeb AYA mouse
### About
Userspace tools to customise the LED colour of the mouse natively under a Linux environment. Also supporting some other hardware based features such as mouse polling. It's possible this will work on other platforms too (bsd / osx).

Vendor  ID: 3938
Product ID: 1101

The USB protocol was reverse engineered using wireshark and usbmon to capture USB control messages from a windows virtual machine. All discovered features of this mouse are documented here: 

https://github.com/Jigoku/ayatool/issues/2

If you are interested in reading how this was done, i have posted an article here:

https://bytepunk.wordpress.com/2017/03/25/reverse-engineering-a-usb-mouse/

### Current Features
* profile slots
* change LED color 
* change LED color mode (on, off, breathe, cycle)
* Hardware persistent settings
* Hardware mouse polling adjustment
* GUI tool using PyQt



### WARNING
This is still work in progress, there may be bugs or missing features
The script requires root access (sudo) to write/read from the USB device
The author takes no responsibility for anything that may go wrong!

You should be able to setup a udev rule for the device, as to not require root access like so:
*/etc/udev/rules.d/50-blackweb-aya.rules*
```
SUBSYSTEMS=="usb", ATTRS{idVendor}=="3938", ATTRS{idProduct}=="1101", GROUP:="plugdev"
```

#### Running the command line tool
```
./ayatool.py <r> <g> <b>
```
for example, to set the mouse LED to green:
```
./ayatool.py 0 255 0
```

#### Running the PyQt interface
```
./ayatool_qt.py
```

If the mouse randomly turns off the LED when setting a new profile, this is a bug. You can work around it by issuing the factory reset command ('File > Factory Reset' in the PyQt interface). It seems to be caused by setting breathe/cycle as the LED mode, but can be unpredictable. Still working on figuring out why this happens. 

#### Requirements
* Python 2.7.*
* PyUSB
* PyQt / Qt4 (for the user interface)

#### Screenshot
![screenshot_2017-04-12_23-43-52](https://cloud.githubusercontent.com/assets/1535179/24982601/121e5fd8-1fda-11e7-9967-bc6128445a67.png)
