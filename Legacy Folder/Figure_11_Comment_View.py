# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Figure_11_Comment_View.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Figure_11_Comment_View(object):
    def setupUi(self, Figure_11_Comment_View):
        Figure_11_Comment_View.setObjectName("Figure_11_Comment_View")
        Figure_11_Comment_View.resize(430, 300)
        self.centralwidget = QtWidgets.QWidget(Figure_11_Comment_View)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setObjectName("textEdit")
        self.gridLayout.addWidget(self.textEdit, 0, 0, 1, 2)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout.addWidget(self.pushButton_2, 1, 0, 1, 1)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 1, 1, 1, 1)
        Figure_11_Comment_View.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(Figure_11_Comment_View)
        self.statusbar.setObjectName("statusbar")
        Figure_11_Comment_View.setStatusBar(self.statusbar)

        self.retranslateUi(Figure_11_Comment_View)
        QtCore.QMetaObject.connectSlotsByName(Figure_11_Comment_View)

    def retranslateUi(self, Figure_11_Comment_View):
        _translate = QtCore.QCoreApplication.translate
        Figure_11_Comment_View.setWindowTitle(_translate("Figure_11_Comment_View", "MainWindow"))
        self.pushButton_2.setText(_translate("Figure_11_Comment_View", "Clear"))
        self.pushButton.setText(_translate("Figure_11_Comment_View", "Save"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Figure_11_Comment_View = QtWidgets.QMainWindow()
    ui = Ui_Figure_11_Comment_View()
    ui.setupUi(Figure_11_Comment_View)
    Figure_11_Comment_View.show()
    sys.exit(app.exec_())
