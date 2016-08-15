import socket
import sys
import json
from subprocess import Popen, PIPE
import time
from console.ConsoleEmulator import ConsoleEmulator
import gtk
import os
import threading
from SerialMock import SerialMock

BASE_PATH,filename = os.path.split(sys.argv[0])
if(BASE_PATH==""):
    BASE_PATH="."

class EmulatorLauncher:
	def __init__(self,console,serialMock,file):
		self.console = console
		self.serialMock = serialMock
		self.file=file
		
	def startServer(self):
		self.thread = threading.Thread(target=self.__runServer, args=())
		self.thread.start()
	def __runServer(self):
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		server_address = ('localhost', 10000)
		print >>sys.stderr, 'starting up on %s port %s' % server_address
		sock.bind(server_address)
		sock.listen(1)
		# Wait for a connection
		print >>sys.stderr, 'waiting for a connection'
		connection, client_address = sock.accept()
		try:
			print >>sys.stderr, 'connection from', client_address
			self.serialMock.setSocket(connection)
			self.console.setSocket(connection)
			
			# Receive the data in small chunks and retransmit it
			while True:
				data = connection.recv(4096)
				#print >>sys.stderr, 'received "%s"' % data
				if data:
					try:
						parts = data.split("}{")
						for data in parts:
							if data[0]!="{":
								data = "{"+data
							if data[-1]!="}":
								data = data + "}"
							data = json.loads(data)
							if data["per"]=="STDOUT":
								self.serialMock.insertText(data["data"])
							else:
								self.console.update(data)
					except:
						print("ERROR RCV")
				else:
					print >>sys.stderr, 'no more data from', client_address
					break
				
		finally:
			# Clean up the connection
			connection.close()		

	def startEmulator(self):
		self.thread = threading.Thread(target=self.__runEmulator, args=())
		self.thread.start()
			
	def __runEmulator(self):
		self.serialMock.insertText("\x15")
		if os.name!="posix":
			process = Popen([BASE_PATH+"/"+'emulator/Emulate/Emulate.exe', self.file], bufsize=1,stdout=PIPE, stdin=None)
		else:
			process = Popen(["python",BASE_PATH+"/"+'emulator/Emulate.py', self.file], bufsize=1,stdout=PIPE, stdin=None)		
		stdout, stderr = process.communicate()


if len(sys.argv) == 2:
	file = sys.argv[1]
		
	gtk.gdk.threads_init()
	c = ConsoleEmulator(BASE_PATH)
	serialMock = SerialMock()			

	el = EmulatorLauncher(c,serialMock,file)
	el.startServer()
	el.startEmulator()

	c.showConsole("",serialMock)
	gtk.main()
else:
		print("ERROR. A file must be provided")



