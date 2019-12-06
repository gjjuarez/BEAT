# BEAT Version 1.2
Currently, this repository contains the UI files of BEAT, and also a version of the main window that combines many of the other UI pages and meant to filter the results of a binary analysis.

## BUILD
To BUILD the python file of the main page run
`pyuic5 -x BEAT.ui -o UiView.py`
To build executable out of python file
`pyinstaller main.py`

## DEPENDENCIES
To build, the only dependencies are
* Python 3 ver. 3.8.0 - website: sudo apt install python3
* PyQT5 5.13.1 - command line: pip3 install PyQt5
* Radare2 ver. 4.0.0 website: https://github.com/radareorg/radare2.git 
* Pyinstaller ver. 3.5 - commmand line: pip3 install pyinstaller
* XMLJSON  ver. 0.2.0 - command line: pip3 install xmljson

## ADDITONAL USEFUL SOFTWARE (OPTIONAL)
* MongoDB Compass: GUI Representation & Control of Mongo Database - https://www.mongodb.com/products/compass

## TUTORIAL
	1. In the terminal type sudo apt install python3-pip
	2. In the terminal type pip3 install PyQt5 
	3. In the terminal type pip3 install xmljson
	4. In the terminal type sudo apt install git
 	5. Go to https://github.com/radareorg/radare2.git and type into the terminal git clone https://github.com/radareorg/radare2.git 
	6. In the terminal change directory to radare2
	7. In the terminal type sys/install.sh
	8. In the terminal type cd ~
	9. In the terminal type pip3 install r2pipe
	10. In the terminal type git clone https://github.com/mongodb/mongo.git
	11. In the terminal type sudo apt install mongodb
`	12.In the terminal type pip3 install pymongo
	13.Go to https://github.com/radareorg/radare2-r2pipe.git and type into the terminal git clone https://github.com/radareorg/radare2-r2pipe.git 
	14. Go to https://github.com/gjjuarez/Team01_BEAT/tree/master and type into the terminal git clone https://github.com/gjjuarez/Team01_BEAT.git
	15. Change directory to BEAT View with cd Team01_BEAT/’BEAT View’  
	16. To run type python3 UiMain.py
