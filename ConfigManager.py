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

class ConfigManager(object):

	def __init__(self):
		pass
		
	def readConfig(self):
		parser=SafeConfigParser()
		parser.read('./config.dat')
  
		port = parser.get("Serial","port")
		print("read from file:"+port)
		return {"port":port}
		
		
		
	def writeConfig(self,port):
		config = SafeConfigParser()
		config.add_section("Serial")
		port = config.set("Serial","port",port)
		with open('./config.dat', 'wb') as configfile:
			config.write(configfile)
	