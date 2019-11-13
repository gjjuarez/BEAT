from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ArchitectureError(object):
    def setupUi(self, ArchitectureError):
        ArchitectureError.setObjectName("ArchitectureError")
        ArchitectureError.resize(688, 230)


app = QtWidgets.QApplication([])

error_dialog = QtWidgets.QErrorMessage()
error_dialog.showMessage('Oh no!')

app.exec_()