# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Figure_10_Output_field_View.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Figure_10_Output_Field_View(object):
    def setupUi(self, Figure_10_Output_Field_View):
        Figure_10_Output_Field_View.setObjectName("Figure_10_Output_Field_View")
        Figure_10_Output_Field_View.resize(400, 300)
        self.centralwidget = QtWidgets.QWidget(Figure_10_Output_Field_View)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.textEdit_2 = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_2.setObjectName("textEdit_2")
        self.gridLayout.addWidget(self.textEdit_2, 1, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.gridLayout.addWidget(self.lineEdit_2, 2, 1, 1, 1)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 3, 1, 1, 1)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout.addWidget(self.pushButton_2, 4, 1, 1, 1)
        Figure_10_Output_Field_View.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(Figure_10_Output_Field_View)
        self.statusbar.setObjectName("statusbar")
        Figure_10_Output_Field_View.setStatusBar(self.statusbar)
        self.label.setBuddy(self.lineEdit)
        self.label_2.setBuddy(self.textEdit_2)
        self.label_3.setBuddy(self.lineEdit_2)

        self.retranslateUi(Figure_10_Output_Field_View)
        QtCore.QMetaObject.connectSlotsByName(Figure_10_Output_Field_View)

    def retranslateUi(self, Figure_10_Output_Field_View):
        _translate = QtCore.QCoreApplication.translate
        Figure_10_Output_Field_View.setWindowTitle(_translate("Figure_10_Output_Field_View", "MainWindow"))
        self.label.setText(_translate("Figure_10_Output_Field_View", "Name"))
        self.label_2.setText(_translate("Figure_10_Output_Field_View", "Description"))
        self.textEdit_2.setToolTip(_translate("Figure_10_Output_Field_View", "<html><head/><body><p>Name</p></body></html>"))
        self.label_3.setText(_translate("Figure_10_Output_Field_View", "Location"))
        self.pushButton.setText(_translate("Figure_10_Output_Field_View", "Browse"))
        self.pushButton_2.setText(_translate("Figure_10_Output_Field_View", "Generate"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Figure_10_Output_Field_View = QtWidgets.QMainWindow()
    ui = Ui_Figure_10_Output_Field_View()
    ui.setupUi(Figure_10_Output_Field_View)
    Figure_10_Output_Field_View.show()
    sys.exit(app.exec_())
