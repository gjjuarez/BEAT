# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DocumentFileName.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DocumentFileName(object):
    def setupUi(self, DocumentFileName):
        DocumentFileName.setObjectName("DocumentFileName")
        DocumentFileName.resize(276, 74)
        self.document_file_name_widget = QtWidgets.QWidget(DocumentFileName)
        self.document_file_name_widget.setObjectName("document_file_name_widget")
        self.gridLayout = QtWidgets.QGridLayout(self.document_file_name_widget)
        self.gridLayout.setObjectName("gridLayout")
        self.cancel_button = QtWidgets.QPushButton(self.document_file_name_widget)
        self.cancel_button.setObjectName("cancel_button")
        self.gridLayout.addWidget(self.cancel_button, 1, 0, 1, 1)
        self.confirm_button = QtWidgets.QPushButton(self.document_file_name_widget)
        self.confirm_button.setObjectName("confirm_button")
        self.gridLayout.addWidget(self.confirm_button, 1, 1, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(self.document_file_name_widget)
        self.lineEdit.setText("")
        self.lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 0, 0, 1, 2)
        DocumentFileName.setCentralWidget(self.document_file_name_widget)

        self.retranslateUi(DocumentFileName)
        QtCore.QMetaObject.connectSlotsByName(DocumentFileName)

    def retranslateUi(self, DocumentFileName):
        _translate = QtCore.QCoreApplication.translate
        DocumentFileName.setWindowTitle(_translate("DocumentFileName", "Name"))
        self.cancel_button.setText(_translate("DocumentFileName", "Cancel"))
        self.confirm_button.setText(_translate("DocumentFileName", "Confirm"))
        self.lineEdit.setPlaceholderText(_translate("DocumentFileName", "File Name"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DocumentFileName = QtWidgets.QMainWindow()
    ui = Ui_DocumentFileName()
    ui.setupUi(DocumentFileName)
    DocumentFileName.show()
    sys.exit(app.exec_())
