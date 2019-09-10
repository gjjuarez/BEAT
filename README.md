# BEAT
Currently, this repository contains the UI files of BEAT, and also a version of the main window that combines many of the other UI pages.

## BUILD
To BUILD the python file of the main page run
`pyuic5 -x BEAT\:\ Behavior\ Extraction\ and\ Analysis\ Tool.ui -o main.py`
To build executable out of python file
`pyinstaller main.py`

## DEPENDENCIES
To build, the only dependencies are
* Python 3
* PyQT5
* pyinstaller
