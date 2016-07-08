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






if __name__ == '__main__':
  main()


