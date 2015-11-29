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

from xmodem import XMODEM
import serial
from array import array
import os
import math
import time

class Protocol:

	def getc(self,size, timeout=1):		
		r = self.port.read()
		print("received:")
		a = array("B", r)
                print map(hex, a)		
		return r

	def putc(self,data, timeout=1):		
		self.port.write(data)
		
		return 1

	def __init__(self,portPath,mode='xmodem'): # (128bytes block). 'xmodem1k' for 1k block
		self.mode = mode
		self.modem = XMODEM(self.getc, self.putc,mode=self.mode)
		self.portPath=portPath

			
				
	def sendFile(self,filePath,callbackStatus):
		self.callbackStatus=callbackStatus
		try:
			self.port = serial.Serial(port=self.portPath,baudrate=115200,timeout = 10)
		except:
			return [False,"Invalid PORT"]
			
		r = False
		try:
			self.fileSize = os.path.getsize(filePath)
			stream = open(filePath, 'rb')			
			r = self.modem.send(stream,retry=2,callback=self.__callbackStatus)
		except:
			pass
		
		self.port.close()		
		return [r,"ERROR"];
	
	def __callbackStatus(self,total_packets, success_count, error_count):
		
		if(self.mode=="xmodem"):
			total = math.ceil(self.fileSize/128) + 1  # 128bytes block
		else:
			total = math.ceil(self.fileSize/1024) + 1 # 1k bytes block
		self.callbackStatus(total,success_count, error_count)
		
