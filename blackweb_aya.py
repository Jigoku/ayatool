# USB library for the BlackWeb AYA mouse
#
# Copyright (C) 2015 Ricky K. Thomson
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
#    VERSION    : 0.2
#
#    Vendor ID  : 3938
#    Product ID : 1101


# TODO
# find out write command for get_polling()
# find out write command for get_smartkey() / set_smartkey()

import usb.core
import usb.util

VENDOR_ID = 0x3938
PRODUCT_ID = 0x1101

def open_usb():
	global dev, interface
	
	
	dev = usb.core.find(idVendor=VENDOR_ID, idProduct=PRODUCT_ID)
	interface = 1

	if dev is None:
		raise ValueError("Device is not connected")

	if dev.is_kernel_driver_active(interface) is True:
		try:
			dev.detach_kernel_driver(interface)
		except usb.core.USBError as e:
			raise ValueError("Failed to detatch kernel driver: %s" % str(e))
			
	usb.util.claim_interface(dev,interface)
	dev.set_interface_altsetting(interface=interface,alternate_setting=0)
	endpoint = dev[0][(interface,0)][0]
	
	print (endpoint)





def close_usb():
	usb.util.release_interface(dev,interface)
	dev.attach_kernel_driver(interface)



#

def get_color(profile):
	
	# bytes to send
	data = [0x07, 0x8a] + [profile] + [0x00]*5
	
	# USB request
	dev.ctrl_transfer(bmRequestType=0x21, bRequest=0x09, wValue=0x0307, wIndex=0x0001, data_or_wLength=data,timeout=1000) 
	
	# USB response
	ret = dev.ctrl_transfer(bmRequestType=0xa1, bRequest=0x1, wValue=0x0307, wIndex=0x0001, data_or_wLength=data,timeout=1000) 
	
	#debug
	#hex_string = "".join("%02x" % b for b in ret)
	#print hex_string
	
	# returns the actively set LED color as a list
	rgb = [ret[3],ret[4],ret[5]]
	return rgb
	
	
def set_color(profile, r,g,b):
	# bytes to change the led colour
	data = [0x07, 0x0a] + [profile] + [ 0x00] + [int(r),int(g),int(b)] + [0x00]
	
	# USB request
	dev.ctrl_transfer(bmRequestType=0x21, bRequest=0x09, wValue=0x0307, wIndex=0x0001, data_or_wLength=data,timeout=1000) 


def get_ledmode(profile):
	data = [0x07, 0x8c] + [profile] + [0x00]*5
	dev.ctrl_transfer(bmRequestType=0x21, bRequest=0x09, wValue=0x0307, wIndex=0x0001, data_or_wLength=data,timeout=1000) 
	
	ret = dev.ctrl_transfer(bmRequestType=0xa1, bRequest=0x1, wValue=0x0307, wIndex=0x0001, data_or_wLength=data,timeout=1000) 
	
	# active LED mode
	if ret[3] == 0x0f:
		return 0
	elif ret[3] == 0x00:
		return 1
	elif ret[3] == 0x0a:
		return 2
	elif ret[3] == 0x07:
		return 3



def set_ledmode(profile, n):
	#changes LED light effect

	if n == 0:
		data = [0x07, 0x0c] + [profile] + [0x00, 0x00, 0x00, 0x00, 0x00] #off
	elif n == 1:
		data = [0x07, 0x0c] + [profile] + [0x00, 0x0f, 0x00, 0x00, 0x00] #on
	elif n == 2:
		data = [0x07, 0x0b] + [profile] + [0x00, 0x08, 0x00, 0x00, 0x00] #breathe
	elif n == 3:
		data = [0x07, 0x0b] + [profile] + [0x00, 0x08, 0xff, 0x00, 0x00] #cycle

	dev.ctrl_transfer(bmRequestType=0x21, bRequest=0x09, wValue=0x0307, wIndex=0x0001, data_or_wLength=data,timeout=1000) 


def set_profile(profile):
	#changes the profile in use
	data = [0x07, 0x03] + [profile] + [0x00]*5 #set profile
	dev.ctrl_transfer(bmRequestType=0x21, bRequest=0x09, wValue=0x0307, wIndex=0x0001, data_or_wLength=data,timeout=1000) 


def get_profile():

	data = [0x07, 0x83] + [0x00]*6
	dev.ctrl_transfer(bmRequestType=0x21, bRequest=0x09, wValue=0x0307, wIndex=0x0001, data_or_wLength=data,timeout=1000) 
	
	ret = dev.ctrl_transfer(bmRequestType=0xa1, bRequest=0x1, wValue=0x0307, wIndex=0x0001, data_or_wLength=data,timeout=1000) 
	
	# active profile number
	return ret[1] 
	

def store_settings(profile):
	data = [0x07, 0x44] + [profile] + [0x00]*5 #store hardware persistent settings
	dev.ctrl_transfer(bmRequestType=0x21, bRequest=0x09, wValue=0x0307, wIndex=0x0001, data_or_wLength=data,timeout=1000) 


def factory_reset():
	#doesn't seem to do anything?
	data = [0x07, 0x03] + [0x00]*6
	dev.ctrl_transfer(bmRequestType=0x21, bRequest=0x09, wValue=0x0307, wIndex=0x0001, data_or_wLength=data,timeout=1000) 


def set_polling(profile, n):
	#change hardware mouse polling speed
	if n == 0:
		poll = [0x00] #125hz
	elif n == 1:
		poll = [0x01] #250hz
	elif n == 2:
		poll = [0x02] #500hz
	elif n == 3:
		poll = [0x03] #1000hz

	data = [0x07] + [profile] + poll + [0x00]*5
	dev.ctrl_transfer(bmRequestType=0x21, bRequest=0x09, wValue=0x0307, wIndex=0x0001, data_or_wLength=data,timeout=1000) 


def debug():
#	send_ctrl([0x07,0x03,0x01] + [0x00]*5)
#	send_ctrl([0x07,0x08,0x01] + [0x00]*5)
	#send_ctrl([0x07,0x03,0x00] + [0x00]*5)
	#print (send_ctrl([0x07, 0x0c, 0x01, 0x00, 0x0f, 0x00, 0x00, 0x00]))
	
	#ret = dev.read(0x21, 0x8a, 0x01)
	print ("test")
