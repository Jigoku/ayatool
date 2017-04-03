# USB control for the BlackWeb AYA mouse
# License : GPLv3
# Version : 0.1
# Author  :  Ricky K. Thomson

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


def send_ctrl(data):
	dev.ctrl_transfer(bmRequestType=0x21, bRequest=0x09, wValue=0x0307, wIndex=0x0001, data_or_wLength=data,timeout=1000)


def change_color(r,g,b):
	#changes the led colour
	data = [0x07, 0x0a, 0x01, 0x00] + [int(r),int(g),int(b)] + [0x00]
	send_ctrl(data)


def change_mode(n):
	#changes LED light effect

	if n == 0:
		data = [0x07, 0x0c, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00] #off
	elif n == 1:
		data = [0x07, 0x0c, 0x01, 0x00, 0x0f, 0x00, 0x00, 0x00] #on
	elif n == 2:
		data = [0x07, 0x0b, 0x01, 0x00, 0x08, 0x00, 0x00, 0x00] #breathe
	elif n == 3:
		data = [0x07, 0x0b, 0x01, 0x00, 0x08, 0xff, 0x00, 0x00] #cycle

	send_ctrl(data)


def change_profile(profile):
	#changes the profile in use
	data = [0x07, 0x03] + [profile] + [0x00]*5 #set profile
	send_ctrl(data)


def store_settings():
	data = [0x07, 0x44, 0x01] + [0x00]*5 #store hardware persistent settings
	send_ctrl(data)


def factory_reset():
	#doesn't seem to do anything?
	data = [0x07, 0x03] + [0x00]*6


def change_polling(n):
	#change hardware mouse polling speed
	if n == 0:
		poll = [0x00] #125hz
	elif n == 1:
		poll = [0x01] #250hz
	elif n == 2:
		poll = [0x02] #500hz
	elif n == 3:
		poll = [0x03] #1000hz

	data = [0x07,0x01] + poll + [0x00]*5
	send_ctrl(data)


def debug():
#	send_ctrl([0x07,0x03,0x01] + [0x00]*5)
#	send_ctrl([0x07,0x08,0x01] + [0x00]*5)
	send_ctrl([0x07,0x03,0x00] + [0x00]*5)

