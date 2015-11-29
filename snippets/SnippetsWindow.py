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
from SnippetsParser import SnippetsParser

class SnippetsWindow():
	def __init__(self,callback):
		self.callback=callback
			
		try:
			builder = gtk.Builder()
			builder.add_from_file("./snippets/SnippetsWindow.glade")
		except Exception,e:
			print(e)
			return
			
		self.window = builder.get_object("window1")
		self.window.set_icon_from_file("./icons/icon.ico")
		self.txtSrc = builder.get_object("txtSrc")
		self.window.show_all()
		
		self.listW = self.window = builder.get_object("listSnippets")
		store = gtk.ListStore(str,int,str)
		parser = SnippetsParser()
		root = parser.parseSnippets('./snippets/snippets.xml')
		for child in root:		
			store.append([child.attrib["name"],0,child.text])
		
		self.listW.set_model(store)
		
		renderer = gtk.CellRendererText()
		column = gtk.TreeViewColumn("Snippets", renderer, text=0)
		self.listW.append_column(column)

		select = self.listW.get_selection()
		select.connect("changed", self.__on_tree_selection_changed)

		
		#Button OK
		buttonOk = builder.get_object("btnOk")
		buttonOk.connect("clicked", self.__okEvent, None)
	
	def __on_tree_selection_changed(self,selection):
		model, treeiter = selection.get_selected()
		if treeiter != None:
			item = model[treeiter]			
			code = item[2]
			#print(code)
			self.txtSrc.get_buffer().set_text(code)
	
	
	def __okEvent(self,a1,a2):
		self.callback([self.txtSrc.get_buffer().get_text(self.txtSrc.get_buffer().get_start_iter(),self.txtSrc.get_buffer().get_end_iter())])
		