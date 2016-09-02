#!/usr/bin/env python

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
# -----------------------------------------------------------------------------
#
# This is Edile: A PyGTK+ text editor.
# http://edile.googlecode.com

# Edile is a basic but useful text editor implemented in one source code file.
# It requires only PyGTK but if you have pygtksourceview2 installed it will use that.
#
# This file is based on part of the tutorial: Linux GUI Programming with GTK+ and Glade3
# http://www.micahcarrick.com/12-24-2007/gtk-glade-tutorial-part-1.html
#
#	EDU-CIAA Python editor (2015)
#					
#	<ernestogigliotti@gmail.com>
#
########################################################################

# edit default configuration here
#=======================================================================

import sys
import os
BASE_PATH,filename = os.path.split(sys.argv[0])
if(BASE_PATH==""):
    BASE_PATH="."

	
CONF_FONT                           =       "monospace 10"
CONF_HIGHLIGHT_CURRENT_LINE         =       True
CONF_HIGHLIGHT_MATCHING_BRACKETS    =       True
CONF_OVERWRITE                      =       False              # insert/overwrite mode
CONF_SHOW_LINE_NUMBERS              =       True
CONF_AUTO_INDENT                    =       True
CONF_INDENT_ON_TAB                  =       True
CONF_SHOW_RIGHT_MARGIN              =       True
CONF_RIGHT_MARGIN_POSITION          =       72
CONF_HIGHLIGHT_SYNTAX               =       True
CONF_SPACES_INSTEAD_OF_TABS         =       True
CONF_TAB_WIDTH                      =       4
CONF_INDENT_WIDTH                   =       -1                  # -1 means use same as tab width
CONF_MAX_UNDO_LEVELS                =       50                  # -1 means no limit

CONF_HIGHLIGHT_CHANGES_SINCE_SAVE   =       True

# color for highlighting changes since last save
CONF_CHANGE_HIGHLIGHT               =       "dark slate gray"      # from /etc/X11/rgb.txt

# color for highlighting find/replace matches
CONF_FIND_HIGHLIGHT                 =       "IndianRed4"

# gtksrcview color scheme
CONF_STYLE_SCHEME                   =       ("oblivion","kate","tango","classic")

# 'note pad'. will open this file on startup instead of untitled. empty string means no default file.
CONF_DEFAULT_FILE                   =       ""

# whether or not to load plugins. off by default.
# plugins provide a way for you to customise edile for your purpose or environment
# without changing the application's source code.
CONF_LOAD_PLUGINS                   =       True

# whether to load plugins when running as the super user. 'no' by default.
CONF_LOAD_PLUGINS_AS_ROOT           =       True

# url of file to load plugins from. any scheme should work (e.g. file:///, http://)
# default is http://edile.googlecode.com/files/edile_plugins-0.1.8.py
# see that file for a description of the plugin interface.
# as of version 0.1.8 options can also be set from that file.
#CONF_PLUGIN_LOCATION             =       "ciaa_plugin.py"
# sha 256 hash of the plugin file for authentication. empty string means no authentication.
CONF_PLUGIN_SHA256               =       ""

# move whichever you want as default into the first position
CONF_WRAP                           =   ('None','Character','Word')
CONF_SMART_HOME_END_TYPE            =   ('Before','Disabled','After','Always')

#=======================================================================
# end configuration

# stuff here you probably shouldn't edit
#=======================================================================
EDILE_VERSION = '1.4'
EDILE_URL = 'https://github.com/ernesto-g/educiaa_python_editor'
EDILE_NAME = 'EDU-CIAA Python Editor'
EDILE_DESCRIPTION = 'Editor based on EDILE 0.2 http://edile.googlecode.com '
#=======================================================================

# here begins the program edile

# TODO: command line options (verbosity, language, conf options)
#       improve find code. handle everything internal to edile w/o relying on gtksrcview features eg. case sensitivity
#       config option for encoding to use when saving file instead of always file's encoding
#		generally firm everything up. condense and refactor code, exception handling, etc.

# UI definition. GTK builder XML string
U_I = '''
<?xml version="1.0"?>
<interface>
  <object class="GtkUIManager" id="uimanager1">
    <child>
      <object class="GtkActionGroup" id="actiongroup1">
        <child>
          <object class="GtkAction" id="file_menu">
            <property name="name">file_menu</property>
            <property name="label" translatable="yes">_File</property>
          </object>
        </child>
        <child>
          <object class="GtkAction" id="new_menu_item">
            <property name="stock_id">gtk-new</property>
            <property name="name">new_menu_item</property>
            <property name="label" translatable="yes">_New</property>
            <signal handler="on_new_menu_item_activate" name="activate"/>
          </object>
        </child>
        
        <child>
          <object class="GtkAction" id="open_menu_item">
            <property name="stock_id">gtk-open</property>
            <property name="name">open_menu_item</property>
            <property name="label" translatable="yes">_Open</property>
            <signal handler="on_open_menu_item_activate" name="activate"/>
          </object>
        </child>

       <child>
          <object class="GtkAction" id="save_menu_item">
            <property name="stock_id">gtk-save</property>
            <property name="name">save_menu_item</property>
            <property name="label" translatable="yes">_Save</property>
            <signal handler="on_save_menu_item_activate" name="activate"/>
          </object>
        </child>
        <child>
          <object class="GtkAction" id="save_as_menu_item">
            <property name="stock_id">gtk-save-as</property>
            <property name="name">save_as_menu_item</property>
            <property name="label" translatable="yes">Save _As</property>
            <signal handler="on_save_as_menu_item_activate" name="activate"/>
          </object>
        </child>
        <child>
          <object class="GtkAction" id="reload_menu_item">
            <property name="stock_id">gtk-reload</property>
            <property name="name">reload_menu_item</property>
            <property name="label" translatable="yes">Reload</property>
            <signal handler="on_reload_menu_item_activate" name="activate"/>
          </object>
        </child>

        <child>
          <object class="GtkAction" id="close_menu_item">
            <property name="stock_id">gtk-close</property>
            <property name="name">close_menu_item</property>
            <property name="label" translatable="yes">_Close</property>
            <signal handler="on_close_menu_item_activate" name="activate"/>
          </object>
        </child>
        <child>
          <object class="GtkAction" id="quit_menu_item">
            <property name="stock_id">gtk-quit</property>
            <property name="name">quit_menu_item</property>
            <property name="label" translatable="yes">_Quit</property>
            <signal handler="on_quit_menu_item_activate" name="activate"/>
          </object>
        </child>
        <child>
          <object class="GtkAction" id="edit_menu">
            <property name="name">edit_menu</property>
            <property name="label" translatable="yes">_Edit</property>
          </object>
        </child>
        <child>
          <object class="GtkAction" id="undo_menu_item">
            <property name="stock_id">gtk-undo</property>
            <property name="name">undo_menu_item</property>
            <property name="label" translatable="yes">_Undo</property>
            <signal handler="on_undo_menu_item_activate" name="activate"/>
          </object>
        <accelerator key="Z" modifiers="GDK_CONTROL_MASK"/>
        </child>
        <child>
          <object class="GtkAction" id="redo_menu_item">
            <property name="stock_id">gtk-redo</property>
            <property name="name">redo_menu_item</property>
            <property name="label" translatable="yes">_Redo</property>
            <signal handler="on_redo_menu_item_activate" name="activate"/>
          </object>
        <accelerator key="Z" modifiers="GDK_CONTROL_MASK|GDK_SHIFT_MASK"/>
        </child>
        <child>
          <object class="GtkAction" id="cut_menu_item">
            <property name="stock_id">gtk-cut</property>
            <property name="name">cut_menu_item</property>
            <property name="label" translatable="yes">Cu_t</property>
            <signal handler="on_cut_menu_item_activate" name="activate"/>
          </object>
        </child>
        <child>
          <object class="GtkAction" id="copy_menu_item">
            <property name="stock_id">gtk-copy</property>
            <property name="name">copy_menu_item</property>
            <property name="label" translatable="yes">_Copy</property>
            <signal handler="on_copy_menu_item_activate" name="activate"/>
          </object>
        </child>
        <child>
          <object class="GtkAction" id="paste_menu_item">
            <property name="stock_id">gtk-paste</property>
            <property name="name">paste_menu_item</property>
            <property name="label" translatable="yes">_Paste</property>
            <signal handler="on_paste_menu_item_activate" name="activate"/>
          </object>
        </child>
        <child>
          <object class="GtkAction" id="select_all_menu_item">
            <property name="stock_id">gtk-select-all</property>
            <property name="name">select_all_menu_item</property>
            <property name="label" translatable="yes">Select _All</property>
            <signal handler="on_select_all_menu_item_activate" name="activate"/>
          </object>
        <accelerator key="A" modifiers="GDK_CONTROL_MASK"/>
        </child>
        <child>
          <object class="GtkAction" id="delete_menu_item">
            <property name="stock_id">gtk-delete</property>
            <property name="name">delete_menu_item</property>
            <property name="label" translatable="yes">_Delete</property>
            <signal handler="on_delete_menu_item_activate" name="activate"/>
          </object>
        </child>
         <child>
          <object class="GtkAction" id="search_menu">
            <property name="name">search_menu</property>
            <property name="label" translatable="yes">_Search</property>
          </object>
        </child>
        <child>
          <object class="GtkAction" id="find_prev_selected_menu_item">
            <property name="name">find_prev_selected_menu_item</property>
            <property name="label" translatable="yes">Find Previous Selected</property>
            <signal handler="on_find_prev_selected_menu_item_activate" name="activate"/>
          </object>
        <accelerator key="E" modifiers="GDK_CONTROL_MASK"/>
        </child>
        <child>
          <object class="GtkAction" id="find_next_selected_menu_item">
            <property name="name">find_next_selected_menu_item</property>
            <property name="label" translatable="yes">Find Next Selected</property>
            <signal handler="on_find_next_selected_menu_item_activate" name="activate"/>
          </object>
        <accelerator key="D" modifiers="GDK_CONTROL_MASK"/>
        </child>
        <child>
          <object class="GtkAction" id="show_find_menu_item">
            <property name="stock_id">gtk-find</property>
            <property name="name">show_find_menu_item</property>
            <property name="label" translatable="yes">_Find &amp; Replace</property>
            <signal handler="on_show_find_menu_item_activate" name="activate"/>
          </object>
        <accelerator key="F" modifiers="GDK_CONTROL_MASK"/>
        </child>
        <child>
          <object class="GtkAction" id="find_next_menu_item">
            <property name="stock_id">gtk-go-forward</property>
            <property name="name">find_next_menu_item</property>
            <property name="label" translatable="yes">Find _Next</property>
            <signal handler="on_find_next_menu_item_activate" name="activate"/>
          </object>
        <accelerator key="G" modifiers="GDK_CONTROL_MASK"/>
        </child>
        <child>
          <object class="GtkAction" id="find_previous_menu_item">
            <property name="stock_id">gtk-go-back</property>
            <property name="name">find_previous_menu_item</property>
            <property name="label" translatable="yes">Find _Previous</property>
            <signal handler="on_find_previous_menu_item_activate" name="activate"/>
          </object>
          <accelerator key="G" modifiers="GDK_CONTROL_MASK|GDK_SHIFT_MASK"/>
        </child>
        <child>
          <object class="GtkAction" id="find_all_menu_item">
            <property name="name">find_all_menu_item</property>
            <property name="label" translatable="yes">Find All</property>
            <signal handler="on_find_all_menu_item_activate" name="activate"/>
          </object>
          <!--<accelerator key="F" modifiers="GDK_CONTROL_MASK|GDK_SHIFT_MASK"/>-->
        </child>
        <!-- <child>
          <object class="GtkAction" id="replace_next_menu_item">
          <property name="stock_id">gtk-find-and-replace</property>
           <property name="name">replace_next_menu_item</property>
            <property name="label" translatable="yes">Replace Next</property>
            <signal handler="on_replace_next_menu_item_activate" name="activate"/>
          </object>
          <accelerator key="G" modifiers="GDK_CONTROL_MASK|GDK_SHIFT_MASK|GDK_MOD1_MASK"/>
        </child> -->
        <child>
          <object class="GtkAction" id="replace_all_menu_item">
            <property name="name">replace_all_menu_item</property>
            <property name="label" translatable="yes">Replace All</property>
            <signal handler="on_replace_all_menu_item_activate" name="activate"/>
          </object>
        </child>
       <child>
          <object class="GtkAction" id="view_menu">
            <property name="name">view_menu</property>
            <property name="label" translatable="yes">_View</property>
          </object>
        </child>
       <child>
          <object class="GtkAction" id="wrap_menu">
            <property name="name">wrap_menu</property>
            <property name="label" translatable="yes">W_rap</property>
          </object>
        </child>
        <child>
          <object class="GtkRadioAction" id="wrap_none_menu_item">
            <property name="name">wrap_none_menu_item</property>
            <property name="label" translatable="yes">_None</property>
            <!--<property name="group">wrap_none_menu_item</property>-->
            <signal handler="on_wrap_none_menu_item_activate" name="activate"/>
          </object>
        </child>
        <child>
          <object class="GtkRadioAction" id="wrap_char_menu_item">
            <property name="name">wrap_char_menu_item</property>
            <property name="label" translatable="yes">_Character</property>
            <property name="group">wrap_none_menu_item</property>
            <signal handler="on_wrap_char_menu_item_activate" name="activate"/>
          </object>
        </child>
        <child>
          <object class="GtkRadioAction" id="wrap_word_menu_item">
            <property name="name">wrap_word_menu_item</property>
            <property name="label" translatable="yes">_Word</property>
            <property name="group">wrap_none_menu_item</property>
            <signal handler="on_wrap_word_menu_item_activate" name="activate"/>
          </object>
        </child>
        <child>
          <object class="GtkAction" id="select_font_menu_item">
            <property name="name">select_font_menu_item</property>
            <property name="label" translatable="yes">Select Font...</property>
            <signal handler="on_select_font_menu_item_activate" name="activate"/>
          </object>
        </child>
        <child>
          <object class="GtkAction" id="help_menu">
            <property name="name">help_menu</property>
            <property name="label" translatable="yes">_Help</property>
          </object>
        </child>
		
         
       <child>
          <object class="GtkAction" id="about_menu_item">
            <property name="stock_id">gtk-about</property>
            <property name="name">about_menu_item</property>
            <property name="label" translatable="yes">_About</property>
            <signal handler="on_about_menu_item_activate" name="activate"/>
          </object>  
        </child>
       <child>
          <object class="GtkAction" id="help_menu_item">
            <property name="stock_id">gtk-help</property>
            <property name="name">help_menu_item</property>
            <property name="label" translatable="yes">_Help</property>
            <signal handler="on_help_menu_item_activate" name="activate"/>
          </object>  
        </child>		

		
      </object>
    </child>
    <ui>
      <menubar name="menubar1">
        <menu action="file_menu">
          <menuitem action="new_menu_item"/>
          
          <separator/>
          <menuitem action="open_menu_item"/>
          <!-- <menuitem action="open_in_new_window_menu_item"/> -->
          <separator/>
          <menuitem action="save_menu_item"/>
          <menuitem action="save_as_menu_item"/>
          <separator/>
          <menuitem action="reload_menu_item"/>
          <!-- <menuitem action="execute_menu_item"/> -->
          <separator/>
          <menuitem action="close_menu_item"/>
          <menuitem action="quit_menu_item"/>
        </menu>
        <menu action="edit_menu">
          <menuitem action="undo_menu_item"/>
          <menuitem action="redo_menu_item"/>
          <separator/>
          <menuitem action="cut_menu_item"/>
          <menuitem action="copy_menu_item"/>
          <menuitem action="paste_menu_item"/>
          <menuitem action="select_all_menu_item"/>
          <separator/>
          <menuitem action="delete_menu_item"/>
        </menu>
        <menu action="search_menu">
          <menuitem action="find_prev_selected_menu_item"/>
          <menuitem action="find_next_selected_menu_item"/>
          <separator/>
          <menuitem action="show_find_menu_item"/>
          <menuitem action="find_next_menu_item"/>
          <menuitem action="find_previous_menu_item"/>
          <menuitem action="find_all_menu_item"/>
          <separator/>
          <!--<menuitem action="replace_next_menu_item"/>-->
          <menuitem action="replace_all_menu_item"/>
        </menu>
        <menu action="view_menu">
          <menu action="wrap_menu">
          <menuitem action="wrap_none_menu_item"/>
          <menuitem action="wrap_char_menu_item"/>
          <menuitem action="wrap_word_menu_item"/>
          </menu>
          <separator/>
          <menuitem action="select_font_menu_item"/>
        </menu>
        <menu action="help_menu">
          <!-- <menuitem action="view_source_menu_item"/> -->
          <menuitem action="help_menu_item"/>
		  <menuitem action="about_menu_item"/>
        </menu>
      </menubar>
    </ui>
  </object>
  <object class="GtkWindow" id="window">
    <property name="events">GDK_POINTER_MOTION_MASK | GDK_POINTER_MOTION_HINT_MASK | GDK_BUTTON_PRESS_MASK | GDK_BUTTON_RELEASE_MASK</property>
    <property name="title" translatable="yes">EduCIAA Python Editor</property>
    <property name="default_width">540</property>
    <property name="default_height">660</property>
    <signal handler="on_window_destroy" name="destroy"/>
    <signal handler="on_window_delete_event" name="delete_event"/>
    <child>
      <object class="GtkVBox" id="vbox1">
        <property name="visible">True</property>
        <property name="events">GDK_POINTER_MOTION_MASK | GDK_POINTER_MOTION_HINT_MASK | GDK_BUTTON_PRESS_MASK | GDK_BUTTON_RELEASE_MASK</property>        
		<child>
          <object class="GtkMenuBar" constructor="uimanager1" id="menubar1">
            <property name="visible">True</property>
            <property name="events">GDK_POINTER_MOTION_MASK | GDK_POINTER_MOTION_HINT_MASK | GDK_BUTTON_PRESS_MASK | GDK_BUTTON_RELEASE_MASK</property>			
          </object>
          <packing>
            <property name="expand">False</property>
          </packing>
        </child>
		<child>
			<object class="GtkVBox" id="vbox2">
				<property name="visible">True</property>								
			</object>
			<packing>
				<property name="expand">False</property>
            </packing>			
		</child>		
        <child>
          <object class="GtkScrolledWindow" id="scrolledwindow">
            <property name="visible">True</property>
            <property name="can_focus">True</property>
            <property name="events">GDK_POINTER_MOTION_MASK | GDK_POINTER_MOTION_HINT_MASK | GDK_BUTTON_PRESS_MASK | GDK_BUTTON_RELEASE_MASK</property>
            <property name="border_width">0</property>
            <property name="hscrollbar_policy">GTK_POLICY_AUTOMATIC</property>
            <property name="vscrollbar_policy">GTK_POLICY_AUTOMATIC</property>
            <property name="shadow_type">GTK_SHADOW_ETCHED_IN</property>
            <child>
                <object class="GtkTextView" id="text_view">
                <property name="visible">True</property>
                <property name="can_focus">True</property>
                <property name="events">GDK_POINTER_MOTION_MASK | GDK_POINTER_MOTION_HINT_MASK | GDK_BUTTON_PRESS_MASK | GDK_BUTTON_RELEASE_MASK</property>
                <property name="left_margin">2</property>
                <property name="right_margin">2</property>
                <property name="wrap_mode">GTK_WRAP_NONE</property>
                <!--<signal handler="on_text_view_insert_at_cursor" name="insert-at-cursor"/>-->
                <!--<signal name="drag_data_received" handler="on_log_drag_data_received"/>-->
              </object>
            </child>
          </object>
          <packing>
            <property name="position">2</property>
          </packing>
        </child>
        <child>
          <object class="GtkStatusbar" id="statusbar">
            <property name="visible">True</property>
            <property name="events">GDK_POINTER_MOTION_MASK | GDK_POINTER_MOTION_HINT_MASK | GDK_BUTTON_PRESS_MASK | GDK_BUTTON_RELEASE_MASK</property>
            <property name="spacing">2</property>
          </object>
          <packing>
            <property name="expand">False</property>
            <property name="position">3</property>
          </packing>
        </child>
      </object>
    </child>
  </object>
</interface>
'''

# for the search ui, because it was easier this way.
SEARCH_UI = '''
<?xml version="1.0"?>
<interface>
<!-- search ui -->
<object class="GtkWindow" id="search_window">
    <signal handler="on_search_window_delete_event" name="delete_event"/>
    <property name="skip-taskbar-hint">True</property>

<child>
      <object class="GtkVBox" id="vbox9">


        <property name="visible">True</property>
        <property name="orientation">GTK_ORIENTATION_VERTICAL</property>
        <property name="orientation">GTK_ORIENTATION_VERTICAL</property>
        <child>
          <object class="GtkHBox" id="hbox1">
            <property name="visible">True</property>
            <child>
              <object class="GtkLabel" id="label1">
                <property name="visible">True</property>
                <property name="label" translatable="yes">Find</property>
                <property name="justify">GTK_JUSTIFY_RIGHT</property>
              </object>
            </child>
            <child>
              <object class="GtkEntry" id="search_find_field">
                <property name="visible">True</property>
                <property name="can_focus">True</property>
                <property name="invisible_char">&#x25CF;</property>
                <signal handler="search_find_field_changed" name="changed"/>
              </object>
              <packing>
                <property name="position">1</property>
              </packing>
            </child>
          </object>
        </child>
        <child>
          <object class="GtkHBox" id="hbox2">
            <property name="visible">True</property>
            <child>
              <object class="GtkLabel" id="label2">
                <property name="visible">True</property>
                <property name="label" translatable="yes">Replace</property>
                <property name="justify">GTK_JUSTIFY_RIGHT</property>
              </object>
            </child>
            <child>
              <object class="GtkEntry" id="search_replace_field">
                <property name="visible">True</property>
                <property name="can_focus">True</property>
                <property name="invisible_char">&#x25CF;</property>
                <signal handler="search_replace_field_changed" name="changed"/>
              </object>
              <packing>
                <property name="position">1</property>
              </packing>
            </child>
          </object>
          <packing>
            <property name="position">1</property>
          </packing>
        </child>
        <child>
          <object class="GtkCheckButton" id="search_whole_word_checkbox">
            <property name="visible">True</property>
            <property name="can_focus">True</property>
            <property name="label" translatable="yes">Whole word</property>
            <property name="draw_indicator">True</property>
            <signal handler="on_search_whole_word_checkbox_toggled" name="toggled"/>
          </object>
          <packing>
            <property name="position">2</property>
          </packing>
        </child>
        <child>
          <object class="GtkCheckButton" id="search_case_sensitive_checkbox">
            <property name="visible">True</property>
            <property name="can_focus">True</property>
            <property name="label" translatable="yes">Case sensitive</property>
            <property name="draw_indicator">True</property>
            <!--<property name="active">True</property>-->
            <signal handler="on_search_case_sensitive_checkbox_toggled" name="toggled"/>
         </object>
          <packing>
            <property name="position">3</property>
          </packing>
        </child>
        <child>
          <object class="GtkHSeparator" id="hseparator1">
            <property name="visible">True</property>
          </object>
          <packing>
            <property name="expand">False</property>
            <property name="position">4</property>
          </packing>
        </child>
        <child>
          <object class="GtkHBox" id="hbox3">
            <property name="visible">True</property>
            <child>
              <object class="GtkButton" id="search_close_button">
                <property name="visible">True</property>
                <property name="can_focus">True</property>
                <property name="receives_default">True</property>
                <property name="label" translatable="yes">Close</property>
                <signal handler="on_search_window_delete_event" name="clicked"/>
              </object>
            </child>
            <child>
              <object class="GtkButton" id="search_find_previous_button">
                <property name="visible">True</property>
                <property name="can_focus">True</property>
                <property name="receives_default">True</property>
                <property name="label" translatable="yes">Find Previous</property>
                <signal handler="on_find_previous_menu_item_activate" name="clicked"/>
              </object>
              <packing>
                <property name="position">1</property>
              </packing>
            </child>
            <child>
              <object class="GtkButton" id="search_find_next_button">
                <property name="visible">True</property>
                <property name="can_focus">True</property>
                <property name="receives_default">True</property>
                <property name="label" translatable="yes">Find Next</property>
                <signal handler="on_find_next_menu_item_activate" name="clicked"/>
              </object>
              <packing>
                <property name="position">2</property>
              </packing>
            </child>
            <child>
              <object class="GtkButton" id="search_replace_and_find_button">
                <property name="visible">True</property>
                <property name="can_focus">True</property>
                <property name="receives_default">True</property>
                <property name="label" translatable="yes">Find &amp; Replace</property>
                <signal handler="on_replace_and_find_menu_item_activate" name="clicked"/>
              </object>
              <packing>
                <property name="position">3</property>
              </packing>
            </child>
          </object>
          <packing>
            <property name="position">5</property>
          </packing>
        </child>
      </object>
      </child>
      </object>
</interface>
'''




import imp,types,tempfile
import string
#import urlparse
import urllib
#import platform
#import gio #this breaks windows
import gtk,gobject
#import gtk

import pango
import subprocess
import hashlib
import webbrowser

from ConfigManager import ConfigManager
import ciaa_plugin
from optparse import OptionParser
import time

from tips.TipsWindow import TipsWindow

gtk.rc_parse(BASE_PATH+'/themes/Mac4Lin_GTK_v0.4/gtk-2.0/gtkrc')

# prints about info from global vars to console
def print_about():
    print "\n%s %s\n%s\n%s"%(EDILE_NAME,EDILE_VERSION,EDILE_URL,EDILE_DESCRIPTION)

print_about()

import gtksourceview2
using_source_view = True

# names for text wrapping types
CONF_WRAP_MAP = {'None':gtk.WRAP_NONE,'Character':gtk.WRAP_CHAR, 'Word':gtk.WRAP_WORD, 'Word Character':gtk.WRAP_WORD_CHAR}

if using_source_view:
    # names for gtksourceview smart home end types
    CONF_SMART_HOME_END_TYPE_MAP =  {'Disabled':gtksourceview2.SMART_HOME_END_DISABLED,'Before':gtksourceview2.SMART_HOME_END_BEFORE,'After':gtksourceview2.SMART_HOME_END_AFTER,'Always':gtksourceview2.SMART_HOME_END_ALWAYS}


#__________________________Auto complete ___________________________________________________
"""
import keyword
class MyCompletionProvider(gobject.GObject, gtksourceview2.CompletionProvider):
	def __init__(self):
		gobject.GObject.__init__(self)

	def do_get_name(self):
		return 'PythonKeywords'

	def do_get_activation(self):
		return gtksourceview2.COMPLETION_ACTIVATION_USER_REQUESTED

	def do_match(self, context):
		return True

	#def do_get_start_iter(self, context,arg):
	#	return context.get_iter()

	def do_activate_proposal(self, proposal, iter):
		return True

	def do_populate(self, context):
		self.completions = []

		end_iter = context.get_iter()

		if end_iter:
			buf = end_iter.get_buffer()
			mov_iter = end_iter.copy()
			if mov_iter.backward_search('=', gtk.TEXT_SEARCH_VISIBLE_ONLY):
				mov_iter, _ = mov_iter.backward_search('=', gtk.TEXT_SEARCH_VISIBLE_ONLY)
				left_text = buf.get_text(mov_iter, end_iter, True)
				left_text = left_text[0:len(left_text)-1]
			else:
				left_text = ''
		print("texto:"+left_text)
		for compl in keyword.kwlist:
			self.completions.append(gtksourceview2.CompletionItem(compl, compl))
		context.add_proposals(self, self.completions, True)
"""
from MyCompletionProvider import MyCompletionProvider
gobject.type_register(MyCompletionProvider)
#_____________________________________________________________________________


class splashScreen():     
    def __init__(self):        
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title('Your app name')
        self.window.set_position(gtk.WIN_POS_CENTER)
        self.window.set_decorated(0)
        self.window.set_default_size(640, 350)
        main_vbox = gtk.VBox(False, 1) 
        self.window.add(main_vbox)
        hbox = gtk.HBox(False, 0)
        #self.lbl = gtk.Label("This shouldn't take too long... :)")
        #self.lbl.set_alignment(0, 0.5)
        self.image = gtk.Image()
        self.image.set_from_file(BASE_PATH+"/splash.png")
        #main_vbox.pack_start(self.lbl, True, True)
        main_vbox.pack_start(self.image, True, True)
        self.window.show_all()
		
class Edile:

###
# on_* = action methods from ui
###

    # Called when the user clicks the 'About' menu. We use gtk_show_about_dialog()
    # which is a convenience function to show a GtkAboutDialog. This dialog will
    # NOT be modal but will be on top of the main application window.
    def on_about_menu_item_activate(self, menuitem, data=None):

        # show standard gtk about window
        def show_about():
            if self.about_dialog:
                self.about_dialog.present()
                return


            about_dialog = gtk.AboutDialog()
            about_dialog.set_transient_for(self.window)
            about_dialog.set_destroy_with_parent(True)
            about_dialog.set_name(EDILE_NAME)
            about_dialog.set_version(EDILE_VERSION)
            about_dialog.set_copyright("")
            about_dialog.set_website(EDILE_URL)
            about_dialog.set_comments(EDILE_DESCRIPTION)
            #about_dialog.set_authors(EDILE_AUTHORS)
            #about_dialog.set_logo_icon_name(gtk.STOCK_EDIT)	
            img = gtk.gdk.pixbuf_new_from_file_at_size(os.path.join(BASE_PATH,"splash.png"), 80, 45)
            about_dialog.set_logo(img)

            # callbacks for destroying the about dialog
            def close(dialog, response, editor):
                editor.about_dialog = None
                dialog.destroy()

            def delete_event(dialog, event, editor):
                editor.about_dialog = None
                return True

            about_dialog.connect("response", close, self)
            about_dialog.connect("delete-event", delete_event, self)

            self.about_dialog = about_dialog
            about_dialog.show()

        # run functions
        print_about()
        show_about()

    def on_help_menu_item_activate(self, menuitem, data=None):
        webbrowser.open_new("http://www.proyecto-ciaa.com.ar/devwiki/doku.php?id=desarrollo:edu-ciaa:edu-ciaa-nxp:python:comenzar_programar")

    '''		
    # view source. displays this file in a new instance.
    def on_view_source_menu_item_activate(self, menuitem, data=None):
        exe = __file__
        exepath = os.path.realpath(exe)
        self.spawn(exepath)
    '''
    '''
    # tries to run file in a terminal
    def on_execute_menu_item_activate(self,menuitem,data=None):
        exe = self.filename

        if exe == None:
            self.error_message("Save file first!")
            return

        if os.path.exists(exe):
            exepath = os.path.realpath(exe)
            subprocess.Popen(["xterm", "-hold", "-e", "\"%s\""%(exepath)])
    '''

    # When our window is destroyed, we want to break out of the GTK main loop.
    # We do this by calling gtk_main_quit(). We could have also just specified
    # gtk_main_quit as the handler in Glade!
    def on_window_destroy(self, widget, data=None):
        gtk.main_quit()

    # When the window is requested to be closed, we need to check if they have
    # unsaved work. We use this callback to prompt the user to save their work
    # before they exit the application. From the "delete-event" signal, we can
    # choose to effectively cancel the close based on the value we return.
    def on_window_delete_event(self, widget, event, data=None):
        if self.check_for_save():
            self.on_save_menu_item_activate(None, None)
            # if user cancelled save
            if self.filename == None: return True

        self.log('exiting')
        return False # Propogate event

    # Called when the user clicks the 'New' menu. We need to prompt for save if
    # the file has been modified, and then delete the buffer and clear the
    # modified flag.
    def on_new_menu_item_activate(self, menuitem, data=None):
        if self.check_for_save(): self.on_save_menu_item_activate(None, None)

        # clear editor for a new file
        buff = self.text_view.get_buffer()
        buff.set_text("")
        buff.set_modified(False)
        self.filename = None
	self.language = None
	self.text_encoding = None
        self.reset_default_status()

    def on_new_window_menu_item_activate(self, menuitem, data=None):
        self.spawn()

    # Called when the user clicks the 'Open' menu. We need to prompt for save if
    # thefile has been modified, allow the user to choose a file to open, and
    # then call load_file() on that file.
    def on_open_menu_item_activate(self, menuitem, data=None):
        if self.check_for_save(): self.on_save_menu_item_activate(None, None)

        filename = self.get_open_filename()
        if filename: self.load_file(filename)

    def on_open_in_new_window_menu_item_activate(self, menuitem, data=None):
        filename = self.get_open_filename()
        if filename: self.spawn(filename)


    # Called when the user clicks the 'Save' menu. We need to allow the user to choose
    # a file to save if it's an untitled document, and then call write_file() on that
    # file.
    def on_save_menu_item_activate(self, menuitem, data=None):
        if self.filename == None:
            filename = self.get_save_filename()
            if filename: self.write_file(filename)
        else: self.write_file(None)

    # Called when the user clicks the 'Save As' menu. We need to allow the user
    # to choose a file to save and then call write_file() on that file.
    def on_save_as_menu_item_activate(self, menuitem, data=None):
        filename = self.get_save_filename()
        if filename: self.write_file(filename)

    def on_close_menu_item_activate(self, menuitem, data=None):
        if self.check_for_save():
            self.on_save_menu_item_activate(None, None)
            # if user cancelled save
            if self.filename == None: return
        self.text_view.set_sensitive(False)
        buff = self.text_view.get_buffer()
        buff.set_text("")
        buff.set_modified(False)
        self.text_view.set_sensitive(True)
        self.filename = None
        self.language = None
        self.reset_default_status()

    # Offer to save any changes, then reload original file from disk
    def on_reload_menu_item_activate(self, menuitem, data=None):
        old_filename = self.filename
        if self.check_for_save():
            self.on_save_as_menu_item_activate(menuitem, None)
            # if user cancelled save
            if self.filename == None: return

        self.log('reloading %s'%(old_filename))
        self.load_file(old_filename)

    # Called when the user clicks the 'Quit' menu. We need to prompt for save if
    # the file has been modified and then break out of the GTK+ main loop
    def on_quit_menu_item_activate(self, menuitem, data=None):
        if self.check_for_save():
            self.on_save_menu_item_activate(None, None)
            # if user cancelled save
            if self.filename == None: return

        self.log('exiting')
        gtk.main_quit()

    def on_undo_menu_item_activate(self, menuitem, data=None):
        if using_source_view:
            if self.text_view.get_buffer().can_undo():
                self.text_view.get_buffer().undo()

    def on_redo_menu_item_activate(self, menuitem, data=None):
        if using_source_view:
            if self.text_view.get_buffer().can_redo():
                self.text_view.get_buffer().redo()
    # Called when the user clicks the 'Cut' menu.
    def on_cut_menu_item_activate(self, menuitem, data=None):
        buff = self.text_view.get_buffer();
        buff.cut_clipboard (gtk.clipboard_get(), True);

    # Called when the user clicks the 'Copy' menu.
    def on_copy_menu_item_activate(self, menuitem, data=None):
        buff = self.text_view.get_buffer();
        buff.copy_clipboard (gtk.clipboard_get());

    # Called when the user clicks the 'Paste' menu.
    def on_paste_menu_item_activate(self, menuitem, data=None):
        buff = self.text_view.get_buffer();
        buff.paste_clipboard (gtk.clipboard_get(), None, True);

    def on_select_all_menu_item_activate(self, menuitem, data=None):
        buff = self.text_view.get_buffer();
        buff.select_range(buff.get_start_iter(),buff.get_end_iter())

    # Called when the user clicks the 'Delete' menu.
    def on_delete_menu_item_activate(self, menuitem, data=None):
        buff = self.text_view.get_buffer();


        gone = buff.get_text(buff.get_selection_bounds()[0],buff.get_selection_bounds()[1])
        self.log('deleting %s'%(gone))

        buff.delete_selection (False, True);

    def on_find_prev_selected_menu_item_activate(self,menuitem,data=None):

        buff = self.text_view.get_buffer()
        selected = buff.get_text(buff.get_selection_bounds()[0],buff.get_selection_bounds()[1])

        iter = self.get_find_iter(buffer=buff, backwards=True,limit_iter=None)

        results = self.do_find_with_iter(iter=iter, search_for=selected,backwards=True,case_sensitive=False,whole_word=False)

        try:
            buff.select_range(results[0],results[1])
            self.text_view.scroll_to_mark(mark=buff.get_insert(),within_margin=0.33,use_align=True,xalign=0.5,yalign=0.5)
        except:
            self.log("\'%s\' not found."%(selected))

    def on_find_next_selected_menu_item_activate(self,menuitem,data=None):
        buff = self.text_view.get_buffer()
        selected = buff.get_text(buff.get_selection_bounds()[0],buff.get_selection_bounds()[1])

        iter = self.get_find_iter(buffer=buff, backwards=False,limit_iter=None)

        results = self.do_find_with_iter(iter=iter, search_for=selected,backwards=False,case_sensitive=True,whole_word=False)

        try:
            buff.select_range(results[0],results[1])
            self.text_view.scroll_to_mark(mark=buff.get_insert(),within_margin=0.33,use_align=True,xalign=0.5,yalign=0.5)
        except:
            self.log("\'%s\' not found."%(selected))

    def on_search_case_sensitive_checkbox_toggled(self, data=None):
        #self.search_case_sensitive = togglebutton.get_active()
        self.search_case_sensitive = not self.search_case_sensitive


    def on_search_whole_word_checkbox_toggled(self, data=None):
        #self.search_is_whole_word = togglebutton.get_active()
        self.search_is_whole_word = not self.search_is_whole_word

    def search_find_field_changed(self, data=None):
        self.search_string = self.search_field.get_text()
    def search_replace_field_changed(self, data=None):
        self.replacement_string = self.replace_field.get_text()

    def on_show_find_menu_item_activate(self,menuitem,data=None):
        #TODO: could load search UI from xml string here

        if self.search_window.get_property("visible"):
            self.search_window.present()
            return

        buff = self.text_view.get_buffer()
        if self.search_string == "":
            if buff.get_selection_bounds():
                self.search_string = buff.get_slice(buff.get_selection_bounds()[0],buff.get_selection_bounds()[1])

        self.search_field.set_text(self.search_string)
        self.replace_field.set_text(self.replacement_string)
        self.search_field.grab_focus()

        self.search_window.show_all()

    def on_search_window_delete_event(self, widget=None, event=None, data=None):
        self.search_window.hide_all()
        return True

    def on_find_next_menu_item_activate(self, sender, data=None):
        buff = self.text_view.get_buffer();
        if self.search_string == "":
            if buff.get_selection_bounds():
                self.search_string = buff.get_slice(buff.get_selection_bounds()[0],buff.get_selection_bounds()[1])
                self.search_field.set_text(self.search_string)
            else:
                self.error_message("Enter the search string first.")
                self.on_show_find_menu_item_activate(sender)

        next_results = self.do_find(buffer=buff,iter=None,backwards=False,case_sensitive=self.search_case_sensitive,whole_word=self.search_is_whole_word)

        #highlight next results
        #offer to wrap

    #find backwards
    def on_find_previous_menu_item_activate(self, menuitem, data=None):
        buff = self.text_view.get_buffer();
        if self.search_string == "":
            if buff.get_selection_bounds():
                self.search_string = buff.get_slice(buff.get_selection_bounds()[0],buff.get_selection_bounds()[1])
                self.search_field.set_text(self.search_string)
            else:
                self.error_message("Enter the search string first.")
                self.on_show_find_menu_item_activate(menuitem)

        prev_results = self.do_find(buffer=buff,iter=None,backwards=True,case_sensitive=self.search_case_sensitive,whole_word=self.search_is_whole_word)

        #highlight prev results
        #offer to wrap

    def on_find_all_menu_item_activate(self, menuitem, data=None):
        buff = self.text_view.get_buffer();
        if self.search_string == "":
            if buff.get_selection_bounds():
                self.search_string = buff.get_slice(buff.get_selection_bounds()[0],buff.get_selection_bounds()[1])
                self.search_field.set_text(self.search_string)
            else:
                self.error_message("Enter the search string first.")
                self.on_show_find_menu_item_activate(menuitem)
                return
        self.do_find_all(buffer=buff)

    def on_replace_and_find_menu_item_activate(self, menuitem, data=None):
        if self.search_string == "":
            self.error_message("Enter the search string first.")
            return
        if self.replacement_string == '':
            self.error_message("Enter the replacement string first.")
            self.on_show_find_menu_item_activate(menuitem)
            return

        buff = self.text_view.get_buffer()

        replace_iter = self.get_find_iter(buffer=buff, backwards=buff.get_has_selection(),limit_iter=None) #LAST

        next_results = self.do_find(buffer=buff,iter=replace_iter,backwards=False,case_sensitive=self.search_case_sensitive,whole_word=self.search_is_whole_word)

        if next_results == None:
            return
        else:
            result_iter = next_results[0]
            #ask for confirm here
            self.do_replace_next(buffer=buff,iter=result_iter,search_for=self.search_string,replace_with=self.replacement_string,limit=next_results[1])

    def on_replace_all_menu_item_activate(self, menuitem, data=None):
        if self.search_string == "":
            self.error_message("Enter the search string first.")
            return
        if self.replacement_string == "":
            self.error_message("Enter the replacement string first.")
            return

        buff = self.text_view.get_buffer()
        self.do_replace_all(buff,self.search_string,self.replacement_string)


    # Called when the user clicks an item from the 'Wrap' menu.
    def on_wrap_none_menu_item_activate(self, menuitem, data=None):
        self.wrapping = 'None'
        self.text_view.set_wrap_mode(gtk.WRAP_NONE);

    def on_wrap_char_menu_item_activate(self, menuitem, data=None):
        self.wrapping = 'Character'
        self.text_view.set_wrap_mode(gtk.WRAP_CHAR);

    def on_wrap_word_menu_item_activate(self, menuitem, data=None):
        self.wrapping = 'Word'
        self.text_view.set_wrap_mode(gtk.WRAP_WORD);

    def on_select_font_menu_item_activate(self,menuitem, data=None):
        if not self.font_dialog:
            window = gtk.FontSelectionDialog("Font Selection Dialog")
            self.font_dialog = window

            window.set_position(gtk.WIN_POS_MOUSE)
            window.set_transient_for(self.window)
            window.connect("destroy", self.font_dialog_destroyed)

            window.ok_button.connect("clicked", self.font_selection_ok)
            window.cancel_button.connect_object("clicked", lambda wid: wid.destroy(), self.font_dialog)
            current_font = self.text_view.get_pango_context().get_font_description().to_string()
            window.set_font_name(current_font)

        window = self.font_dialog
        if not (window.flags() & gtk.VISIBLE):
            window.show()
        else:
            window.destroy()
            self.font_dialog = None

    def font_selection_ok(self, button):
        self.font = self.font_dialog.get_font_name()
        if self.window:
            font_desc = pango.FontDescription(self.font)
            if font_desc:
                self.text_view.modify_font(font_desc)
                self.font_dialog.destroy()
    def font_dialog_destroyed(self, data=None):
        self.font_dialog = None

    #emitted when the modified flag of the buffer changes
    def on_text_buffer_modified_changed(self, buff, data=None):
        self.mark_window_status(self.window,buff.get_modified())

    #emitted BEFORE the text is actually inserted into the buffer
    def on_text_buffer_insert_text(self, buff, iter, text, length, data=None):
        # for change highlighting. just save the edit location and length here.
        # the actual highlight is applied in on_text_buffer_changed()
        self.edit_loc = iter.get_offset()
        self.edit_len = length


        # remove any find highlighting we've done
        if buff.get_tag_table().lookup("search_results"):
            buff.remove_tag_by_name('search_results', buff.get_start_iter(), buff.get_end_iter())


    #emitted AFTER text is inserted into the buffer
    #here we retrieve the location and apply the highlight tag
    def on_text_buffer_changed(self, buff,data=None):

        # we set edit_loc to -1 on deletions
        if self.edit_loc >=0:
            start_iter = buff.get_iter_at_offset(self.edit_loc)
            start_mark = buff.create_mark(None,start_iter)
            end_iter = buff.get_iter_at_offset(self.edit_loc + self.edit_len)
            end_mark = buff.create_mark(None,end_iter)
            self.mark_range_as_changed(buff,start_mark,end_mark)
            buff.delete_mark(start_mark)
            buff.delete_mark(end_mark)

    #set the edit location to -1 here so on_text_buffer_changed() doesn't
    #try to set attributes on a deleted range
    def on_text_buffer_delete_range(self,buff,start,end, data=None):
        self.edit_loc = -1


    #def on_text_buffer_mark_set(self, textbuffer, iter, textmark, data=None):
    #    if textmark.get_name() == 'insert':
    #        self.move_replace_cursor(textbuffer,iter)

    # We call error_message() any time we want to display an error message to
    # the user. It will both show an error dialog and log the error to the
    # terminal window.
    def error_message(self, message):
        # log to terminal window
        self.log(message)

        # create an error message dialog and display modally to the user
        dialog = gtk.MessageDialog(None,
                                   gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                                   gtk.MESSAGE_ERROR, gtk.BUTTONS_OK, message)

        dialog.run()
        dialog.destroy()

    # This function will check to see if the text buffer has been
    # modified and prompt the user to save if it has been modified.
    def check_for_save (self):
        ret = False
        buff = self.text_view.get_buffer()

        if buff.get_modified():

            # we need to prompt for save
            message = "Do you want to save the changes you have made?"
            dialog = gtk.MessageDialog(self.window,
                                       gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                                       gtk.MESSAGE_QUESTION, gtk.BUTTONS_YES_NO,
                                       message)
            dialog.set_title("Save?")

            if dialog.run() == gtk.RESPONSE_NO: ret = False
            else: ret = True

            dialog.destroy()

        return ret

    # We call get_open_filename() when we want to get a filename to open from the
    # user. It will present the user with a file chooser dialog and return the
    # filename or None.
    def get_open_filename(self):
        filename = None
        chooser = gtk.FileChooserDialog("Open File...", self.window,
                                        gtk.FILE_CHOOSER_ACTION_OPEN,
                                        (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                         gtk.STOCK_OPEN, gtk.RESPONSE_OK))

        response = chooser.run()
        if response == gtk.RESPONSE_OK: filename = chooser.get_filename()
        chooser.destroy()

        return filename

    # We call get_save_filename() when we want to get a filename to save from the
    # user. It will present the user with a file chooser dialog and return the
    # filename or None.
    def get_save_filename(self):
        filename = None
        chooser = gtk.FileChooserDialog("Save File...", self.window,
                                        gtk.FILE_CHOOSER_ACTION_SAVE,
                                        (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                         gtk.STOCK_SAVE, gtk.RESPONSE_OK))

        response = chooser.run()
        if response == gtk.RESPONSE_OK: filename = chooser.get_filename()
        #if response == gtk.RESPONSE_CANCEL: print "save cancelled"
        chooser.destroy()

        return filename



###
# do_* = controller methods called from on_* actions
###

    # find

    def get_find_iter(self,buffer=None, backwards=False,limit_iter=None):
        find_iter = None
        selection = buffer.get_selection_bounds()
        if selection == ():
            find_iter = buffer.get_iter_at_mark(buffer.get_insert())
            if find_iter == None:
                find_iter = buffer.get_bounds()[int(backwards)]
        else:
            find_iter = selection[int(not backwards)]

        return find_iter


    def do_find(self,buffer=None,iter=None,backwards=False,case_sensitive=False,whole_word=False):

        if self.search_string == "":
            # show the ui
            self.on_show_find_menu_item_activate(buffer)
            return

        find_iter = iter

        if find_iter == None:
            find_iter = self.get_find_iter(buffer=buffer, backwards=backwards,limit_iter=None)

        results = self.do_find_with_iter(find_iter, self.search_string, backwards=backwards, case_sensitive=case_sensitive,whole_word=whole_word)

        if results == None:
            #nothing else found. ask to wrap.
            self.log( "\'%s\' not found"%(self.search_string))
            if self.ask_for_wrap(backwards=backwards):
                self.log("wrapping")
                wrapped_iter = buffer.get_bounds()[int(backwards)]
                results = self.do_find_with_iter(wrapped_iter, self.search_string, backwards=backwards, case_sensitive=case_sensitive,whole_word=whole_word)
                if results:
                    ins, bound = results
                    buffer.select_range(ins,bound)
                    self.text_view.scroll_to_mark(mark=buffer.get_insert(),within_margin=0.33,use_align=True,xalign=0.5,yalign=0.5)
                else:
                    # really not found. beep.
                    gtk.gdk.beep()
        else:
            #happily select and highlight
            ins, bound = results
            buffer.select_range(ins,bound)
            self.text_view.scroll_to_mark(mark=buffer.get_insert(),within_margin=0.33,use_align=True,xalign=0.5,yalign=0.5)

        return results

    def do_find_with_iter(self, iter=None, search_for=None,backwards=False,case_sensitive=False,whole_word=False):

        def next_match():
            results = None
            search_flags = 0
            if using_source_view:
                if not self.search_case_sensitive:
                    search_flags = gtksourceview2.SEARCH_CASE_INSENSITIVE
                if backwards:
                    results = gtksourceview2.iter_backward_search(iter, search_for, flags=search_flags)#, limit=limit_iter)
                else:
                    results = gtksourceview2.iter_forward_search(iter, search_for, flags=search_flags)#, limit=limit_iter)
            else:
                if backwards:
                    results = iter.backward_search(search_for, flags=search_flags)#, limit=limit_iter)
                else:
                    results = iter.forward_search(search_for, flags=search_flags)#, limit=limit_iter)
            return results

        #test for whole word , case
        def next_whole_word():
            word_hit = None
            whole_word_hit = False
            while not whole_word_hit:
                word_hit = next_match()
                if word_hit:
                    if word_hit[0].starts_word() and word_hit[1].ends_word():
                        #hit = result
                        whole_word_hit = True
                        return word_hit
                    else:
                        if not backwards:
                            iter.forward_chars(len(search_for))
                        else:
                            iter.backward_chars(len(search_for))
                        #print iter.get_offset()
                        word_hit = next_match()
                else:
                    return None

            return word_hit

        result = next_match()

        # test substring result for conditions
        if self.search_is_whole_word:
            hit = next_whole_word()
        else:
            hit = result

        return hit

    def ask_for_wrap(self,backwards=False):
        ret = False

        direction = 'beginning'
        if backwards:
            direction = 'end'

        message = "\'%s\' not found. Wrap and start from %s of document?"%(self.search_string,direction)
        dialog = gtk.MessageDialog(self.window,
                                   gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                                   gtk.MESSAGE_QUESTION, gtk.BUTTONS_YES_NO,
                                   message)

        dialog.set_title("Wrap Search?")

        if dialog.run() == gtk.RESPONSE_NO: ret = False
        else: ret = True

        dialog.destroy()

        return ret

    def ask_for_replace(self):
        ret = False

        message = "Replace?"
        dialog = gtk.MessageDialog(self.window,
                                       gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                                       gtk.MESSAGE_QUESTION, gtk.BUTTONS_YES_NO,
                                       message)
        dialog.set_title("Replace?")

        if dialog.run() == gtk.RESPONSE_NO: ret = False
        else: ret = True

        dialog.destroy()

        return ret

    def do_find_all(self,buffer=None,case_sensitive=False,whole_word=False):
        start_iter = buffer.get_start_iter()
        end_iter = buffer.get_end_iter()

        begin_mark = buffer.create_mark(None,start_iter)
        end_mark = buffer.create_mark(None,end_iter)
        search_results = self.find_all_in_range(buffer, self.search_string, begin_mark,end_mark)
        buffer.delete_mark(begin_mark)
        buffer.delete_mark(end_mark)

        if not buffer.get_tag_table().lookup("search_results"):
            preview_tag = buffer.create_tag("search_results", background_set="True",background=CONF_FIND_HIGHLIGHT)
        else:
            buffer.remove_tag_by_name('search_results', start_iter, end_iter)

        if search_results:
            for range in search_results:
                if self.search_is_whole_word:
                    if range[0].starts_word() and range[1].ends_word():
                        buffer.apply_tag_by_name("search_results",range[0],range[1])
                else:
                    buffer.apply_tag_by_name("search_results",range[0],range[1])


    def do_replace_next(self,buffer=None,iter=None,search_for='',replace_with='',limit=None):

        buffer.remove_tag_by_name('search_results', buffer.get_start_iter(), buffer.get_end_iter())

        replace_iter = iter

        range = self.do_find(buffer=buffer,iter=replace_iter,backwards=False,case_sensitive=self.search_case_sensitive,whole_word=self.search_is_whole_word)

        if range:
            if not buffer.get_tag_table().lookup("search_results"):
                preview_tag = buffer.create_tag("search_results", background_set="True",background=CONF_FIND_HIGHLIGHT)

            #apply tag
            buffer.apply_tag_by_name("search_results",range[0],range[1])

            if not self.ask_for_replace():
                self.log("replace declined")
                return

            replace_begin = buffer.create_mark(None,range[0])
            replace_end = buffer.create_mark(None,range[1])
            replace_list = [(replace_begin,replace_end)]


            replaced_range = self.replace_text(buffer,replace_with,replace_list)

            self.text_view.scroll_to_mark(replace_end,0)
            buffer.delete_mark(replace_begin)
            buffer.delete_mark(replace_end)


    def do_replace_all(self,buffer,search_for,replace_with):
        #search_results = self.search_for_text(buffer,search_for,buffer.get_start_iter(),buffer.get_end_iter())
        replace_begin = buffer.create_mark(None,buffer.get_start_iter())
        replace_end = buffer.create_mark(None,buffer.get_end_iter())
        search_results = self.find_all_in_range(buffer,search_for,replace_begin,replace_end)

        result_marks = []
        for iter_pair in search_results:
            this_mark_pair = []
            for iter in iter_pair:
                this_mark = buffer.create_mark(None,iter)
                this_mark_pair.append(this_mark)
            self.edit_loc = iter_pair[0]#wft

            result_marks.append(this_mark_pair)

        self.replace_text(buffer,replace_with,result_marks)

        for that_mark_pair in result_marks:
            for that_mark in that_mark_pair:
                buffer.delete_mark(that_mark)

        buffer.delete_mark(replace_begin)
        buffer.delete_mark(replace_end)


    def find_all_in_range(self, buff, search_string, start_mark, end_mark):
        start_iter = buff.get_iter_at_mark(start_mark)
        end_iter = buff.get_iter_at_mark(end_mark)
        search_results = []

        next_result = self.do_find_with_iter(iter=start_iter,search_for=self.search_string,backwards=False,case_sensitive=self.search_case_sensitive,whole_word=self.search_is_whole_word)
        while next_result:
            #self.search_for_text(buff,search_string,start_iter,end_iter)
            search_results.append(next_result)
            next_result = self.do_find_with_iter(iter=next_result[1],search_for=self.search_string,backwards=False,case_sensitive=self.search_case_sensitive,whole_word=self.search_is_whole_word)

        return search_results

    def guess_encoding(self,data):
        """
        Given a byte string, attempt to decode it.
        Tries the standard 'UTF8' and 'latin-1' encodings,
        Plus several gathered from locale information.

        The calling program *must* first call
            locale.setlocale(locale.LC_ALL, '')

        If successful it returns
            (decoded_unicode, successful_encoding)
        If unsuccessful it raises a ``UnicodeError``
        """
        import locale

        successful_encoding = None
        # we make 'utf-8' the first encoding
        encodings = ['utf-8']
        #
        # next we add anything we can learn from the locale
        try:
            encodings.append(locale.nl_langinfo(locale.CODESET))
        except AttributeError:
            pass
        try:
            encodings.append(locale.getlocale()[1])
        except (AttributeError, IndexError):
            pass
        try:
            encodings.append(locale.getdefaultlocale()[1])
        except (AttributeError, IndexError):
            pass
        #
        # we try 'latin-1' last
        encodings.append('latin-1')
        for enc in encodings:
            # some of the locale calls
            # may have returned None
            if not enc:
                continue
            try:
                decoded = unicode(data, enc)
                successful_encoding = enc

            except (UnicodeError, LookupError):
                pass
            else:
                break
        if not successful_encoding:
             raise UnicodeError(
            'Unable to decode input data.  Tried the following encodings: %s.'
            % ', '.join([repr(enc) for enc in encodings if enc]))
        else:
             return (decoded, successful_encoding)


    #thanks to http://www.pyzine.com/Issue008/Section_Articles/article_Encodings.html
    def decode_text(self,the_text=None):
        # adapted from io.py
        # in the docutils extension module
        # see http://docutils.sourceforge.net
        import codecs
        import locale
        import sys

        # uses the guess_encoding function from above

        bomdict = {
                         codecs.BOM_UTF8 : 'UTF8',
                 codecs.BOM_UTF16_BE : 'UTF-16BE',
                 codecs.BOM_UTF16_LE : 'UTF-16LE' }

        # check if there is Unicode signature
        for bom, encoding in bomdict.items():
            if the_text.startswith(bom):
                the_text = the_text[len(bom):]
                break
            else:
               bom  = None
               encoding = None

        if encoding is None:    # there was no BOM
            try:
                unicode_text, encoding = self.guess_encoding(the_text)
            except UnicodeError:
                print "Sorry - we can't work out the encoding."
                raise
        else:
            # we found a BOM so we know the encoding
            unicode_text = the_text.decode(encoding)
        # now you have your Unicode text.. and can do with it what you will

        # now we want to re-encode it to a byte string
        # so that we can write it back out
        # we will reuse the original encoding, and preserve any BOM
        if bom is not None:
            if encoding.startswith('UTF-16'):
            # we will use the right 'endian-ness' for this machine
                encoding = 'UTF-16'
                bom = codecs.BOM_UTF16
        byte_string = unicode_text.encode(encoding)
        if bom is not None:
            byte_string = bom + byte_string
        # now we have the text encoded as a byte string, ready to be saved to a file

        return byte_string


    # We call load_file() when we have a filename and want to load it into the
    # buffer for the GtkTextView. The previous contents are overwritten.
    def load_file(self, filename):
        # add Loading message to status bar and ensure GUI is current
		self.statusbar.push(self.statusbar_cid, "Loading %s" % filename)
		while gtk.events_pending():
			gtk.main_iteration()

		buff = self.text_view.get_buffer()
		if using_source_view:
			try:
				buff.begin_not_undoable_action()
			except AttributeError:
				pass

		try:
			# get the file contents
			fin = open(filename, "r")
			text_data = fin.read()
			fin.close()

			# disable the text view while loading the buffer with the text
			self.text_view.set_sensitive(False)


			#unicode?
			#buff.set_text(text)
			the_text,the_encoding = self.guess_encoding(text_data)
			buff.set_text(the_text)
			self.text_encoding = the_encoding
			#print "encoding: %s"%self.text_encoding

			# reenable text view and set everything up for the user
			buff.set_modified(False)
			self.text_view.set_sensitive(True)

			# now we can set the window's filename since loading was a success
			self.filename = filename

		except:
			# error loading file, show message to user
			self.error_message ("Could not open file: %s\n%s" % (filename,sys.exc_info()[0]))
			raise

		# syntax highlighting
		if using_source_view:
			if CONF_HIGHLIGHT_SYNTAX:
				buffer = self.text_view.get_buffer()
				#f = gio.File(filename)
				#path = f.get_path()
				#info = f.query_info("*")
				#mime_type = info.get_content_type()
				language = gtksourceview2.language_manager_get_default().get_language("python")

				try:
					buffer.set_language(language)

					buffer.set_highlight_syntax(CONF_HIGHLIGHT_SYNTAX)
				except AttributeError:
					pass

		# move insertion point and scroll to top
		buff.place_cursor(buff.get_start_iter())

		if using_source_view:
			try:
				self.text_view.get_buffer().end_not_undoable_action()
			except AttributeError:
				pass

		# clear loading status and restore default
		self.statusbar.pop(self.statusbar_cid)
		self.reset_default_status()

    def write_file(self, filename):
        # add Saving message to status bar and ensure GUI is current
        if filename:
            self.statusbar.push(self.statusbar_cid, "Saving %s" % filename)
        else:
            self.statusbar.push(self.statusbar_cid, "Saving %s" % self.filename)

        while gtk.events_pending(): gtk.main_iteration()

        try:
            # disable text view while getting contents of buffer
            buff = self.text_view.get_buffer()
            self.text_view.set_sensitive(False)
            text = buff.get_text(buff.get_start_iter(), buff.get_end_iter())

	    if self.text_encoding == None:
		self.text_encoding = "utf-8"
            #text_data = unicode(text)
            text_data = text.encode(self.text_encoding)

            self.text_view.set_sensitive(True)
            buff.set_modified(False)

            # set the contents of the file to the text from the buffer
            if filename: fout = open(filename, "w")
            else: fout = open(self.filename, "w")
            fout.write(text_data)
            fout.close()

            if filename: self.filename = filename
        except:
            # error writing file, show message to user
            self.error_message ("Could not save file: %s" % filename)

        # clear saving status and restore default
        self.statusbar.pop(self.statusbar_cid)
        self.reset_default_status()

    ######################################################################
    ##### Note this function is silly and wrong, because it ignores mime
    ##### parent types and subtypes.
    # i don't care i'm using it anyway
    def get_language_for_mime_type(self,mime):
        lang_manager = gtksourceview2.language_manager_get_default()
        lang_ids = lang_manager.get_language_ids()
        for i in lang_ids:
            lang = lang_manager.get_language(i)
            for m in lang.get_mime_types():
                if m == mime:
                    return lang
        return None

    def mark_window_status(self,window,changed):
        if changed:
            if not window.get_title()[0] == "*":
                window.set_title("*" + window.get_title())

    class StatusBarManager:
        def __init__(self):
            self.filename = "(UNTITLED)"
            self.language = "(NONE)"
            self.encoding = "utf-8" #get default encoding
            self.status_line = {}
            self.statusbar = None

        def StatusBarManager(self, statusbar=None, language=None,filename=None,encoding=None):
            self.set_language(language)
            self.set_filename(filename)
            self.set_encoding(encoding)
            self.set_statusbar(statusbar)

        def set_language(self,language=None):
            self.language = language
            self.status_line['Language'] = self.language
            self.update_status()


        def set_encoding(self,encoding=None):
            self.encoding = encoding
            self.status_line['Encoding'] = self.encoding
            self.update_status()

        def set_filename(self,filename=None):
            self.filename = filename
            self.status_line['File'] = self.filename
            self.update_status()


        def set_statusbar(self,statusbar=None):
            self.statusbar = statusbar


        def update_status(self):
            cid = self.statusbar.get_context_id("EduCIAA Python Editor")
            self.statusbar.push(cid,self.get_status())


        def reset_status(self):
            self.update_status()

        def set_status(self,string):
            cid = self.statusbar.get_context_id("EduCIAA Python Editor")
            self.statusbar.push(cid,string)

        def get_status(self):
            status_string = "File: %s | Encoding: %s"%(self.filename,self.encoding)

            return status_string

    class PluginInterface:
        def set_parent(self,parent=None):
            self.parent = parent

        def replace_selection(self,new_text=None):
            #create marks
            range = self.get_selected_range()
            buff = self.get_buffer()
            start = buff.create_mark(None,range[0])
            end = buff.create_mark(None,range[1])
            repl = self.parent.replace_text(buff,new_text,[(start,end)])
            buff.select_range(buff.get_iter_at_mark(start),buff.get_iter_at_mark(end))
            buff.delete_mark(start)
            buff.delete_mark(end)

        def insert(self,text=None):
            if text:
                self.parent.text_view.get_buffer().insert_at_cursor(text)

        def select(self,start,end):
            self.get_buffer().select_range(end,start)

        def get_selection(self):
            range = self.parent.text_view.get_buffer().get_selection_bounds()
            return self.parent.text_view.get_buffer().get_text(range[0],range[1])

        def get_selected_range(self):
            return self.parent.text_view.get_buffer().get_selection_bounds()

        def open_file(self,path=None):
            self.parent.spawn(path)
            return

        def get_text(self):
            buf = self.parent.text_view.get_buffer()
            return buf.get_text(buf.get_start_iter(),buf.get_end_iter())

        def message(self,string=None):
            self.parent.error_message(string)

        def get_language(self):
            return self.parent.language

        def get_buffer(self):
            return self.parent.text_view.get_buffer()

        def get_filename(self):
            return self.parent.filename
			
        def get_base_path(self):
            return BASE_PATH
            

    def on_drag_motion(self,wid, context, x, y, time):
        context.drag_status(gtk.gdk.ACTION_COPY, time)
        #path = context.drag_get_selection()
        path = ""
        self.statusbar_manager.set_status('Open: %s'%(path))
        return True

   # def on_drag_drop(self,wid, context, x, y, time):
   #     self.text_view.get_buffer().set_text('\n'.join([str(t) for t in context.targets]))
   #     #load file
   #     wid.drag_get_data()
   #     context.finish(True, False, time)
   #     return True
    def on_drag_end(self,widget, drag_context, data):
        self.statusbar_manager.reset_status()

    def on_drag_data_received(self,widget, drag_context, x, y, selection, target_type, time, data):
        if target_type == 80:
            uri = selection.data.strip('\r\n\x00')
            uri_splitted = uri.split() # we may have more than one file dropped
            #for uri in uri_splitted:
            #print uri_splitted
            uri = uri_splitted[0]
            path = self.get_file_path_from_dnd_dropped_uri(uri)
            #path = urlparse.urlparse(uri).path
            #print path
            if os.path.isfile(path):
                if self.check_for_save():
                    self.on_save_menu_item_activate(None, None)
                    # if user cancelled save
                    if self.filename == None: return
                self.load_file(path)

                drag_context.finish(success=True, del_=False, time=time)
                #drag_context.drop_finish(True,time)
            else:
                #drag_context.drop_finish(False,time)
                drag_context.finish(success=False, del_=False, time=time)


    def get_file_path_from_dnd_dropped_uri(self,uri):
        # get the path to file
        path = ""
        if uri.startswith('file:\\\\\\'): # windows
            path = uri[8:] # 8 is len('file:///')
        elif uri.startswith('file://'): # nautilus, rox
            path = uri[7:] # 7 is len('file://')
        elif uri.startswith('file:'): # xffm
            path = uri[5:] # 5 is len('file:')

        path = urllib.url2pathname(path) # escape special chars
        path = path.strip('\r\n\x00') # remove \r\n and NULL

        return path

    def running_as_root(self):
        return (os.name == 'posix') and (os.geteuid() == 0)

    def reset_default_status(self):
        if self.filename:
            status = "File: %s" % self.filename #os.path.basename(self.filename)
            self.window.set_title("%s | EDU-CIAA Python Editor" % os.path.basename(self.filename))
        else:
            status = "File: (UNTITLED)"
            self.window.set_title("Untitled | EDU-CIAA Python Editor")

        #check for root
        #if platform.system() is not "Windows":
        if self.running_as_root():
            old_title = self.window.get_title()
            new_title = old_title + " | RUNNING AS ROOT"
            self.window.set_title(new_title)

        self.statusbar.pop(self.statusbar_cid)
        self.statusbar.push(self.statusbar_cid, status)

        self.statusbar_manager.set_filename(self.filename)
        self.statusbar_manager.set_language(self.language)
        self.statusbar_manager.set_encoding(self.text_encoding)

        buff = self.text_view.get_buffer()
        buff.remove_tag_by_name("change_highlight",buff.get_start_iter(),buff.get_end_iter())

        #self.move_replace_cursor(buff,buff.get_start_iter())

        self.text_view.grab_focus()

    def search_for_text(self, txtbuf, text, begin, end):
        """
        Search for text within a specified text buffer.

        This function searches for the text within the boundaries specified by begin
        and end in a specified text buffer. If matches are found the function
        returns the position of the found matches represented by pairs of
        gtk.TextMarks. Otherwise, the functions returns an empty List.

        @param txtbuf: Reference to the text buffer to search.
        @type editor: A gtk.TextBuffer object.

        @param text: The string to search for in the text editor's buffer.
        @type text: A String object.

        @param begin: The position in the buffer to begin searching for text.
        @type begin: A gtk.TextIter object.

        @param end: The position in the buffer to stop searching for text.
        @type end: A gtk.TextIter object.

        @return: The position of found matches in the buffer.
        @rtype: A List object containing pairs of gtk.TextIter or None.
        """
        found_matches = []
        from gtk import TEXT_SEARCH_VISIBLE_ONLY
        while True:
            result = begin.forward_search(text, TEXT_SEARCH_VISIBLE_ONLY, end)
            if result:
                found_matches.append((result[0], result[1]))
                begin = result[1]
            else:
                break
        return found_matches

    def mark_range_as_changed(self,txtbuf,start_mark,end_mark):

        if self.highlight_changes:
            begin = txtbuf.get_iter_at_mark(start_mark)
            end = txtbuf.get_iter_at_mark(end_mark)
            txtbuf.apply_tag_by_name("change_highlight",begin,end)

    def replace_text(self, txtbuf, text, positions):
        """
        Replace text at specified positions in a text buffer with one specified as
        a parameter.

        @param txtbuf: Reference to a text buffer where replacement should occur.
        @type txtbuf: A gtk.TextBuffer object.

        @param text: Text to insert into the text buffer.
        @type text: A String object.

        @param positions: Positions in the text buffer to replace text.
        @type positions: A List object containing pairs of gtk.TextMarks.
        """

        replaced_ranges = []
        for marks in positions:
            begin = txtbuf.get_iter_at_mark(marks[0])
            end = txtbuf.get_iter_at_mark(marks[1])
            txtbuf.delete(begin, end)
            begin = txtbuf.get_iter_at_mark(marks[0])
            txtbuf.insert(begin, text)
            replaced_ranges.append((marks[0],marks[1]))

        return replaced_ranges

    #spawn a new edile instance
    def spawn(self, file=None):
        exe = __file__
        exepath = os.path.realpath(exe)
        if file:
            path = os.path.realpath( file )
        else:
            path = ""

        #doesnt use subprocess
        #os.system("%s \"%s\"&"% (exepath,path))
        child_pid = subprocess.Popen([exepath, path]).pid

        self.log("new %s instance pid %d"%(os.path.basename(exepath),child_pid))

    def plugin_load_from_url(self,url):
        f = open(url)
        plugin_string = f.read()
        f.close()
        #plugin_string = urllib.urlopen(url).read()

        #plugin_file = tempfile.NamedTemporaryFile()
        #plugin_file.write(plugin_string)
        #print plugin_file.name

        return plugin_string

    def plugin_getfunctions(self,module):
        l = []
        for key, value in module.__dict__.items():            
            if type(value) is types.FunctionType and key[0:5]=="item_":
                l.append(value)
        return l

    '''
    def plugin_get_plugins(self):
            plugin_tree = {}

            if CONF_PLUGIN_LOCATION == "": return

            plugin_string = self.plugin_load_from_url(CONF_PLUGIN_LOCATION)

            if plugin_string:
                plugin_hash = hashlib.sha256(plugin_string).hexdigest()

                if (plugin_hash == CONF_PLUGIN_SHA256) or (CONF_PLUGIN_SHA256 == ''):
                    plugins = imp.new_module("plugins")
                    exec(plugin_string, plugins.__dict__)
                    #print plugins.__dict__['Tools'].shortcuts
                else:
                    self.error_message("plugin authentication failed")
                    quit()


            #pl = imp.load_source("plugins",plugin_file) #path only
            
            for thing in plugins.__dict__:
                
                #if thing[:2] != "__":
                #if type(thing) is types.MethodType:
                if thing[0:4] == "mnu_":				
                    pl_key = (thing,plugins.__dict__[thing])
                    plugin_tree[pl_key] = self.plugin_getfunctions(plugins.__dict__[thing])

            #print plugin_tree
            return plugin_tree
    '''

    def plugin_create_menus(self):
		menus = []
		self.plugin_menu_items = []
		plugin = ciaa_plugin.mnu_EDUCIAA()
		the_menubar_item = gtk.MenuItem("EDU-CIAA",False)
		the_menu = gtk.Menu()

		menu_item = gtk.MenuItem("Load Script",False)
		menu_item.connect('activate',plugin.item_Load_Script,self.plugin_interface)
		the_menu.append(menu_item)
		self.plugin_menu_items.append(menu_item)
		
		menu_item = gtk.MenuItem("Terminal",False)
		menu_item.connect('activate',plugin.item_Console,self.plugin_interface)
		the_menu.append(menu_item)
		self.plugin_menu_items.append(menu_item)
		
		menu_item = gtk.MenuItem("Snippets",False)
		menu_item.connect('activate',plugin.item_Snippets,self.plugin_interface)
		the_menu.append(menu_item)
		self.plugin_menu_items.append(menu_item)

		menu_item = gtk.MenuItem("Configuration",False)
		menu_item.connect('activate',plugin.item_Configuration,self.plugin_interface)
		the_menu.append(menu_item)
		self.plugin_menu_items.append(menu_item)
		
		menu_item = gtk.MenuItem("Emulator",False)
		menu_item.connect('activate',plugin.item_Emulator,self.plugin_interface)
		the_menu.append(menu_item)
		self.plugin_menu_items.append(menu_item)
		
		menu_item = gtk.MenuItem("Tips",False)
		menu_item.connect('activate',plugin.item_Tips,self.plugin_interface)
		the_menu.append(menu_item)
		self.plugin_menu_items.append(menu_item)		
		
		agr = gtk.AccelGroup()
		self.window.add_accel_group(agr)
		
		the_menubar_item.set_submenu(the_menu)
		menus.append(the_menubar_item)
		return menus

	
    def plugin_add_menus(self,menubar=None,plugin_menus=None):
        #insert plugin menus into the menu bar before the Help menu
        [menubar.insert(every_menu,4) for every_menu in plugin_menus]

    # output in a friendly fashion
    def log(self,string):
        instance_name = self.window.get_title()
        pid = '[%d]'%(os.getpid())

        print "%s %s %s"%(instance_name,pid,string)

    
    def load_plugins(self):
        should_load = CONF_LOAD_PLUGINS

        if should_load:
            if CONF_LOAD_PLUGINS_AS_ROOT == False:
                should_load = not self.running_as_root()

        if should_load:
            #pluginlist = self.plugin_get_plugins()
            self.plugin_menus = self.plugin_create_menus()

            self.plugin_add_menus(self.menubar,self.plugin_menus)
            self.window.show_all()
    
    # setter methods for options
    def set_auto_indent(self, indent=CONF_AUTO_INDENT):
        self.text_view.set_auto_indent(CONF_AUTO_INDENT)

    def set_highlight_changes(self, highlight=CONF_HIGHLIGHT_CHANGES_SINCE_SAVE):
        self.highlight_changes = highlight

    def set_highlight_current_line(self, highlight=CONF_HIGHLIGHT_CURRENT_LINE):
        self.text_view.set_highlight_current_line(highlight)

    def set_show_line_numbers(self, number=CONF_SHOW_LINE_NUMBERS):
        self.text_view.set_show_line_numbers(number)

    def set_show_right_margin(self, margin=CONF_SHOW_RIGHT_MARGIN):
        self.text_view.set_show_right_margin(margin)

    def set_insert_spaces_instead_of_tabs(self, insert=CONF_SPACES_INSTEAD_OF_TABS):
        self.text_view.set_insert_spaces_instead_of_tabs(insert)

    def set_tab_width(self, width=CONF_TAB_WIDTH):
        self.text_view.set_tab_width(width)

    def set_indent_width(self, width=CONF_INDENT_WIDTH):
        self.text_view.set_indent_width(width)

    def set_smart_home_end(self, type=CONF_SMART_HOME_END_TYPE_MAP[CONF_SMART_HOME_END_TYPE[0]]):
        self.text_view.set_smart_home_end(type)

    def set_indent_on_tab(self, indent=CONF_INDENT_ON_TAB):
        self.text_view.set_indent_on_tab(indent)

    def set_right_margin_position(self, pos=CONF_RIGHT_MARGIN_POSITION):
        self.text_view.set_right_margin_position(pos)

    def set_highlight_syntax(self, highlight=CONF_HIGHLIGHT_SYNTAX):
        self.text_view.get_buffer().set_highlight_syntax(highlight)

    def set_highlight_matching_brackets(self, highlight=CONF_HIGHLIGHT_MATCHING_BRACKETS):
        self.text_view.get_buffer().set_highlight_matching_brackets(highlight)

    def set_max_undo_levels(self, levels=CONF_MAX_UNDO_LEVELS):
        self.text_view.get_buffer().set_max_undo_levels(levels)

    def set_wrap_mode(self, mode=CONF_WRAP_MAP['None']):
        mode = CONF_WRAP_MAP[self.wrapping]
        self.text_view.set_wrap_mode(mode)

    def set_wrapping(self, wrap=CONF_WRAP[0]):
        self.wrapping = wrap

    def set_font(self, font=CONF_FONT):
        self.text_view.modify_font(pango.FontDescription(font))

    def set_overwrite(self, overwrite=CONF_OVERWRITE):
        self.text_view.set_overwrite(overwrite)

    def set_style_scheme(self, scheme=CONF_STYLE_SCHEME[0]):
            mgr = gtksourceview2.style_scheme_manager_get_default()
            style_scheme = mgr.get_scheme(scheme)
            if style_scheme:
                self.text_view.get_buffer().set_style_scheme(style_scheme)
				
    def __toolbarBtnNewEvent(self,arg):
        self.on_new_menu_item_activate(None)
		
    def __toolbarBtnOpenEvent(self,arg):
        self.on_open_menu_item_activate(None)
		
    def __toolbarBtnSaveEvent(self,arg):
        self.on_save_menu_item_activate(None)
	
    def __toolbarLoadScriptEvent(self,arg):
        print(self.plugin_menus)
        self.__toolbarBtnSaveEvent(None) # save file first
        self.plugin_menu_items[0].activate()
		
    def	__toolbarTerminalEvent(self,arg):
        self.plugin_menu_items[1].activate()
		
    def __toolbarSnippetsEvent(self,arg):
        self.plugin_menu_items[2].activate()
		
    # We use the initialization of the Edile class to establish
    # references to the widgets we'll need to work with in the callbacks for
    # various signals. This is done using the XML in the U_I string
    def __init__(self):
		# Default values
		self.filename = None
		self.language = None
		self.text_encoding = None
		self.about_dialog = None
		self.search_string = ""
		self.replacement_string = ""
		self.font_dialog = None
		self.edit_loc = 0
		self.edit_len = 0
		self.search_did_wrap = False

		self.plugin_interface = Edile.PluginInterface()
		self.plugin_interface.set_parent(self)
		# search options
		self.search_case_sensitive = False
		self.search_is_whole_word = False

		import locale
		locale.setlocale(locale.LC_ALL, '')

		self.set_highlight_changes(CONF_HIGHLIGHT_CHANGES_SINCE_SAVE)
		# use GtkBuilder to build our interface from the XML file
		try:
			builder = gtk.Builder()
			#need to specify len() to work around pygtk <2.13 bug.
			builder.add_from_string(U_I,len(U_I))
			builder.add_from_string(SEARCH_UI,len(SEARCH_UI))
		except:
			self.error_message("Failed to load UI")
			sys.exit(1)

		# get the widgets which will be referenced in callbacks
		self.window = builder.get_object("window")
		self.window.set_icon_from_file(BASE_PATH+"/icons/icon.ico")
		self.statusbar = builder.get_object("statusbar")
		self.text_view = builder.get_object("text_view")
		self.scroll_view = builder.get_object("scrolledwindow")
		self.search_window = builder.get_object('search_window')
		self.search_field = builder.get_object("search_find_field")
		self.replace_field = builder.get_object("search_replace_field")
		self.menubar = builder.get_object("menubar1")
        
		#toolbar
		toolbar = gtk.Toolbar()
		toolbar.set_orientation(gtk.ORIENTATION_HORIZONTAL)
		toolbar.set_style(gtk.TOOLBAR_BOTH)
		toolbar.set_border_width(3)
		#toolbar buttons
		newtb = gtk.ToolButton(gtk.STOCK_NEW)
		newtb.set_label("New")
		opentb = gtk.ToolButton(gtk.STOCK_OPEN)
		opentb.set_label("Open")
		savetb = gtk.ToolButton(gtk.STOCK_SAVE)
		savetb.set_label("Save")
		loadScriptb = gtk.ToolButton()
		icon = gtk.Image()
		icon.set_from_file(BASE_PATH+"/icons/loadScript.png")
		loadScriptb.set_icon_widget(icon)
		loadScriptb.set_label("Load Script")
		
		terminaltb = gtk.ToolButton()
		icon = gtk.Image()
		icon.set_from_file(BASE_PATH+"/icons/terminal.png")
		terminaltb.set_icon_widget(icon)
		terminaltb.set_label("Terminal")
		
		snippetstb = gtk.ToolButton()
		icon = gtk.Image()
		icon.set_from_file(BASE_PATH+"/icons/snippets.png")
		snippetstb.set_icon_widget(icon)
		snippetstb.set_label("Snippets")
		sep = gtk.SeparatorToolItem()	
		sep.set_draw(True)
		toolbar.insert(newtb, 0)
		toolbar.insert(opentb, 1)
		toolbar.insert(savetb, 2)
		toolbar.insert(sep, -1)
		
		toolbar.insert(loadScriptb, 4)
		toolbar.insert(terminaltb, 5)
		toolbar.insert(snippetstb, 6)
		
		#events
		newtb.connect("clicked", self.__toolbarBtnNewEvent)
		opentb.connect("clicked", self.__toolbarBtnOpenEvent)
		savetb.connect("clicked", self.__toolbarBtnSaveEvent)
		loadScriptb.connect("clicked", self.__toolbarLoadScriptEvent)
		terminaltb.connect("clicked", self.__toolbarTerminalEvent)
		snippetstb.connect("clicked", self.__toolbarSnippetsEvent)
		
		vbox = builder.get_object("vbox2")
		vbox.pack_start(toolbar, False, False, 0)			
        #____________________________________________________________________
		###
		# command line options
		###
		parser = OptionParser()
		parser.add_option("-p", "--plain-text", action="store_false", dest="using_source_view", default=True, help="don't use GTKSourceView if available")
		parser.add_option("-q", "--quiet", action="store_false", dest="verbose", default=True, help="don't print status messages to stdout")

		(options, args) = parser.parse_args()
		using_source_view = options.using_source_view
		#if parser.has_option("plain-text"):

		# to switch off option parser
		#args = sys.argv


		#gtksourceview is installed and we should use it, set up dev stuff
		if (using_source_view):
		#if 0:
			self.scroll_view.remove(self.text_view)
			self.text_view = gtksourceview2.View()
			self.set_auto_indent(CONF_AUTO_INDENT)
			self.set_highlight_current_line(CONF_HIGHLIGHT_CURRENT_LINE)
			self.set_show_line_numbers(CONF_SHOW_LINE_NUMBERS)
			self.set_show_right_margin(CONF_SHOW_RIGHT_MARGIN)
			self.set_insert_spaces_instead_of_tabs(CONF_SPACES_INSTEAD_OF_TABS)
			self.set_tab_width(CONF_TAB_WIDTH)
			self.set_indent_width(CONF_INDENT_WIDTH)
			self.set_right_margin_position(CONF_RIGHT_MARGIN_POSITION)
			self.set_smart_home_end(CONF_SMART_HOME_END_TYPE_MAP[CONF_SMART_HOME_END_TYPE[0]])
			self.set_indent_on_tab(CONF_INDENT_ON_TAB)

			# make a buffer for the view
			self.text_view.set_buffer(gtksourceview2.Buffer())

			# configure the source view buffer
			self.set_highlight_syntax(CONF_HIGHLIGHT_SYNTAX)
			self.set_highlight_matching_brackets(CONF_HIGHLIGHT_MATCHING_BRACKETS)
			self.set_max_undo_levels(CONF_MAX_UNDO_LEVELS)
			self.text_view.show()
			self.text_view.set_events(gtk.gdk.POINTER_MOTION_MASK | gtk.gdk.POINTER_MOTION_HINT_MASK | gtk.gdk.BUTTON_PRESS_MASK | gtk.gdk.BUTTON_RELEASE_MASK)
			self.text_view.set_left_margin(2)
			self.text_view.set_right_margin(2)
			self.scroll_view.add(self.text_view)

			self.set_style_scheme()

		# non-gtksrcview-exclusive options
		# set the text view font
		self.set_font(CONF_FONT)

		self.set_overwrite(CONF_OVERWRITE)

		# set the text view wrapping
		self.set_wrapping(CONF_WRAP[0])

		if not self.wrapping: self.wrapping = 'None'

		self.set_wrap_mode(CONF_WRAP_MAP[self.wrapping])

		wrap_none_menu_item = builder.get_object("wrap_none_menu_item")
		wrap_char_menu_item = builder.get_object("wrap_char_menu_item")
		wrap_word_menu_item = builder.get_object("wrap_word_menu_item")

		if self.wrapping == 'None' : wrap_none_menu_item.set_active(True)
		if self.wrapping == 'Character' : wrap_char_menu_item.set_active(True)
		if self.wrapping == 'Word' : wrap_word_menu_item.set_active(True)

		self.statusbar_manager = Edile.StatusBarManager()
		self.statusbar_manager.set_statusbar(self.statusbar)

		buff = self.text_view.get_buffer()
		self.change_highlight = buff.create_tag("change_highlight", background_set="True",background=CONF_CHANGE_HIGHLIGHT)
		buff.connect("modified-changed", self.on_text_buffer_modified_changed,None)
		buff.connect("insert-text",self.on_text_buffer_insert_text,None)
		buff.connect("delete-range",self.on_text_buffer_delete_range,None)
		buff.connect("changed",self.on_text_buffer_changed,None)
        #buff.connect("mark-set",self.on_text_buffer_mark_set,None)

        # connect signals
		builder.connect_signals(self)

        # setup to accept file drags
		TARGET_TYPE_URI_LIST = 80
		dnd_list = [ ( 'text/uri-list', 0, TARGET_TYPE_URI_LIST ) ]
        #dnd_list = [("text/uri-list", 0, 25)]
		self.statusbar.drag_dest_set( gtk.DEST_DEFAULT_MOTION |
                  gtk.DEST_DEFAULT_HIGHLIGHT | gtk.DEST_DEFAULT_DROP,
                  dnd_list, gtk.gdk.ACTION_COPY)
        #self.text_view.drag_dest_set(0, [], 0)
		self.statusbar.connect('drag_motion', self.on_drag_motion)
        #self.text_view.connect('drag_drop', self.on_drag_drop)
		self.statusbar.connect('drag_data_received', self.on_drag_data_received,None)
		self.statusbar.connect('drag_end', self.on_drag_end,None)
        #self.text_view.connect('drag_data_received', self.on_drag_data_received,None)
        #self.text_view.connect('drag_end', self.on_drag_end,None)

        # set the default icon to the GTK "edit" icon
		gtk.window_set_default_icon_name(gtk.STOCK_EDIT)

        # setup and initialize our statusbar
		self.statusbar_cid = self.statusbar.get_context_id("EduCIAA Python Editor")

        # setup search window
		self.search_window.set_destroy_with_parent(True)
		self.search_window.set_transient_for(self.window)
		self.search_window.set_position(gtk.WIN_POS_CENTER_ON_PARENT)
		self.search_window.set_title('Find | EduCIAA Python Editor')
		self.search_window.set_type_hint(gtk.gdk.WINDOW_TYPE_HINT_DIALOG)

		#autocomplete
		self.view_completion = self.text_view.get_completion()
		self.view_completion.add_provider(MyCompletionProvider())
		#___________________

        ###
        # load plugins
        ###
		self.load_plugins()
        # figure out what to put in the window and set the filename to
		should_load_default_file = (CONF_DEFAULT_FILE != "")


        # open file from command line or stdin/pipe
		if len(args) > 0:
			# first file from command line
			self.filename = args[0]
			# don't load the default document
			should_load_default_file = False

			if len(args) > 2:
				# there are other filenames. spawn instances for them
				other_filenames = sys.argv[2:]
				[self.spawn(other_file) for other_file in other_filenames]

			if os.path.exists(self.filename):
				# open first file
				self.load_file(self.filename)
			else:
				# file doesn't exist. create it on save.
				self.reset_default_status()

				# let user know what's going on
				if os.access(os.path.dirname(self.filename),os.W_OK):
					print "\nfile %s will be created."%(self.filename)
				else:
					print "\nfile %s not writable!"%(self.filename)
		'''		
		if not sys.stdin.isatty():
			# open from pipe
			#self.filename = None
			#^you can log output this way
			buffer = self.text_view.get_buffer()
			buffer.set_text(sys.stdin.read())
			# move insertion point and scroll to top
			buffer.place_cursor(buffer.get_start_iter())
			self.reset_default_status()
		else:
			# open default document if appropriate
			if should_load_default_file:
				if (os.path.exists(CONF_DEFAULT_FILE)) & (os.access(CONF_DEFAULT_FILE,os.W_OK)):
					self.load_file(CONF_DEFAULT_FILE)
				else:
					print "\n%s doesn't exist. not opening\n"%(CONF_DEFAULT_FILE)
					self.reset_default_status()
			else:
				self.reset_default_status()
		'''


        #tv_dnd_list = self.text_view.drag_dest_get_target_list()

        #tv_dnd_list.extend(dnd_list)
        #self.text_view.drag_dest_set_target_list(tv_dnd_list)
        
		#enable python highlight
		buffer = self.text_view.get_buffer()
		language = gtksourceview2.language_manager_get_default().get_language("python")
		try:
			buffer.set_language(language)
			buffer.set_highlight_syntax(CONF_HIGHLIGHT_SYNTAX)
		except AttributeError:
			pass
		#________________________	

    # Run main application window
    def main(self):
		gtk.gdk.threads_init()
		self.window.show_all()
		gtk.main()
		
if __name__ == "__main__":
    splScr = splashScreen()    
    while gtk.events_pending():
        gtk.main_iteration()        
    time.sleep(2)
    editor = Edile()
    tipsWindow = TipsWindow(None,BASE_PATH)
    tipsWindow.showTips()
    splScr.window.destroy() 
    editor.main()
