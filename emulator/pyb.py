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

import json
import time
import threading
import sys
import Queue

class CPUMock:
	def __init__(self):
		self.sws = [True,True,True,True]		
		self.leds = [False,False,False,False,0,0,0]

class PeripheralMockManager:
	socket = None
	cpu = CPUMock()
	stdinQueue = Queue.Queue()
	stdinBuffer = ""
	stdinCondition = threading.Condition()

	@staticmethod
	def pmm_setSocket(s):
		PeripheralMockManager.socket = s
	@staticmethod
	def sendData(data):
		if PeripheralMockManager.socket!=None:
			try:
				PeripheralMockManager.socket.send(data)
				#try:
				#	PeripheralMockManager.socket.close()
				#except:
				#	pass
			except:
				pass
	@staticmethod
	def pmm_startReception():
		if PeripheralMockManager.socket!=None:
			t = threading.Thread(target=PeripheralMockManager.runReception)
			t.daemon = True
			t.start()
	@staticmethod
	def runReception():
		while True:
			try:
				data = PeripheralMockManager.socket.recv(4096)
			except:
				print(">>pyb>>RCV ERROR")
				PeripheralMockManager.socket.close()
				return
			
			try:
				data = json.loads(data)
			except:
				PeripheralMockManager.socket.close()
				return
				
			if data["per"]=="Switch":
				PeripheralMockManager.cpu.sws[data["swn"]] = data["swv"]
			if data["per"]=="STDIN":
				if data["data"]=="\n" or data["data"]=="\r\n":
					PeripheralMockManager.stdinCondition.acquire()
					PeripheralMockManager.stdinQueue.put(PeripheralMockManager.stdinBuffer)
					PeripheralMockManager.stdinCondition.notify()
					PeripheralMockManager.stdinCondition.release()
					PeripheralMockManager.stdinBuffer = ""
					PeripheralMockManager.sendData(json.dumps({"per":"STDOUT","data":data["data"]})) # echo
				else:
					if data["data"]=="\b":
						if len(PeripheralMockManager.stdinBuffer)>=1:
							PeripheralMockManager.sendData(json.dumps({"per":"STDOUT","data":"\x1b[K"})) # echo
							PeripheralMockManager.stdinBuffer = PeripheralMockManager.stdinBuffer[0:-1]
					else:
						PeripheralMockManager.sendData(json.dumps({"per":"STDOUT","data":data["data"]})) # echo
						PeripheralMockManager.stdinBuffer+=data["data"]

				
	@staticmethod
	def updateLeds():
		PeripheralMockManager.sendData(json.dumps({"per":"LED","data":PeripheralMockManager.cpu.leds}))

	@staticmethod
	def readStdin():
		while True:
			PeripheralMockManager.stdinCondition.acquire()
			if not PeripheralMockManager.stdinQueue.empty():
				r = PeripheralMockManager.stdinQueue.get()
				PeripheralMockManager.stdinCondition.release()
				return r
			else:
				PeripheralMockManager.stdinCondition.wait()
				PeripheralMockManager.stdinCondition.release()
		
# functions
def delay(val):
	time.sleep(val/1000.0)

# classes		
class LED:
	def __init__(self,ledNumber):
		self.__ln=ledNumber-1		
	def on(self):
		PeripheralMockManager.cpu.leds[self.__ln] = True
		PeripheralMockManager.updateLeds()
	def off(self):
		PeripheralMockManager.cpu.leds[self.__ln] = False
		PeripheralMockManager.updateLeds()
	def intensity(self,val):
		PeripheralMockManager.cpu.leds[self.__ln] = val
		PeripheralMockManager.updateLeds()

class Switch:
	def __init__(self,swNumber):
		self.__sn=swNumber-1
		self.__threadCallback = None
		self.__state0 = False
	def switch(self):
		return PeripheralMockManager.cpu.sws[self.__sn]
	def callback(self,fn):
		self.__fnCallback = fn
		if self.__threadCallback == None:
			t = threading.Thread(target=self.__callbackPool)
			t.daemon = True
			t.start()
	def __callbackPool(self):
		while True:
			time.sleep(0.1)
			#print("pool estado sw")
			if PeripheralMockManager.cpu.sws[self.__sn] == False:
				if self.__state0==False:
					self.__fnCallback(self)
					self.__state0 = True
			else:
				self.__state0 = False
				