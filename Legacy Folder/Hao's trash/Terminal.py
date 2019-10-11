#!/usr/bin/env python
#-*- coding:utf-8 -*-

import sys
import platform
from PyQt5 import QtCore, QtGui, QtWidgets


class embterminal(QtWidgets.QWidget):

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.process = QtCore.QProcess(self)
        self.terminal = QtWidgets.QWidget(self)
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.terminal)
        
        current_OS = platform.system()
        if current_OS == "Windows":
            print("Windows")
            self.process.start(
                'xterm',['-into', str(int(self.terminal.winId()))])
            print(self.winId())
        elif current_OS == "Linux":
            print("Linux")
            self.process.start(
                'urxvt',['-embed', str(int(self.terminal.winId()))])
            print(self.winId())
        else: 
            print("This tool is not supported by your current Operating system." + "\n" + "Try using BEAT on Windows or Linux.")

        self.setGeometry(1, 1, 800, 600)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main = embterminal()
    main.show()
    sys.exit(app.exec_())


'''
import sys
from PyQt5 import QtCore, QtWidgets


class EmbTerminalLinux(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(EmbTerminalLinux, self).__init__(parent)
        self.process = QtCore.QProcess(self)
        self.terminal = QtWidgets.QWidget(self)
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.terminal)
        # Works also with urxvt:
        self.process.start('urxvt',['-embed', str(int(self.winId()))])
        self.setFixedSize(640, 480)

class mainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(mainWindow, self).__init__(parent)

        central_widget = QtWidgets.QWidget()
        lay = QtWidgets.QVBoxLayout(central_widget)
        self.setCentralWidget(central_widget)

        tab_widget = QtWidgets.QTabWidget() #Find this part in View 
        lay.addWidget(tab_widget) 

        tab_widget.addTab(EmbTerminalLinux(), "EmbTerminal")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main = mainWindow()
    main.show()
    sys.exit(app.exec_())
'''