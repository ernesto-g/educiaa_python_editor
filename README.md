# Python editor for EDU-CIAA

[Spanish Version](README_ES.md)

This project is based on EDILE. http://edile.googlecode.com

Directories and files:
  - Main.py: Start the IDE with this file
  - snippets/snippets.xml: In snippets.xml file you will find examples the IDE will load as snippets
  - LICENSE.txt: Project license
  - tests: In this directory you will find unit tests developed for this IDE
  - PyInstaller-3.1: Tools to generate an IDE's executable version


### Running the code from binaries

Download the proper installer from releases section: https://github.com/ernesto-g/educiaa_python_editor/releases



### Running the code from source

##### Linux
The following packages are required:
  - git
  - python-gtksourceview2
  - python-gtk2
  - python-serial
  

##### Windows
The following programs are required:
  - git bash
  - python-2.7
  - pygtk-all-in-one-2.24.2.win32-py2.7
  - pyserial-2.7.win32_py3k
  - pywin32-219.win32-py2.7

##### OSX
The following packages are required:
  - git
  - gtksourceview3
  - pygtksourceview
  
Open a terminal and write:

```sh
$ git clone https://github.com/ernesto-g/educiaa_python_editor.git
$ cd educiaa_python_editor
$ python Main.py
```


##Developer

### Creating Windows Executable

```sh
$ cd PyInstaller-3.1
$ python pyinstaller.py --clean --noconsole --ico ../icons/icon.ico ../Main.py
```
Executable file Main.exe will be found in Main/dist/Main directory.
Copy files in PyInstaller-3.1/extraFiles to PyInstaller-3.1/Main/dist/Main

### Creating Linux Executable

```sh
$ cd PyInstaller-3.1
$ python pyinstaller.py --clean --noconsole --ico ../icons/icon.ico ../Main.py
```
Executable file Main will be found in Main/dist/Main directory.
Copy files in PyInstaller-3.1/extraFiles to PyInstaller-3.1/Main/dist/Main

### Running unit tests (only Linux)
Must be at least 1 serial device in the computer. (EDU-CIAA must be connected by USB)

```sh
$ python tests/EditorTest.py
```

