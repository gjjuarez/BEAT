# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Figure7x86ArchitectureError.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ArchitectureError(object):
    def setupUi(self, ArchitectureError):
        ArchitectureError.setObjectName("ArchitectureError")

        self.geo = QtWidgets.QDesktopWidget().screenGeometry()
        ArchitectureError.resize(self.geo.width()/2, self.geo.height()/3)

        ArchitectureError.setMaximumSize(QtCore.QSize(16777215, 16777215))


        self.gridLayout_2 = QtWidgets.QGridLayout(ArchitectureError)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.groupBox = QtWidgets.QGroupBox(ArchitectureError)
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.readme_pushbutton = QtWidgets.QPushButton(self.groupBox)
        self.readme_pushbutton.setObjectName("readme_pushbutton")
        self.gridLayout.addWidget(self.readme_pushbutton, 2, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(484, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 2, 1, 1, 1)
        self.ok_pushbutton = QtWidgets.QPushButton(self.groupBox)
        self.ok_pushbutton.setObjectName("ok_pushbutton")
        self.ok_pushbutton.clicked.connect(self.close_window)
        self.gridLayout.addWidget(self.ok_pushbutton, 2, 2, 1, 1)
        self.error_message_type_lineedit = QtWidgets.QLineEdit(self.groupBox)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(114, 159, 207))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(114, 159, 207))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        self.error_message_type_lineedit.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.error_message_type_lineedit.setFont(font)
        self.error_message_type_lineedit.setAutoFillBackground(False)
        self.error_message_type_lineedit.setAlignment(QtCore.Qt.AlignCenter)
        self.error_message_type_lineedit.setReadOnly(True)
        self.error_message_type_lineedit.setObjectName("error_message_type_lineedit")
        self.gridLayout.addWidget(self.error_message_type_lineedit, 0, 0, 1, 3)
        self.textBrowser = QtWidgets.QTextBrowser(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.textBrowser.setFont(font)
        self.textBrowser.setObjectName("textBrowser")
        self.gridLayout.addWidget(self.textBrowser, 1, 0, 1, 3)
        self.gridLayout_2.addWidget(self.groupBox, 0, 0, 1, 1)
        self.ok_pushbutton.clicked.connect(self.close_window)

        self.retranslateUi(ArchitectureError)
        QtCore.QMetaObject.connectSlotsByName(ArchitectureError)

    def close_window(self):
        import sys
        sys.exit()


    def retranslateUi(self, ArchitectureError):
        _translate = QtCore.QCoreApplication.translate
        ArchitectureError.setWindowTitle(_translate("ArchitectureError", "Form"))
        self.readme_pushbutton.setText(_translate("ArchitectureError", "README"))
        self.ok_pushbutton.setText(_translate("ArchitectureError", "OK"))
        self.error_message_type_lineedit.setText(_translate("ArchitectureError", "Error Message: x86 Architecture Binary File"))
        self.textBrowser.setHtml(_translate("ArchitectureError", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt;\">The system only supports executable binary files that are of x86 architecture. More information on accepted file types can be found in the README. <br /></span></p></body></html>"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ArchitectureError = QtWidgets.QWidget()
    ui = Ui_ArchitectureError()
    ui.setupUi(ArchitectureError)
    ArchitectureError.show()
    sys.exit(app.exec_())
