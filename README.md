# Python editor for EDU-CIAA

This project is based on EDILE. http://edile.googlecode.com

Directories and files:
  - binaries: Here you will find executables for several Operating Systems
  - snippets: In snippets.xml file you will find examples the IDE will load as snippets
  - Main.py: Start the IDE with this file

### Running the code from binaries

##### Linux
In binaries/debian directory you will find a zip file with Linux executables and a deb package to install.

##### Windows
In binaries/windows directory you will find a zip file with Windows executables and a setup wizard installer.



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
