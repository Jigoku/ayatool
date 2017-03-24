#!/usr/bin/env python

import blackweb_aya_led
import sys
import os

if os.geteuid() != 0:
	exit("You need to have root privileges to run this script.")

blackweb_aya_led.open_usb()
blackweb_aya_led.set_color(sys.argv[1],sys.argv[2],sys.argv[3])
blackweb_aya_led.store_color()
blackweb_aya_led.close_usb()
