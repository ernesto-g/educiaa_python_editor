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

class TipsWindow():
	def __init__(self,tipsWindowCloseEventCallback,basePath):	
		
		self.tipsWindowCloseEventCallback=tipsWindowCloseEventCallback
		try:
			builder = gtk.Builder()
			builder.add_from_file(basePath+"/tips/TipsWindow.glade")
		except Exception,e:
			print(e)
			return
			
		self.window = builder.get_object("window1")
		self.window.set_icon_from_file(basePath+"/icons/icon.ico")
		self.window.set_title("Tips")
		self.window.show_all()
		self.window.connect("delete_event", self.__closeBtnEvent)	
		self.window.connect("destroy", self.__closeBtnEvent)	

		#Button Next
		self.buttonOk = builder.get_object("btnNext")
		self.buttonOk.connect("clicked", self.__nextEvent, None)

		#Button Close
		self.buttonOk = builder.get_object("btnClose")
		self.buttonOk.connect("clicked", self.__closeBtnEvent, None)


		
	def __nextEvent(self,a1,a2):
		print("next!!")


	def __closeBtnEvent(self,a1,a2):		
		self.window.destroy()
		self.tipsWindowCloseEventCallback()
		
