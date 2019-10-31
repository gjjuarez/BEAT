# BEAT Version 1.2
Currently, this repository contains the UI files of BEAT, and also a version of the main window that combines many of the other UI pages and meant to filter the results of a binary analysis.

## BUILD
To BUILD the python file of the main page run
`pyuic5 -x BEAT\:\ Behavior\ Extraction\ and\ Analysis\ Tool.ui -o main.py`
To build executable out of python file
`pyinstaller main.py`

## DEPENDENCIES
To build, the only dependencies are
* Python 3 ver. 3.8.0 - website: https://www.python.org/downloads
* PyQT5 5.13.1 - command line: pip install PyQt5
* Radare2 ver. 4.0.0 website: https://wwww.radare.org/r/
* Jinja ver. 2.10.3 - website: jinja.pocoo.org
* pyinstaller ver. 3.5 - commmand line: pip install pyinstaller

## TUTORIAL
	1. Download Python3 from https://www.python.org/downloads.
	2. Download Radare2 from https://wwww.radare.org/r/
	3. Download Jinja from jinja.pocoo.org
	
	For Windows
		4. Navigate to the Downloads Folder an run the Python3 installation.
		5. In the command prompt type pip install PyQt5
		6. type pip install pyinstaller
		7. type `pyuic5 -x BEAT\:\ Behavior\ Extraction\ and\ Analysis\ Tool.ui -o main.py`
		8. type `pyinstaller main.py`
	
	For Linux:
		4. Go into the terminal and type apt-get update
		5. type cd Downloads
		6. type tar -xvf Python-3.8.0.tar.xz
		7. type cd Python3.8.0
		8. type ./configure
		9. type make
		10. type make install
		11. type python3 -v
		12. type apt-get install python3-pip
		13. type pip install PyQt5
		14. type pip install pyinstaller
		15. type git clone https://github.com/gjjuarez/Team01_BEAT.git
		16. type `pyuic5 -x BEAT\:\ Behavior\ Extraction\ and\ Analysis\ Tool.ui -o main.py`
		17. type `pyinstaller main.py`
