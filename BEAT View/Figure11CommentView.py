# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Figure11CommentView.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Figure11CommentView(object):
    def setupUi(self, Figure11CommentView):
        Figure11CommentView.setObjectName("Figure11CommentView")
        Figure11CommentView.resize(509, 301)
        self.comment_view_widget = QtWidgets.QWidget(Figure11CommentView)
        self.comment_view_widget.setObjectName("comment_view_widget")
        self.gridLayout = QtWidgets.QGridLayout(self.comment_view_widget)
        self.gridLayout.setObjectName("gridLayout")
        self.comment_textedit = QtWidgets.QTextEdit(self.comment_view_widget)
        self.comment_textedit.setObjectName("comment_textedit")
        self.gridLayout.addWidget(self.comment_textedit, 0, 0, 1, 2)
        self.clear_button = QtWidgets.QPushButton(self.comment_view_widget)
        self.clear_button.setObjectName("clear_button")
        self.gridLayout.addWidget(self.clear_button, 1, 0, 1, 1)
        self.save_button = QtWidgets.QPushButton(self.comment_view_widget)
        self.save_button.setObjectName("save_button")
        self.gridLayout.addWidget(self.save_button, 1, 1, 1, 1)
        Figure11CommentView.setCentralWidget(self.comment_view_widget)

        self.retranslateUi(Figure11CommentView)
        QtCore.QMetaObject.connectSlotsByName(Figure11CommentView)

    def retranslateUi(self, Figure11CommentView):
        _translate = QtCore.QCoreApplication.translate
        Figure11CommentView.setWindowTitle(_translate("Figure11CommentView", "Comment View"))
        self.clear_button.setText(_translate("Figure11CommentView", "Clear"))
        self.save_button.setText(_translate("Figure11CommentView", "Save"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Figure11CommentView = QtWidgets.QMainWindow()
    ui = Ui_Figure11CommentView()
    ui.setupUi(Figure11CommentView)
    Figure11CommentView.show()
    sys.exit(app.exec_())
