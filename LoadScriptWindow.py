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
import threading
import time

class LoadScriptWindow():
	def __init__(self,protocol,fileName,loadScriptWindowCloseEventCallback,basePath):	
		
		self.loadScriptWindowCloseEventCallback=loadScriptWindowCloseEventCallback
		try:
			builder = gtk.Builder()
			builder.add_from_file(basePath+"/LoadScriptWindow.glade")
		except Exception,e:
			print(e)
			return
			
		self.window = builder.get_object("window1")
		self.window.set_resizable(False)
		self.window.set_icon_from_file(basePath+"/icons/icon.ico")
		self.window.show_all()
		self.window.connect("delete_event", self.__closeBtnEvent)	
		self.window.connect("destroy", self.__closeBtnEvent)	
		
		#Button OK
		self.buttonClose = builder.get_object("btnClose")
		self.buttonClose.connect("clicked", self.__closeEvent, None)
		self.buttonClose.set_sensitive(False)
		
		# status label
		self.lblStatus = builder.get_object("lblStatus")
		#progress bar
		self.progressBar = builder.get_object("progressbar")
		
		self.protocol=protocol
		self.fileName=fileName
		self.thread = threading.Thread(target=self.__sendingThread, args=())
		self.thread.start()
			
			
	def __sendingThread(self):
	
		#on_save_menu_item_activate
	
		gtk.gdk.threads_enter()
		self.lblStatus.set_text("Waiting board reboot...")
		gtk.gdk.threads_leave()

		r,errorMsg = self.protocol.sendFile(self.fileName,self.__callbackStatus)
		if r:
			gtk.gdk.threads_enter()
			self.lblStatus.set_text("File copied")
			self.buttonClose.set_sensitive(True)
			gtk.gdk.threads_leave()
		else:
			gtk.gdk.threads_enter()
			print(self.fileName)
			if self.fileName ==None:
				self.lblStatus.set_text("ERROR: Save File first")
			else:
				self.lblStatus.set_text(errorMsg)
			self.buttonClose.set_sensitive(True)
			gtk.gdk.threads_leave()
		
		
	def __callbackStatus(self,total_packets, success_count, error_count):
		print("total:"+str(total_packets)+" success:"+str(success_count)+" error:"+str(error_count))
		gtk.gdk.threads_enter()
		prog = int((success_count/total_packets)*100)
		self.lblStatus.set_text(str(prog)+"%")	
		self.progressBar.set_fraction(prog/100.0)		
		gtk.gdk.threads_leave()
		
	def __closeEvent(self,a1,a2):		
		self.window.destroy()
		self.loadScriptWindowCloseEventCallback()
		
	def __closeBtnEvent(self,*args):
		return True
		