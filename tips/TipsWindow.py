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
from os import listdir
from os.path import isfile, join
from ConfigManager import ConfigManager
from random import shuffle
		
class TipsWindow():
	def __init__(self,tipsWindowCloseEventCallback,basePath):	
		
		self.tipsWindowCloseEventCallback=tipsWindowCloseEventCallback
		self.basePath=basePath
		try:
			builder = gtk.Builder()
			builder.add_from_file(basePath+"/tips/TipsWindow.glade")
		except Exception,e:
			print(e)
			return
			
		self.window = builder.get_object("window1")
		self.window.set_icon_from_file(basePath+"/icons/icon.ico")
		self.window.set_title("Tips")		
		self.window.connect("delete_event", self.__closeBtnEvent)	
		self.window.connect("destroy", self.__closeBtnEvent)	

		#Button Next
		self.buttonOk = builder.get_object("btnNext")
		self.buttonOk.connect("clicked", self.__nextEvent, None)

		#Button Close
		self.buttonOk = builder.get_object("btnClose")
		self.buttonOk.connect("clicked", self.__closeBtnEvent, None)

		#lang combo
		self.indexLang=0;
		self.comboLang = builder.get_object("combobox1")
		liststore = gtk.ListStore(str)
		cell = gtk.CellRendererText()
		self.comboLang.pack_start(cell)
		self.comboLang.add_attribute(cell, 'text', 0)		
		self.comboLang.set_wrap_width(5)
		liststore.append(["Spanish"])
		self.comboLang.set_model(liststore)
		self.comboLang.connect('changed', self.__changedLangEvent)
		self.comboLang.set_active(self.indexLang)
		
		
		# show at start config check
		self.checkShowAtStart = builder.get_object("checkShowAtStart")
		self.checkShowAtStart.connect('clicked', self.__changedShowAtStartConfigEvent)
		self.cm = ConfigManager()
		self.checkShowAtStart.set_active(int(self.cm.readTipsConfig()["flagShowAtStart"]))
		
		#images
		self.imgData = builder.get_object("imgData")
		self.indexTip=0
		self.tipList = self.__loadTips(self.indexLang)
		shuffle(self.tipList)
		self.__showNextTip()
		
		
		
	
	def showTips(self,flagForce=False):
		if int(self.cm.readTipsConfig()["flagShowAtStart"])==1 or flagForce==True:
			self.window.show_all()
		
	def __loadTips(self,indexLang):
		if indexLang == 0:
			lanDir="es"
		else:
			lanDir="es"
		
		pathFiles = self.basePath+"/tips/imgs/"+lanDir+"/"
		onlyfiles = [f for f in listdir(pathFiles) if isfile(join(pathFiles, f))]
		tipList = []
		for f in onlyfiles:
			tipList.append(pathFiles+f)		
		return tipList
		
	def __showNextTip(self):
		self.imgData.set_from_file(self.tipList[self.indexTip])
		self.indexTip+=1
		if self.indexTip>=len(self.tipList):
			self.indexTip=0
		
	def __nextEvent(self,a1,a2):
		self.__showNextTip()


	def __closeBtnEvent(self,*args):		
		self.window.destroy()
		if self.tipsWindowCloseEventCallback!=None:
			self.tipsWindowCloseEventCallback()
		
	def __changedLangEvent(self,*args):
		pass
	def __changedShowAtStartConfigEvent(self,*args):
		if self.checkShowAtStart.get_active():
			self.cm.writeTipsConfig("1")
		else:
			self.cm.writeTipsConfig("0")
		