# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Figure 11 Comment View.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_CommentView(object):
    def setupUi(self, CommentView):
        CommentView.setObjectName("CommentView")
        CommentView.resize(400, 300)
        self.gridLayout = QtWidgets.QGridLayout(CommentView)
        self.gridLayout.setObjectName("gridLayout")
        self.textEdit = QtWidgets.QTextEdit(CommentView)
        self.textEdit.setObjectName("textEdit")
        self.gridLayout.addWidget(self.textEdit, 0, 0, 1, 2)
        self.pushButton_2 = QtWidgets.QPushButton(CommentView)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout.addWidget(self.pushButton_2, 1, 0, 1, 1)
        self.pushButton = QtWidgets.QPushButton(CommentView)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 1, 1, 1, 1)

        self.retranslateUi(CommentView)
        QtCore.QMetaObject.connectSlotsByName(CommentView)
        CommentView.setTabOrder(self.textEdit, self.pushButton)
        CommentView.setTabOrder(self.pushButton, self.pushButton_2)

    def retranslateUi(self, CommentView):
        _translate = QtCore.QCoreApplication.translate
        CommentView.setWindowTitle(_translate("CommentView", "Comment View"))
        self.pushButton_2.setText(_translate("CommentView", "Clear"))
        self.pushButton.setText(_translate("CommentView", "Save"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    CommentView = QtWidgets.QGroupBox()
    ui = Ui_CommentView()
    ui.setupUi(CommentView)
    CommentView.show()
    sys.exit(app.exec_())
