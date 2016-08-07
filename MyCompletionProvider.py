import keyword
import gobject
import gtksourceview2
import gtk
import pprint

TYPE_0 = 0 # from
TYPE_1 = 1 # import
TYPE_2 = 2 # from xxx import 
TYPE_3 = 3 # moduleName.
TYPE_4 = 4 # =
 

class MyCompletionProvider(gobject.GObject, gtksourceview2.CompletionProvider):


    def __init__(self):
        gobject.GObject.__init__(self)
        self.keywordsModules = ["pyb","json","ModBus","os","unittest","utime"]
        self.keywordsClasses = {"pyb":["LED","UART","Switch","Pin","ExtInt","DAC","Timer","PWM","ADC","Keyboard","LCD","EEPROM","SPI","RTC","I2C"],
                                "utime":["time","localtime","mktime","sleep"],
                                "ModBus":["Instrument","Slave"],
                                "unittest":["TestException","TestCase"],
                                "json" : ["dumps","loads"]
                                }
        self.keywordsPython = keyword.kwlist


    def do_get_name(self):
        return 'MicroPython'
	
    def do_get_activation(self):
        return gtksourceview2.COMPLETION_ACTIVATION_USER_REQUESTED

    def do_match(self, context):
        return True

    #def do_get_start_iter(self, context,arg):
    #   return context.get_iter()

    def do_activate_proposal(self, proposal, iter):
        return False


    def do_populate(self, context):
        self.completions = []

        type,word = self.__get_type(context)
        print("type:"+str(type)+" word:"+str(word))

        kwList = []
        if type==TYPE_0 or type==TYPE_1: # from/import: show modules
            kwList = self.keywordsModules

        if type==TYPE_2 : # from xxx import: show classes
            kwList = self.keywordsClasses["pyb"]

        if type==TYPE_3 : # moduleName.: show classes
            modName = word.split(".")[0]
            if modName in self.keywordsClasses:
                kwList = self.keywordsClasses[modName]

        if type==TYPE_4 : # =: show classes and modules
            kwList = self.keywordsModules

        if type==-1: # default
            kwList = self.keywordsPython


        for compl in kwList:
            self.completions.append(gtksourceview2.CompletionItem(compl, compl))
        context.add_proposals(self, self.completions, True)

    def __get_type(self,context):
        end_iter = context.get_iter()
        if end_iter:
            buf = end_iter.get_buffer()
            mov_iter = end_iter.copy()

            iterStart = end_iter.copy()
            iterStart.backward_line()
            if iterStart.get_line()==0:
                iterStart=None

            if mov_iter.backward_search('.', gtk.TEXT_SEARCH_VISIBLE_ONLY,limit=iterStart):
                mov_iter2, _ = mov_iter.backward_search('.', gtk.TEXT_SEARCH_VISIBLE_ONLY,limit=iterStart)
                w = mov_iter2.backward_word_start()
                left_text = buf.get_text(mov_iter2, end_iter, True)
                return TYPE_3,left_text # moduleName.

            if mov_iter.backward_search('=', gtk.TEXT_SEARCH_VISIBLE_ONLY,limit=iterStart):
                mov_iter2, _ = mov_iter.backward_search('=', gtk.TEXT_SEARCH_VISIBLE_ONLY,limit=iterStart)
                left_text = buf.get_text(mov_iter2, end_iter, True)
                if left_text.split(" ")[-1]=="=":
                    return TYPE_4,""
                return TYPE_4,left_text.split(" ")[-1] # =


            if mov_iter.backward_search('from ', gtk.TEXT_SEARCH_VISIBLE_ONLY,limit=iterStart):
                mov_iter2, _ = mov_iter.backward_search('from ', gtk.TEXT_SEARCH_VISIBLE_ONLY,limit=iterStart)
                left_text = buf.get_text(mov_iter2, end_iter, True)
                parts = left_text.split(" ")
                if len(left_text.split(" "))>=3 and left_text.split(" ")[2]=="import":
                    return TYPE_2,parts[3] # from xxx import

            if mov_iter.backward_search('from ', gtk.TEXT_SEARCH_VISIBLE_ONLY,limit=iterStart):
                mov_iter2, _ = mov_iter.backward_search('from ', gtk.TEXT_SEARCH_VISIBLE_ONLY,limit=iterStart)
                left_text = buf.get_text(mov_iter2, end_iter, True)
                return TYPE_0,left_text.split(" ")[-1] # from

            if mov_iter.backward_search('import ', gtk.TEXT_SEARCH_VISIBLE_ONLY,limit=iterStart):
                mov_iter2, _ = mov_iter.backward_search('import ', gtk.TEXT_SEARCH_VISIBLE_ONLY,limit=iterStart)
                left_text = buf.get_text(mov_iter2, end_iter, True)
                return TYPE_1,left_text.split(" ")[-1] # import
            
        return -1,None
