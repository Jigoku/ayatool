# USB library for the BlackWeb AYA mouse
#
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
#    VERSION    : 0.3
#
#    Vendor ID  : 3938
#    Product ID : 1101

import usb.core
import usb.util

VENDOR_ID = 0x3938
PRODUCT_ID = 0x1101
DEBUG = True

def open_usb():
	#setup the USB mouse ready for reads/writes
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
	
	#DEBUG
	#endpoint = dev[0][(interface,0)][0]
	#print (endpoint)



def close_usb():
	#reattach the kernel driver
	usb.util.release_interface(dev,interface)
	dev.attach_kernel_driver(interface)



def usb_write(data):
	#write to the usb device
	#return number of bytes written

	ret = dev.ctrl_transfer(
		bmRequestType=0x21, 
		bRequest=0x09, 
		wValue=0x0307, 
		wIndex=0x0001, 
		data_or_wLength=data,timeout=1000
	) 
	
	if DEBUG:
		print "\tSEND " + hex2string(data)
		

def usb_read(data):
	#send a write to the device
	usb_write(data)
	
	#return response data
	ret = dev.ctrl_transfer(
		bmRequestType=0xa1, 
		bRequest=0x1, 
		wValue=0x0307, 
		wIndex=0x0001, 
		data_or_wLength=data,timeout=1000
	) 
	
	if DEBUG:
		print "\tRECV " + hex2string(ret)
	
	return ret
	
	
def hex2string(h):
	string = "".join("%02x " % b for b in h)
	return string
	
	
def get_color(profile):
		
	#get the current LED color
	data = [0x07, 0x8a] + [profile] + [0x00]*5
	ret = usb_read(data)
	
	#DEBUG
	#hex_string = "".join("%02x" % b for b in ret)
	#print hex_string
	
	# returns the actively set LED color as a list
	rgb = [ret[3],ret[4],ret[5]]
	return rgb
	
	
def set_color(profile, r,g,b):
		
	# set a new LED colour
	data = [0x07, 0x0a] + [profile] + [ 0x00] + [int(r),int(g),int(b)] + [0x00]
	usb_write(data)


def get_ledmode(profile):

	#get the active LED light mode
	data = [0x07, 0x8c] + [profile] + [0x00]*5
	ret = usb_read(data)
	
	#TODO FIX THIS
	#return the LED mode as int (0-3)
	if ret[3] == 0x0f: 
		return 0 #off
	elif ret[3] == 0x00:
		return 1 #on
	elif ret[3] == 0x0a:
		return 2 #breathe
	elif ret[3] == 0x07:
		return 3 #cycle


def set_ledmode(profile, n):
		
	#set the LED light mode

	if n == 0:
		data = [0x07, 0x0c] + [profile] + [0x00, 0x00, 0x00, 0x00, 0x00] #off
	elif n == 1:
		data = [0x07, 0x0c] + [profile] + [0x00, 0x0f, 0x00, 0x00, 0x00] #on
	elif n == 2:
		data = [0x07, 0x0b] + [profile] + [0x00, 0x08, 0x00, 0x00, 0x00] #breathe
	elif n == 3:
		data = [0x07, 0x0b] + [profile] + [0x00, 0x08, 0xff, 0x00, 0x00] #cycle

	usb_write(data)
	

def set_smartkey(n):
		
	#set the smartkey delay
	data = [0x07, 0x19, 0x01] + [0x00]*5
	usb_write(data)
	
	 
def set_profile(profile):
		
	#set the new profile slot
	data = [0x07, 0x03] + [profile] + [0x00]*5
	usb_write(data)
	

def get_profile():
		
	#get the actively set profile slot
	data = [0x07, 0x83] + [0x00]*6
	ret = usb_read(data)
	
	return ret[1] 
	

def store_settings(profile):
		
	#store hardware persistent settings
	data = [0x07, 0x44] + [profile] + [0x00]*5 
	usb_write(data)
	

def factory_reset():
		
	#reset to the hardware defaults
	data = [0x07, 0x03] + [0x00]*6
	usb_write(data)


def set_polling(profile, n):
		
	#set hardware mouse polling speed
	if n == 0:
		poll = [0x00] #125hz
	elif n == 1:
		poll = [0x01] #250hz
	elif n == 2:
		poll = [0x02] #500hz
	elif n == 3:
		poll = [0x03] #1000hz

	data = [0x07] + [profile] + poll + [0x00]*5
	usb_write(data)


def get_polling(profile):
	
	data = [0x07] + [0x81] + [profile] + [0x00]*5
	ret = usb_read(data)
	
	return ret[1]
	
	
def debug():
	pass
