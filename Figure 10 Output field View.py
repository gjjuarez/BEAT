# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Figure 10 Output field View.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_OutputfieldView(object):
    def setupUi(self, OutputfieldView):
        OutputfieldView.setObjectName("OutputfieldView")
        OutputfieldView.resize(400, 300)
        OutputfieldView.setTitle("")
        OutputfieldView.setFlat(False)
        self.gridLayout = QtWidgets.QGridLayout(OutputfieldView)
        self.gridLayout.setObjectName("gridLayout")
        self.lineEdit = QtWidgets.QLineEdit(OutputfieldView)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 0, 1, 1, 1)
        self.pushButton_2 = QtWidgets.QPushButton(OutputfieldView)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout.addWidget(self.pushButton_2, 4, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(OutputfieldView)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.lineEdit_2 = QtWidgets.QLineEdit(OutputfieldView)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.gridLayout.addWidget(self.lineEdit_2, 2, 1, 1, 1)
        self.label = QtWidgets.QLabel(OutputfieldView)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(OutputfieldView)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.textEdit_2 = QtWidgets.QTextEdit(OutputfieldView)
        self.textEdit_2.setObjectName("textEdit_2")
        self.gridLayout.addWidget(self.textEdit_2, 1, 1, 1, 1)
        self.pushButton = QtWidgets.QPushButton(OutputfieldView)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 3, 1, 1, 1)
        self.label_2.setBuddy(self.textEdit_2)
        self.label.setBuddy(self.lineEdit)
        self.label_3.setBuddy(self.lineEdit_2)

        self.retranslateUi(OutputfieldView)
        QtCore.QMetaObject.connectSlotsByName(OutputfieldView)
        OutputfieldView.setTabOrder(self.lineEdit, self.textEdit_2)
        OutputfieldView.setTabOrder(self.textEdit_2, self.lineEdit_2)
        OutputfieldView.setTabOrder(self.lineEdit_2, self.pushButton)
        OutputfieldView.setTabOrder(self.pushButton, self.pushButton_2)

    def retranslateUi(self, OutputfieldView):
        _translate = QtCore.QCoreApplication.translate
        OutputfieldView.setWindowTitle(_translate("OutputfieldView", "Output Field View"))
        self.pushButton_2.setText(_translate("OutputfieldView", "Generate"))
        self.label_2.setText(_translate("OutputfieldView", "Description"))
        self.label.setText(_translate("OutputfieldView", "Name"))
        self.label_3.setText(_translate("OutputfieldView", "Location"))
        self.textEdit_2.setToolTip(_translate("OutputfieldView", "<html><head/><body><p>Name</p></body></html>"))
        self.pushButton.setText(_translate("OutputfieldView", "Browse"))
