# Python editor para EDU-CIAA

Este proyecto esta basado en EDILE http://edile.googlecode.com


Archivos y directorios:
  - Main.py: Ejecutar el IDE usando este archivo
  - snippets/snippets.xml: En el archivo snippets.xml se encontrarán ejemplos que el IDE cargará como snippets
  - LICENSE.txt: Licencia el proyecto
  - tests: Dentro de este directorio se encuentran los tests unitarios desarrollados
  - PyInstaller-3.1: Dentro de este directorio se encuentran las herramientas para generar un programa ejecutable


### Ejecutar el IDE desde binarios

Seleccionar el instalador desde la sección releases: https://github.com/ernesto-g/educiaa_python_editor/releases
 

### Ejecutar el IDE desde el código fuente

##### Linux
Se requieren los siguientes packages:
  - git
  - python-gtksourceview2
  - python-gtk2
  - python-serial
  

##### Windows
Se requieren los siguientes programas:
  - git bash
  - python-2.7
  - pygtk-all-in-one-2.24.2.win32-py2.7
  - pyserial-2.7.win32_py3k
  - pywin32-219.win32-py2.7

##### OSX
Se requieren los siguientes packages:
  - git
  - gtksourceview
  
Una vez que los paquetes se encuentran instalados, abrir una terminal y escribir:

```sh
$ git clone https://github.com/ernesto-g/educiaa_python_editor.git
$ cd educiaa_python_editor
$ python Main.py
```

##Desarrollador

### Crear un ejecutable para Windows:

```sh
$ cd PyInstaller-3.1
$ python pyinstaller.py --clean --noconsole --ico ../icons/icon.ico ../Main.py
```
Se generará el archivo ejecutable Main.exe en el directorio Main/dist/Main.
Copiar los archivos que en encuentran en PyInstaller-3.1/extraFiles a PyInstaller-3.1/Main/dist/Main

### Crear un ejecutable para Linux:

```sh
$ cd PyInstaller-3.1
$ python pyinstaller.py --clean --noconsole --ico ../icons/icon.ico ../Main.py
```
Se generará el archivo ejecutable Main en el directorio Main/dist/Main.
Copiar los archivos que en encuentran en PyInstaller-3.1/extraFiles a PyInstaller-3.1/Main/dist/Main


### Correr test unitarios (Solo Linux)
La EDU-CIAA debe estar conectada a la PC y debe haber al menos un device ttyUSB.

```sh
$ python tests/EditorTest.py
```

