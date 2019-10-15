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
        #f.write(str(output) + "\n")
        #f.close()



class EmbTerminalLinux(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(EmbTerminalLinux, self).__init__(parent)
        self.process = SandboxProcess(self)
        self.terminal = QtWidgets.QWidget(self)
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.terminal)
        # Works also with urxvt:

    def begin_static(self):
        self.process.start('xterm',[ '-hold', '-e', 'python', 'radare2_scripts/radare_commands_interface.py', 'static'])
        self.process.waitForFinished();

    def begin_dynamic(self):
        self.process.start('xterm',[ '-hold', '-e', 'python', 'radare2_scripts/radare_commands_interface.py', 'dynamic'])
        self.process.waitForFinished();

    def kill_process(self):
        self.process.kill()

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
