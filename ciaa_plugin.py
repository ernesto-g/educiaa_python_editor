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

from console.Console import Console
import serial.tools.list_ports
from ConfigWindow import ConfigWindow
from LoadScriptWindow import LoadScriptWindow
from ConfigManager import ConfigManager
from protocol.Protocol import Protocol
from snippets.SnippetsWindow import SnippetsWindow

#emulator
import subprocess

class mnu_EDUCIAA:
	
	def __init__(self):
		self.configManager = ConfigManager()
		self.console = None
		self.loadScriptWindow = None
		self.interface=None
		self.p = None
		
	def item_Console(self,menuItem,interface):
		self.console = Console(interface.get_base_path())
		config = self.__getConfigData()
			
		if self.console.showConsole(config["port"]):
			self.console.addText(config["port"] + " Opened.\n")
		else:
			interface.message("Error opening serial port: "+config["port"])
			self.console.closeConsole()
			self.console = None
	
	def item_Load_Script(self,menuItem,interface):
		#debug!
		#if self.p!=None:
		#	self.p.kill()
		#	time.sleep(0.5)
			
		self.p = subprocess.Popen([".\PyInstaller-3.1\EmulatorLauncher\dist\EmulatorLauncher\EmulatorLauncher.exe", interface.get_filename()])
		#self.p.communicate()
		"""
		if self.console!=None:
			self.console.closeConsole()
			self.console = None
			
		config = self.__getConfigData()			
		
		if self.loadScriptWindow==None:
			protocol = Protocol(config["port"])		
			self.loadScriptWindow = LoadScriptWindow(protocol,interface.get_filename(),self.__loadScriptWindowCloseEvent,interface.get_base_path()) # show status window
		"""

	def item_Snippets(self,menuItem,interface):
		self.interface=interface
		self.snippetsW = SnippetsWindow(self.__callbackInsertSnippet,interface.get_base_path())
	
		
	def item_Configuration(self,menuItem,interface):
		config = self.configManager.readConfig()
		self.configW = ConfigWindow(self.__callbackPort,config["port"],interface.get_base_path()) # show config window
		

	def __callbackInsertSnippet(self,data):
		code = data[0]
		self.interface.insert(code)
	
	def __callbackPort(self,data):			
		self.configManager.writeConfig(data[0])
	
	def __getConfigData(self):
		config = self.configManager.readConfig()
		if config.has_key("port")==False:
			ports = list(serial.tools.list_ports.comports())
			config["port"] = ports[0][0] #default port
		return config

	def __loadScriptWindowCloseEvent(self):
		self.loadScriptWindow = None
		
