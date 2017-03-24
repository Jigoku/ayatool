# Linux userspace tools for the BlackWeb AYA mouse
###About
A simple script to customise the LED colour of the mouse natively under a Linux environment.
Reverse engineered using wireshark and usbmon to capture usb control frames from a windows VM, so far i have discovered how to set the LED color, and how to store this as a persistent setting.

#####TODO;
* Add support for turning the LED off
* Add support to configure LED effect (on, breathing, cycle)

###Current Features
* LED colour control

####Usage
``./led_color.py <r> <g> <b>``
for example, to set the mouse LED to green:
``./led_color.py 0 255 0``
