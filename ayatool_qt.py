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
#    VERSION    : 0.3
#
#    Vendor ID  : 3938
#    Product ID : 1101


from PyQt4 import QtCore, QtGui
import sys, os
import ayatoolgui
import blackweb_aya


class config():
	def __init__(self):
		global rgb, profile, ledmode, pollingrate, smartkey
		

class AyaTool(QtGui.QMainWindow, ayatoolgui.Ui_MainWindow):
	def __init__(self):
		super(self.__class__, self).__init__()
		self.setupUi(self)
		
		# set up connect signals
		self.btnUpdateMouse.activated.connect(self.UpdateMouse)
		self.btnFactoryReset.activated.connect(self.FactoryReset)
		self.btnExit.activated.connect(self.Exit)
		self.btnGithub.activated.connect(self.Github)
		self.btnAbout.activated.connect(self.About)
		self.comboMousePolling.currentIndexChanged.connect(self.PollingRate)
		self.comboProfile.currentIndexChanged.connect(self.Profile)
		self.comboSmartKey.currentIndexChanged.connect(self.SmartKey)
		self.btnApply.clicked.connect(self.UpdateMouse)
		self.radioLedOff.clicked.connect(self.LedMode)
		self.radioLedOn.clicked.connect(self.LedMode)
		self.radioLedBreathe.clicked.connect(self.LedMode)
		self.radioLedCycle.clicked.connect(self.LedMode)
		
		
		self.hboxLedColor.addWidget(ColorBox())
		
		
		# open the USB device
		blackweb_aya.open_usb()
		
		# set the current profile
		config.profile = blackweb_aya.get_profile()
		self.comboMousePolling.setCurrentIndex(config.profile -1)
		
		# set the smartkey
				
		config.smartkey = 1 # find out how to get this value
		self.comboSmartKey.setCurrentIndex(config.smartkey -1)
		
		# set the current color
		config.rgb = blackweb_aya.get_color(config.profile)
		ColorBox.setStyleSheet(self, "QWidget#ColorBox { background-color: rgb(%d,%d,%d) }" % (config.rgb[0],config.rgb[1],config.rgb[2]))
		
		# set the current LED mode
		config.ledmode = blackweb_aya.get_ledmode(config.profile)
		
		if config.ledmode == 0:
			self.radioLedOn.setChecked(1)
		elif config.ledmode == 1:
			self.radioLedOff.setChecked(1)
		elif config.ledmode == 2:
			self.radioLedBreathe.setChecked(1)
		elif config.ledmode == 3:
			self.radioLedCycle.setChecked(1)
		
		# todo:
		# implement reading current values for:
		# * polling rate
		# * smart key
		
		
		#close the USB device
		blackweb_aya.close_usb()
		
		
	def UpdateMouse(self):
		blackweb_aya.open_usb()
		blackweb_aya.set_profile(config.profile)
		blackweb_aya.set_ledmode(config.profile,config.ledmode)
		blackweb_aya.set_color(config.profile, config.rgb[0],config.rgb[1],config.rgb[2])
		blackweb_aya.set_polling(config.profile,config.pollingrate)
		blackweb_aya.set_smartkey(config.smartkey)
		blackweb_aya.store_settings(config.profile)
		blackweb_aya.close_usb()
		
	def PollingRate(self,i):
		config.pollingrate = i
		
	def LedMode(self):
		if self.radioLedOff.isChecked():
			config.ledmode = 0
		if self.radioLedOn.isChecked():
			config.ledmode = 1
		if self.radioLedBreathe.isChecked():
			config.ledmode = 2
		if self.radioLedCycle.isChecked():
			config.ledmode = 3
			
		print config.ledmode
		
	def Profile(self,i):
		config.profile = i +1
		
	def SmartKey(self,i):
		config.smartkey = i +1
		
	def FactoryReset(self):
		blackweb_aya.open_usb()
		blackweb_aya.factory_reset()
		#blackweb_aya.store_settings(config.profile)
		blackweb_aya.close_usb()
		
	def Exit(self):
		sys.exit()

	def Github(self):
		# maybe a better way to do this?
		os.system("xdg-open " + "http://github.com/Jigoku/blackweb_aya")

	def About(self):
		# TODO About dialog
		print ("test")


class ColorBox(QtGui.QFrame):
	def __init__(self,parent=None):
		super(ColorBox,self).__init__(parent)

        # setup ColorBox widget
		self.color = QtCore.Qt.white
		self.setFixedHeight(20)
		self.setFrameStyle(0)
		self.setObjectName("ColorBox");
		self.setStyleSheet("QWidget { border-color: rgba(,0,0,0)}")
		
		
	def mousePressEvent(self, e):
		if e.buttons() == QtCore.Qt.LeftButton:
			
			# spawn the color dialog
			col = QtGui.QColorDialog.getColor(self.color, self)
   
		if col.isValid():
			config.rgb = [col.red(), col.green(), col.blue()]
			
			# update ColorButton background color
			self.setStyleSheet("QWidget#ColorBox { background-color: rgb(%d,%d,%d) }" % (config.rgb[0],config.rgb[1],config.rgb[2]))

			#Possibly preview the LED color, by setting it, without storing the setting here?
			#blackweb_aya.open_usb()
			#blackweb_aya.set_ledmode(config.profile,config.ledmode)
			#blackweb_aya.set_color(config.profile, config.rgb[0],config.rgb[1],config.rgb[2])
			#blackweb_aya.close_usb()

def main():
	app = QtGui.QApplication(sys.argv)
	form = AyaTool()
	form.show()

	sys.exit(app.exec_())

if __name__ == '__main__':
	main()
