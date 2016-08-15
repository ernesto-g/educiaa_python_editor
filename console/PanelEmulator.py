########################################################################
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

#
#	EDU-CIAA Python editor (2016)
#	
#	<ernestogigliotti@gmail.com>
#
########################################################################

import gtk 
import pango
import serial
import threading
import struct
import time
import datetime
from console.Console import Console
import json

class PanelEmulator:
	def __init__(self,basePath):
		self.c = Console(basePath)
		self.__socket = None
		self.__emulatorLauncher = None
		
		try:
			builder = gtk.Builder()
			builder.add_from_file(basePath+"/EmulatorPanel.glade")
		except Exception,e:
			print(e)
			return
			
		self.window = builder.get_object("window1")
		self.window.connect("destroy", self.__closePanel)
		self.window.set_icon_from_file(basePath+"/icons/icon.ico")
		self.window.set_title("EDU-CIAA Emulator Panel")

		self.buttonOk = builder.get_object("btnSw1")
		self.buttonOk.connect("clicked", self.__btnSw1, None)

		self.buttonOk = builder.get_object("btnSw2")
		self.buttonOk.connect("clicked", self.__btnSw2, None)

		self.buttonOk = builder.get_object("btnSw3")
		self.buttonOk.connect("clicked", self.__btnSw3, None)


		self.buttonOk = builder.get_object("btnSw4")
		self.buttonOk.connect("clicked", self.__btnSw4, None)

		#leds
		self.chkLed1 = builder.get_object("chkLed1")
		self.chkLed2 = builder.get_object("chkLed2")
		self.chkLed3 = builder.get_object("chkLed3")
		self.lblRgb = builder.get_object("lblRgb")
		self.lblRgb.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse('#000000'))
		
		self.imgBkg = builder.get_object("image1")
		self.imgBkg.set_from_file(basePath+"/educiaa.png")
		
		self.window.show_all()

	def showConsole(self,port,serialMock):
		self.c.showConsole(port,serialMock)

	def __btnSw1(self,a1,a2):
		if self.__socket!=None:
			self.__socket.sendall(json.dumps({"per":"Switch","swn":0,"swv":False}))
			time.sleep(0.1)
			self.__socket.sendall(json.dumps({"per":"Switch","swn":0,"swv":True}))			
		
	def __btnSw2(self,a1,a2):
		if self.__socket!=None:
			self.__socket.sendall(json.dumps({"per":"Switch","swn":1,"swv":False}))
			time.sleep(0.1)
			self.__socket.sendall(json.dumps({"per":"Switch","swn":1,"swv":True}))			

	def __btnSw3(self,a1,a2):
		if self.__socket!=None:
			self.__socket.sendall(json.dumps({"per":"Switch","swn":2,"swv":False}))
			time.sleep(0.1)
			self.__socket.sendall(json.dumps({"per":"Switch","swn":2,"swv":True}))			

	def __btnSw4(self,a1,a2):
		if self.__socket!=None:
			self.__socket.sendall(json.dumps({"per":"Switch","swn":3,"swv":False}))
			time.sleep(0.1)
			self.__socket.sendall(json.dumps({"per":"Switch","swn":3,"swv":True}))			

	def update(self,data):
		if data["per"]=="LED":
			gtk.gdk.threads_enter()			
			ledsStatus = data["data"]
			self.chkLed1.set_active(ledsStatus[0])
			self.chkLed2.set_active(ledsStatus[1])
			self.chkLed3.set_active(ledsStatus[2])
			r = (ledsStatus[3]/15.0)*255
			if r>255 :
				r=255
			g = (ledsStatus[4]/15.0)*255
			if g>255 :
				g=255
			b = (ledsStatus[5]/15.0)*255
			if b>255 :
				b=255
			colorStr = "%0.2X" % r
			colorStr+= "%0.2X" % g
			colorStr+= "%0.2X" % b
			self.lblRgb.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse('#'+colorStr))
			gtk.gdk.threads_leave()
	
		
	def setSocket(self,socket):
		self.__socket = socket
	
	def __closePanel(self,arg):
		self.c.closeConsole()
		self.window.destroy()
		if self.__emulatorLauncher!=None:
			self.__emulatorLauncher.closeAll()
			
	def setEmulatorLauncher(self,el):
		self.__emulatorLauncher = el