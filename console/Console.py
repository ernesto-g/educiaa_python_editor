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

import gtk 
import pango
import serial
import threading
import struct
import time
import datetime

class Console(gtk.Window):
	def __init__(self,basePath):
		super(Console, self).__init__()
		self.connect("destroy", self.__closeConsole)
		self.connect('key_press_event', self.__onKeyPressEvent)
		self.set_size_request(600, 400)
		self.set_position(gtk.WIN_POS_CENTER)
		self.set_title("EDU-CIAA Serial Console")
		self.set_icon_from_file(basePath+"/icons/icon.ico")
		
		sw = gtk.ScrolledWindow()
		self.sw=sw
		sw.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
		textview = gtk.TextView()
		textview.set_editable(False)
		textview.modify_base(gtk.STATE_NORMAL, gtk.gdk.color_parse('black'))
		textview.modify_text(gtk.STATE_NORMAL, gtk.gdk.color_parse('white'))
		textview.connect("size-allocate", self._autoscroll)
		font = pango.FontDescription('Monospace 10')
		textview.set_cursor_visible(False)
		textview.modify_font(font)
		
		self.textbuffer = textview.get_buffer()
		sw.add(textview)
		sw.show()
		textview.show()
		textview.get_buffer().set_text("")
		self.add(sw)
		self.ser=None
		self.thread=None
		
		
	def showConsole(self,portPath,serialMock=None):	
		self.show()
		print("Opening:"+portPath)		
		try:
			if serialMock!=None:
				self.ser = serialMock
			else:
				self.ser = serial.Serial(port=portPath,baudrate=115200,timeout = 1)	
			self.thread = threading.Thread(target=self.__receptionThread, args=())
			self.thread.start()
		except serial.SerialException, e:			
			print(e)
			return False
		return True

	def addText(self,text):
		end_iter = self.textbuffer.get_end_iter()
		self.textbuffer.insert(end_iter, text)	

	def removeText(self):
		end_iter = self.textbuffer.get_end_iter()
		start_iter = self.textbuffer.get_end_iter()
		start_iter.backward_chars(1);
		self.textbuffer.delete(start_iter, end_iter)
		
	def removeTextLastLine(self):
		end_iter = self.textbuffer.get_end_iter()
		line_count = self.textbuffer.get_line_count()		
		start_iter = self.textbuffer.get_iter_at_line(line_count-1)
		
		self.textbuffer.delete(start_iter, end_iter)		
		self.addText(">>> ")
		
	def __closeConsole(self,arg):
		self.closeConsole()
		
	def closeConsole(self):		

		if self.ser!=None:
			self.ser.close()
			time.sleep(0.5)
			self.ser=None
		self.destroy()
			
	def __receptionThread(self):
		ignoreCounter=0
		flagReceivingSpecial=False
		special=""
		while True:
			try:
				x = self.ser.read()
			except Exception,e:
				print(e)
				break
			
			if x!=-1 and x!="":
							
				gtk.gdk.threads_enter()
				ignoreCounter-=1

				if(flagReceivingSpecial==False and ord(x)==27):
					flagReceivingSpecial=True
					special=""
				
				if(flagReceivingSpecial):
					if(ord(x)!=27):
						special=special+x
					
					if(special=="[K"):
						#print("<ESC>[K")
						self.removeText()
						flagReceivingSpecial=False
						
					try:
						if(special[len(special)-1]=="D"):
							columns =  special[1:len(special)-1]
							#print("Columns:"+str(columns))
							self.removeTextLastLine()
							flagReceivingSpecial=False
					except: pass
					
				else:
					if(ord(x)==8):
						#self.removeText()
						pass
					elif(ord(x)==0x15):
						today = datetime.date.today()
						self.addText(datetime.datetime.now().strftime(">>> EDUCIAA Reboot. %d-%m-%Y %H:%M:%S\r\n"))
					else:
						self.addText(x)
					
				gtk.gdk.threads_leave()

		
	def __onKeyPressEvent(self, widget, event):
		try:
			if(gtk.gdk.keyval_name (event.keyval)=="Return"):
				self.ser.write("\r\n")
			elif(gtk.gdk.keyval_name (event.keyval)=="BackSpace"):
				self.ser.write("\b")
			elif(gtk.gdk.keyval_name (event.keyval)=="Up"):
				self.removeTextLastLine()
				self.ser.write("\x1b[A")				
			elif(gtk.gdk.keyval_name (event.keyval)=="Down"):
				self.removeTextLastLine()
				self.ser.write("\x1b[B")
			elif(gtk.gdk.keyval_name (event.keyval)=="Left"):
				#self.ser.write("\x1b[D")
				pass
			elif(gtk.gdk.keyval_name (event.keyval)=="Right"):
				#self.ser.write("\x1b[C")				
				pass
			else:	
				self.ser.write(struct.pack('!B',event.keyval))
		except:
			pass
		
	def _autoscroll(self, *args):
		adj = self.sw.get_vadjustment()
		adj.set_value(adj.get_upper() - adj.get_page_size())
		