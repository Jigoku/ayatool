#!/usr/bin/env python
# Copyright (C) 2017 Ricky K. Thomson
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# u should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# This is only a sample file and does not include full feature use
# for controlling the mouse. ayatool_qt.py provieds more features.
#
# This will hopefully be updated soon to include the use of getargs
# to set other features such as LED mode and polling/smartkey. 

import blackweb_aya
import sys, os

if len(sys.argv) <= 3:
		for v in sys.argv:
			if type(v) != int or v < 0 or v > 255:
				raise ValueError('Colors must be supplied as 0-255 only')
				sys.exit(1);
				
blackweb_aya.open_usb()
#blackweb_aya.get_color(1)
#blackweb_aya.get_ledmode(1)
#blackweb_aya.get_profile()
blackweb_aya.set_profile(1)
blackweb_aya.set_ledmode(1,1)
blackweb_aya.set_color(1, sys.argv[1],sys.argv[2],sys.argv[3])
blackweb_aya.set_polling(1,3)
blackweb_aya.store_settings(1)

blackweb_aya.close_usb()
