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
		

class Emulate:

	def __init__(self):
		pass
		
	def start(self,file,port):	
		timeout=3
		while True:
			try:
				sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				server_address = ('localhost', port)
				print("Connecting...")
				sock.connect(server_address)
				break;
			except:
				time.sleep(1)
				timeout-=1
				if timeout==0:
					print("Connection error")
					return False

		pyb.PeripheralMockManager.pmm_setSocket(sock)
		pyb.PeripheralMockManager.pmm_startReception()
		time.sleep(1)
		print("Start execution")
		sys.stdout = writer()
		sys.stdin = reader()
		execfile(file)
		sys.stdout = sys.__stdout__
		sys.stdin = sys.__stdin__
		sock.close()
		return True
	
	