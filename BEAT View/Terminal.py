import sys
from PyQt5 import QtCore, QtWidgets

class SandboxProcess(QtCore.QProcess):
    def setupChildProcess(self):
        # Drop all privileges in the child process, and enter
        # a chroot jail.
        bashCommand = "tty"
        import subprocess
        sprocess = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        output, error = sprocess.communicate()
        print(output)
        #f = ("t.txt", "w+")
        #f.write(output)
        #f.close()



class EmbTerminalLinux(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(EmbTerminalLinux, self).__init__(parent)
        self.process = SandboxProcess(self)
        self.terminal = QtWidgets.QWidget(self)
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.terminal)
        # Works also with urxvt:
        self.process.start('urxvt',['-embed', str(int(self.winId())), '-e', 'tmux'])
        x = self.process.processId()
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
