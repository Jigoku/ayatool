# BlackWeb AYA LED controller library
# License : GPLv3
# Version : 0.1
# Author  :  Ricky K. Thomson (24th March 2017)

import usb.core
import usb.util

def open_usb():
	global dev
	dev = usb.core.find(idVendor=0x3938, idProduct=0x1101)

	if dev is None:
		raise ValueError('Device is not connected')

	dev.detach_kernel_driver(1)
	usb.util.claim_interface(dev,1)

	dev.set_interface_altsetting(interface=1,alternate_setting=0)


def close_usb():
	usb.util.release_interface(dev,1)
	dev.attach_kernel_driver(1)


def set_color(r,g,b):
	#set the led colour
	colors = [int(r),int(g),int(b)]
	data = [0x07, 0x0a, 0x01, 0x00] + colors + [0x00]
	dev.ctrl_transfer(bmRequestType=0x21, bRequest=0x09, wValue=0x0307, wIndex=0x0001, data_or_wLength=data,timeout=1000)


def store_color():
	#store color (persistent), flashes momentarily
	data = [0x07,0x44,0x01,0x00,0x00,0x00,0x00,0x00]
	dev.ctrl_transfer(bmRequestType=0x21, bRequest=0x09, wValue=0x0307, wIndex=0x0001, data_or_wLength=data,timeout=1000)


