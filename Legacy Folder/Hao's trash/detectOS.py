import platform
import sys
from PyQt5 import QtCore, QtWidgets

class EmbTerminal(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(EmbTerminal, self).__init__(parent)
        self.process = QtCore.QProcess(self)
        self.terminal = QtWidgets.QWidget(self)
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.terminal)
        # Works also with urxvt:
        self.process.start('urxvt',['-embed', str(int(self.winId()))])
        self.setFixedSize(640, 480)


current_OS = platform.system()

if current_OS == "Windows":
    print("Satya")
elif current_OS == "Linux":
    print("Unix bish")
else: 
	print("This tool is not supported by your current Operating system." + "\n" + "Try using BEAT on Windows or Linux.")