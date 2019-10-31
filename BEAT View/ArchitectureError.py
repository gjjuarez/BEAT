# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Figure7x86Architecture Error.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ArchitectureError(object):
    def setupUi(self, ArchitectureError):
        ArchitectureError.setObjectName("ArchitectureError")
        ArchitectureError.resize(688, 230)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(184, 184, 184, 142))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(184, 184, 184, 142))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        ArchitectureError.setPalette(palette)
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.groupBox = QtWidgets.QGroupBox(self.dockWidgetContents)
        self.groupBox.setGeometry(QtCore.QRect(0, -20, 691, 231))
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.PluginView_4 = QtWidgets.QLineEdit(self.groupBox)
        self.PluginView_4.setGeometry(QtCore.QRect(0, 10, 691, 51))
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
        self.PluginView_4.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.PluginView_4.setFont(font)
        self.PluginView_4.setAutoFillBackground(False)
        self.PluginView_4.setAlignment(QtCore.Qt.AlignCenter)
        self.PluginView_4.setReadOnly(True)
        self.PluginView_4.setObjectName("PluginView_4")
        self.PluginView_3 = QtWidgets.QColumnView(self.groupBox)
        self.PluginView_3.setGeometry(QtCore.QRect(0, 60, 691, 171))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(184, 184, 184, 142))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(184, 184, 184, 142))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        self.PluginView_3.setPalette(palette)
        self.PluginView_3.setObjectName("PluginView_3")
        #self.pushButton = QtWidgets.QPushButton(self.groupBox)
        #self.pushButton.setGeometry(QtCore.QRect(534, 182, 81, 31))
        #self.pushButton.setObjectName("pushButton")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(30, 80, 501, 101))
        self.label.setTextFormat(QtCore.Qt.AutoText)
        self.label.setObjectName("label")
        self.PluginView_3.raise_()
        self.PluginView_4.raise_()
        #self.pushButton.raise_()
        self.label.raise_()
        ArchitectureError.setCentralWidget(self.dockWidgetContents)

        self.retranslateUi(ArchitectureError)
        QtCore.QMetaObject.connectSlotsByName(ArchitectureError)
        #self.pushButton.clicked.connect(self.close_window)

    def close_window():
        import sys
        sys.exit()

    def retranslateUi(self, ArchitectureError):
        _translate = QtCore.QCoreApplication.translate
        ArchitectureError.setWindowTitle(_translate("ArchitectureError", "DockWidget"))
        self.PluginView_4.setText(_translate("ArchitectureError", "Error Message: x86 Architecture Binary File"))
        #self.pushButton.setText(_translate("ArchitectureError", "OK"))
        self.label.setText(_translate("ArchitectureError", "<html><head/><body><p><span style=\" font-size:11pt; font-weight:600;\">The system only supports executable binary </span></p><p><span style=\" font-size:11pt; font-weight:600;\">files that are of x86 architecture. More information </span></p><p><span style=\" font-size:11pt; font-weight:600;\">on accepted files can be found in the </span><span style=\" font-size:11pt; font-weight:600; text-decoration: underline; color:#0000ff;\">README</span><span style=\" font-size:11pt; font-weight:600;\">.</span></p></body></html>"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ArchitectureError = QtWidgets.QDockWidget()
    ui = Ui_ArchitectureError()
    ui.setupUi(ArchitectureError)
    ArchitectureError.show()
    sys.exit(app.exec_())
