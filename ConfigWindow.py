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
#	EDU-CIAA Python editor (2015)
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
import serial.tools.list_ports

class ConfigWindow():
	def __init__(self,callback,currentPort,basePath):
		self.callback=callback
		try:
			self.ports = list(serial.tools.list_ports.comports())
			#print(self.ports)
		except:
			self.ports = list("")
		
		try:
			builder = gtk.Builder()
			builder.add_from_file(basePath+"/ConfigWindow.glade")
		except Exception,e:
			print(e)
			return
			
		self.window = builder.get_object("window1")
		self.window.set_icon_from_file(basePath+"/icons/icon.ico")
		self.window.show_all()

		#Populate combobox
		combobox = builder.get_object("comboPorts")
		liststore = gtk.ListStore(str)
		cell = gtk.CellRendererText()
		combobox.pack_start(cell)
		combobox.add_attribute(cell, 'text', 0)		
		combobox.set_wrap_width(5)
		
		indexActive=0
		i=0
		for port in self.ports:
			liststore.append([str(port[0])])
			if str(port[0]) == currentPort:
				indexActive=i
			i+=1
		
		combobox.set_model(liststore)
		combobox.connect('changed', self.__changedCb)
		combobox.set_active(indexActive)
		
		#Button OK
		self.buttonOk = builder.get_object("btnOk")
		self.buttonOk.connect("clicked", self.__okEvent, None)
		
	def __changedCb(self, combobox):
		model = combobox.get_model()
		index = combobox.get_active()
		if index > -1:
			#print model[index][0], 'selected'
			self.portSelected = model[index][0]
		return
			
	def __okEvent(self,a1,a2):
		self.callback([self.portSelected])
		self.window.destroy()
