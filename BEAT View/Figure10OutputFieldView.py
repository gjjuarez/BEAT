# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Figure10OutputFieldView.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Figure10OutputFieldView(object):
    def setupUi(self, Figure10OutputFieldView):
        Figure10OutputFieldView.setObjectName("Figure10OutputFieldView")
        Figure10OutputFieldView.resize(400, 300)
        self.centralwidget = QtWidgets.QWidget(Figure10OutputFieldView)
        self.centralwidget.setObjectName("centralwidget")
        self.description_label = QtWidgets.QLabel(self.centralwidget)
        self.description_label.setGeometry(QtCore.QRect(10, 35, 54, 172))
        self.description_label.setObjectName("description_label")
        self.generate_button = QtWidgets.QPushButton(self.centralwidget)
        self.generate_button.setGeometry(QtCore.QRect(70, 267, 320, 23))
        self.generate_button.setObjectName("generate_button")
        self.description_textedit = QtWidgets.QTextEdit(self.centralwidget)
        self.description_textedit.setGeometry(QtCore.QRect(70, 35, 320, 172))
        self.description_textedit.setObjectName("description_textedit")
        self.location_label = QtWidgets.QLabel(self.centralwidget)
        self.location_label.setGeometry(QtCore.QRect(10, 213, 54, 19))
        self.location_label.setObjectName("location_label")
        self.name_lineedit = QtWidgets.QLineEdit(self.centralwidget)
        self.name_lineedit.setGeometry(QtCore.QRect(70, 10, 320, 19))
        self.name_lineedit.setObjectName("name_lineedit")
        self.name_label = QtWidgets.QLabel(self.centralwidget)
        self.name_label.setGeometry(QtCore.QRect(10, 10, 54, 19))
        self.name_label.setObjectName("name_label")
        self.location_lineedit = QtWidgets.QLineEdit(self.centralwidget)
        self.location_lineedit.setGeometry(QtCore.QRect(70, 213, 320, 19))
        self.location_lineedit.setObjectName("location_lineedit")
        self.browse_button = QtWidgets.QPushButton(self.centralwidget)
        self.browse_button.setGeometry(QtCore.QRect(70, 238, 320, 23))
        self.browse_button.setObjectName("browse_button")
        Figure10OutputFieldView.setCentralWidget(self.centralwidget)
        self.description_label.setBuddy(self.description_textedit)
        self.location_label.setBuddy(self.location_lineedit)
        self.name_label.setBuddy(self.name_lineedit)

        self.retranslateUi(Figure10OutputFieldView)
        QtCore.QMetaObject.connectSlotsByName(Figure10OutputFieldView)

    def retranslateUi(self, Figure10OutputFieldView):
        _translate = QtCore.QCoreApplication.translate
        Figure10OutputFieldView.setWindowTitle(_translate("Figure10OutputFieldView", "MainWindow"))
        self.description_label.setText(_translate("Figure10OutputFieldView", "Description"))
        self.generate_button.setText(_translate("Figure10OutputFieldView", "Generate"))
        self.description_textedit.setToolTip(_translate("Figure10OutputFieldView", "<html><head/><body><p>Name</p></body></html>"))
        self.location_label.setText(_translate("Figure10OutputFieldView", "Location"))
        self.name_label.setText(_translate("Figure10OutputFieldView", "Name"))
        self.browse_button.setText(_translate("Figure10OutputFieldView", "Browse"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Figure10OutputFieldView = QtWidgets.QMainWindow()
    ui = Ui_Figure10OutputFieldView()
    ui.setupUi(Figure10OutputFieldView)
    Figure10OutputFieldView.show()
    sys.exit(app.exec_())
