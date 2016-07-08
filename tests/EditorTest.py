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
#   EDU-CIAA Python editor unit tests (2016)
#
#   <ernestogigliotti@gmail.com>
#
########################################################################

from unittest import TestCase, main
import gtk
import time
import sys
import os
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )

from Main import Edile
import Main
Main.BASE_PATH = "."
import ciaa_plugin
from snippets.SnippetsParser import SnippetsParser
from ConfigManager import ConfigManager


# Mock GUI refresh
def refresh_gui(delay=0):
  while gtk.events_pending():
      gtk.main_iteration_do(block=False)
  time.sleep(delay)



class EditorTest(TestCase):

    def setUp(self):
        self.editor = Edile()

    def tearDown(self):
        pass


    def test_openFileOk(self):
        flagOk=False
        try:
            self.editor.load_file("tests/test.py")
            flagOk=True
        except:
            pass
        self.assertEqual(flagOk,True)


    def test_openFileInvalid(self):
        flagOk=False
        try:
            self.editor.load_file("tests/test2.py")
            flagOk=True
        except:
            pass
        self.assertEqual(flagOk,False)


    def test_saveFile(self):
        buff = self.editor.text_view.get_buffer()
        buff.insert_at_cursor("Test String")
        self.editor.write_file("tests/testOut.py")

        self.editor.load_file("tests/testOut.py")
        text = buff.get_text(buff.get_start_iter(), buff.get_end_iter())

        self.assertEqual("Test String",text)






class SnippetsWindowTest(TestCase):

    def setUp(self):
        self.editor = Edile()

    def tearDown(self):
        pass

    def test_openSnippets(self):
        plugin = ciaa_plugin.mnu_EDUCIAA()
        plugin.item_Snippets(None,self.editor.plugin_interface)
        plugin.snippetsW.listW.set_cursor(1) # select 2nd snippet
        buff = plugin.snippetsW.txtSrc.get_buffer()
        text = buff.get_text(buff.get_start_iter(), buff.get_end_iter())

        #compare text inserted in text field snippets window
        self.assertEqual("#Number to String example\n# Integer variable\nn = 5\n#n to String\nnString = str(n)\nprint(nString)\t\t\n#___________",text)

    def test_addSnippet(self):
        plugin = ciaa_plugin.mnu_EDUCIAA()
        plugin.item_Snippets(None,self.editor.plugin_interface)
        plugin.snippetsW.listW.set_cursor(1) # select 2nd snippet
        plugin.snippetsW.buttonOk.clicked()

        #compare text inserted in editor
        buff = self.editor.text_view.get_buffer()
        text = buff.get_text(buff.get_start_iter(), buff.get_end_iter())
        self.assertEqual("#Number to String example\n# Integer variable\nn = 5\n#n to String\nnString = str(n)\nprint(nString)\t\t\n#___________",text)


class SnippetsParserTest(TestCase):

    def setUp(self):
        self.parser = SnippetsParser()

    def tearDown(self):
        pass

    def test_parse(self):
        root = self.parser.parseSnippets(Main.BASE_PATH+'/tests/snippetsTest.xml')
        i=1
        for child in root:
            self.assertEqual("test"+str(i),child.attrib["name"])
            self.assertEqual("test content "+str(i),child.text)
            i+=1



class ConfigWindowTest(TestCase):

    def setUp(self):
        self.editor = Edile()

    def tearDown(self):
        pass

    def test_openConfig(self):
        plugin = ciaa_plugin.mnu_EDUCIAA()
        plugin.item_Configuration(None,self.editor.plugin_interface)
        portsLen = len(plugin.configW.ports)
        self.assertGreater(portsLen,0,"Amount of serial ports in the system.")


    def test_selectPort(self):
        plugin = ciaa_plugin.mnu_EDUCIAA()
        plugin.item_Configuration(None,self.editor.plugin_interface)
        plugin.configW.buttonOk.clicked()

        ps = plugin.configW.portSelected

        self.assertEquals("/dev/tty",ps[0:8])


class ConfigManagerTest(TestCase):

    def setUp(self):
        self.cm = ConfigManager()


    def test_write(self):
        flagOk=False
        try:
            self.cm.writeConfig("/dev/ttyUSB1")
            flagOk=True
        except:
            pass

        self.assertEqual(True,flagOk)


    def test_read(self):

        conf = self.cm.readConfig()

        self.assertEqual("/dev/ttyUSB1",conf["port"])




if __name__ == '__main__':
  main()


