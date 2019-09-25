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
        Figure10OutputFieldView.setTitle("")
        Figure10OutputFieldView.setFlat(False)
        self.gridLayout = QtWidgets.QGridLayout(Figure10OutputFieldView)
        self.gridLayout.setObjectName("gridLayout")
        self.name_lineedit = QtWidgets.QLineEdit(Figure10OutputFieldView)
        self.name_lineedit.setObjectName("name_lineedit")
        self.gridLayout.addWidget(self.name_lineedit, 0, 1, 1, 1)
        self.generate_button = QtWidgets.QPushButton(Figure10OutputFieldView)
        self.generate_button.setObjectName("generate_button")
        self.gridLayout.addWidget(self.generate_button, 4, 1, 1, 1)
        self.description_label = QtWidgets.QLabel(Figure10OutputFieldView)
        self.description_label.setObjectName("description_label")
        self.gridLayout.addWidget(self.description_label, 1, 0, 1, 1)
        self.location_lineedit = QtWidgets.QLineEdit(Figure10OutputFieldView)
        self.location_lineedit.setObjectName("location_lineedit")
        self.gridLayout.addWidget(self.location_lineedit, 2, 1, 1, 1)
        self.name_label = QtWidgets.QLabel(Figure10OutputFieldView)
        self.name_label.setObjectName("name_label")
        self.gridLayout.addWidget(self.name_label, 0, 0, 1, 1)
        self.location_label = QtWidgets.QLabel(Figure10OutputFieldView)
        self.location_label.setObjectName("location_label")
        self.gridLayout.addWidget(self.location_label, 2, 0, 1, 1)
        self.description_textedit = QtWidgets.QTextEdit(Figure10OutputFieldView)
        self.description_textedit.setObjectName("description_textedit")
        self.gridLayout.addWidget(self.description_textedit, 1, 1, 1, 1)
        self.browse_button = QtWidgets.QPushButton(Figure10OutputFieldView)
        self.browse_button.setObjectName("browse_button")
        self.gridLayout.addWidget(self.browse_button, 3, 1, 1, 1)
        self.description_label.setBuddy(self.description_textedit)
        self.name_label.setBuddy(self.name_lineedit)
        self.location_label.setBuddy(self.location_lineedit)

        self.retranslateUi(Figure10OutputFieldView)
        QtCore.QMetaObject.connectSlotsByName(Figure10OutputFieldView)
        Figure10OutputFieldView.setTabOrder(self.name_lineedit, self.description_textedit)
        Figure10OutputFieldView.setTabOrder(self.description_textedit, self.location_lineedit)
        Figure10OutputFieldView.setTabOrder(self.location_lineedit, self.browse_button)
        Figure10OutputFieldView.setTabOrder(self.browse_button, self.generate_button)

    def retranslateUi(self, Figure10OutputFieldView):
        _translate = QtCore.QCoreApplication.translate
        Figure10OutputFieldView.setWindowTitle(_translate("Figure10OutputFieldView", "Output Field View"))
        self.generate_button.setText(_translate("Figure10OutputFieldView", "Generate"))
        self.description_label.setText(_translate("Figure10OutputFieldView", "Description"))
        self.name_label.setText(_translate("Figure10OutputFieldView", "Name"))
        self.location_label.setText(_translate("Figure10OutputFieldView", "Location"))
        self.description_textedit.setToolTip(_translate("Figure10OutputFieldView", "<html><head/><body><p>Name</p></body></html>"))
        self.browse_button.setText(_translate("Figure10OutputFieldView", "Browse"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Figure10OutputFieldView = QtWidgets.QGroupBox()
    ui = Ui_Figure10OutputFieldView()
    ui.setupUi(Figure10OutputFieldView)
    Figure10OutputFieldView.show()
    sys.exit(app.exec_())
