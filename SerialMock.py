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