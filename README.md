# BEAT Version 1.2
Currently, this repository contains the UI files of BEAT, and also a version of the main window that combines many of the other UI pages and meant to filter the results of a binary analysis.

## BUILD
To BUILD the python file of the main page run
`pyuic5 -x BEAT\:\ Behavior\ Extraction\ and\ Analysis\ Tool.ui -o main.py`
To build executable out of python file
`pyinstaller main.py`

## DEPENDENCIES
To build, the only dependencies are
* Python 3 ver. 3.8.0 https://www.python.org/downloads
* PyQT5 5.13.1 pip install PyQt5
* Radare2 ver. 4.0.0 https://wwww.radare.org/r/
* Jinja ver. 2.10.3 jinja.pocoo.org
* pyinstaller

## TUTORIAL
	1. Download Python3 from https://www.python.org/downloads.
	2. Download Radare2 from https://wwww.radare.org/r/
	3. Download Jinja from jinja.pocoo.org
	
	For Windows
		7. Navigate to the Downloads Folder an run the Python3 installation.
		8. In the command prompt type pip install PyQt5
		9. In the command prompt type pip install pyinstaller
		10. Run main_window2.exe from the build directory in Team01_Beat you opened earlier.
		11. `pyuic5 -x BEAT\:\ Behavior\ Extraction\ and\ Analysis\ Tool.ui -o main.py`
		12. `pyinstaller main.py`
	
	For Linux:
		7. Go into the terminal and type apt-get update
		8. cd Downloads
		9. tar -xvf Python-3.8.0.tar.xz
		10. cd Python3.8.0
		11. ./configure
		12. make
		13. make install
		14. python3 -v
		15. apt-get install python3-pip
		16. pip install PyQt5
		18. pip install pyinstaller
		19. git clone 
		20. Run main_window2.exe from the build directory in Team01_Beat you opened earlier.
