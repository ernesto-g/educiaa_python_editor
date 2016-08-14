import sys
import socket
import pyb 
import json
import time
import threading
import Queue


class writer :
	def write(self, text) :
		pyb.PeripheralMockManager.sendData(json.dumps({"per":"STDOUT","data":text}))
			
class reader :
	def readline(self) :
		s = pyb.PeripheralMockManager.readStdin()
		return "'"+s.replace("'","\\'")+"'"
		
if len(sys.argv) == 2:
	timeout=3
	while True:
		try:
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			server_address = ('localhost', 10000)
			print("Connecting...")
			sock.connect(server_address)
			break;
		except:
			time.sleep(1)
			timeout-=1
			if timeout==0:
				print("Connection error")
				#exit()
				sock = None
				break

	pyb.PeripheralMockManager.pmm_setSocket(sock)
	pyb.PeripheralMockManager.pmm_startReception()
	time.sleep(1)
	print("Start execution")
	fout = file('out.log', 'w')
	sys.stdout = writer()
	sys.stdin = reader()

	execfile(sys.argv[1])
	
else:
	print("ERROR")
	