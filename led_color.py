#!/usr/bin/env python

import blackweb_aya
import sys
import os

if os.geteuid() != 0:
	exit("You need to have root privileges to run this script.")

blackweb_aya.open_usb()
blackweb_aya.change_mode(2)
blackweb_aya.change_color(sys.argv[1],sys.argv[2],sys.argv[3])
#blackweb_aya.change_polling(3)
blackweb_aya.store_settings()
blackweb_aya.close_usb()
