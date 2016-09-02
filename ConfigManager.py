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

from ConfigParser import SafeConfigParser
from ConfigParser import RawConfigParser
from ConfigParser import SafeConfigParser
import os
import sys

CONFIG_FILENAME = ".educiaapythoneditorconfig.dat"
class ConfigManager(object):

	def __init__(self):
		try:
			from win32com.shell import shellcon, shell            
			self.homedir = shell.SHGetFolderPath(0, shellcon.CSIDL_APPDATA, 0, 0)
		except ImportError:
			self.homedir = os.path.expanduser("~")		
		self.homedir = os.path.join(self.homedir,".educiaa-python-editor")
		if not os.path.exists(self.homedir):
			os.makedirs(self.homedir)
		#print("Home dir:"+self.homedir)
		if not os.path.exists(os.path.join(self.homedir,CONFIG_FILENAME)):
			if sys.platform.startswith('win32'):
				self.writeConfig("COM1")
			else:
				self.writeConfig("ttyUSB0")
		
		
	def readConfig(self):
		parser=SafeConfigParser()
		parser.read(os.path.join(self.homedir,CONFIG_FILENAME))
  
		port = parser.get("Serial","port")
		pathEmulator = ""
		try:
			pathEmulator = parser.get("Emulator","path")
		except:
			pass
		print("read from file:"+port)
		return {"port":port,"pathEmulator":pathEmulator}
		
		
		
	def writeConfig(self,port,pathEmulator):
		config = SafeConfigParser()
		config.add_section("Serial")
		port = config.set("Serial","port",port)

		config.add_section("Emulator")
		port = config.set("Emulator","path",pathEmulator)
		
		with open(os.path.join(self.homedir,CONFIG_FILENAME), 'wb') as configfile:
			config.write(configfile)
	
	def readTipsConfig(self):
		parser=SafeConfigParser()
		parser.read(os.path.join(self.homedir,CONFIG_FILENAME))
  
		flagShowAtStart = "1"
		try:
			flagShowAtStart = parser.get("Tips","showAtStart")			
		except:
			pass
		return {"flagShowAtStart":flagShowAtStart}
		
	def writeTipsConfig(self,showAtStart):
		config = SafeConfigParser()
		config.add_section("Tips")
		config.set("Tips","showAtStart",showAtStart)
		
		with open(os.path.join(self.homedir,CONFIG_FILENAME), 'wb') as configfile:
			config.write(configfile)