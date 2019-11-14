# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PluginDeletionWarning.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_PluginDeletionWarning(object):
    def setupUi(self, PluginDeletionWarning):
        PluginDeletionWarning.setObjectName("PluginDeletionWarning")
        
        ###########################
        # Resizing according to user's desktop
        ###########################
        self.geo = QtWidgets.QDesktopWidget().screenGeometry()
        PluginDeletionWarning.resize(self.geo.width()/2.3, self.geo.height()/3)
        PluginDeletionWarning.setMaximumSize(QtCore.QSize(self.geo.width()/2.3, self.geo.height()/3))

        
        self.plugin_deletion_warning_widget = QtWidgets.QWidget(PluginDeletionWarning)
        self.plugin_deletion_warning_widget.setObjectName("plugin_deletion_warning_widget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.plugin_deletion_warning_widget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.project_deletion_warning_groupbox = QtWidgets.QGroupBox(self.plugin_deletion_warning_widget)
        self.project_deletion_warning_groupbox.setTitle("")
        self.project_deletion_warning_groupbox.setObjectName("project_deletion_warning_groupbox")
        self.gridLayout = QtWidgets.QGridLayout(self.project_deletion_warning_groupbox)
        self.gridLayout.setObjectName("gridLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 2, 1, 1)
        self.ok_pushbutton = QtWidgets.QPushButton(self.project_deletion_warning_groupbox)
        self.ok_pushbutton.setObjectName("ok_pushbutton")
        self.gridLayout.addWidget(self.ok_pushbutton, 4, 2, 1, 1)
        self.label = QtWidgets.QLabel(self.project_deletion_warning_groupbox)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 0, 0, 1, 1)
        self.cancel_pushbutton = QtWidgets.QPushButton(self.project_deletion_warning_groupbox)
        self.cancel_pushbutton.setObjectName("cancel_pushbutton")
        self.gridLayout.addWidget(self.cancel_pushbutton, 4, 0, 1, 1)
        self.gridLayout_2.addWidget(self.project_deletion_warning_groupbox, 0, 0, 1, 1)
        PluginDeletionWarning.setCentralWidget(self.plugin_deletion_warning_widget)

        self.retranslateUi(PluginDeletionWarning)
        QtCore.QMetaObject.connectSlotsByName(PluginDeletionWarning)

        

    def retranslateUi(self, PluginDeletionWarning):
        _translate = QtCore.QCoreApplication.translate
        PluginDeletionWarning.setWindowTitle(_translate("PluginDeletionWarning", "MainWindow"))
        self.ok_pushbutton.setText(_translate("PluginDeletionWarning", "Ok"))
        self.label.setText(_translate("PluginDeletionWarning", "Are you sure that you want to permanently delete this plugin? "))
        self.cancel_pushbutton.setText(_translate("PluginDeletionWarning", "Cancel"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    PluginDeletionWarning = QtWidgets.QMainWindow()
    ui = Ui_PluginDeletionWarning()
    ui.setupUi(PluginDeletionWarning)
    PluginDeletionWarning.show()
    sys.exit(app.exec_())
