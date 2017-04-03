#!/usr/bin/env python

import blackweb_aya
import sys
import os

if os.geteuid() != 0:
	exit("You need to have root privileges to run this script.")

if len(sys.argv) <= 3:
		for v in sys.argv:
			if type(v) != int or v < 0 or v > 255:
				raise ValueError('Colors must be supplied as 0-255 only')
				sys.exit(1);
				
blackweb_aya.open_usb()
#blackweb_aya.factory_reset()
blackweb_aya.change_profile(1)
blackweb_aya.change_mode(1)
blackweb_aya.change_color(sys.argv[1],sys.argv[2],sys.argv[3])
blackweb_aya.change_polling(3)
blackweb_aya.store_settings()

blackweb_aya.close_usb()
