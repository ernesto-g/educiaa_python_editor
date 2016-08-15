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

import Queue
import threading
import json

class SerialMock:
	def __init__(self):
		self.q = Queue.Queue()
		self.condition = threading.Condition()
		self.__socket = None
		
	def setSocket(self,socket):
		self.__socket = socket

	def read(self):
		self.condition.acquire()
		if not self.q.empty():
			r = self.q.get()
			self.condition.release()
			return r
		else:
			self.condition.wait(1)
			self.condition.release()
			return -1
		
	def write(self,text):
		if self.__socket!=None:
			d = json.dumps({"per":"STDIN","data":text})
			try:
				self.__socket.sendall(d)
			except Exception as e:
				print(e)
		
	def insertText(self,text):
		self.condition.acquire()
		for c in text:
			self.q.put(c)
		self.condition.notify() # signal that a new item is available
		self.condition.release()
		
	def close(self):
		pass