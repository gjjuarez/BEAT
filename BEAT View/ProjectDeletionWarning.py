# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ProjectDeletionWarning.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ProjectDeletionWarning(object):
    def setupUi(self, ProjectDeletionWarning):
        ProjectDeletionWarning.setObjectName("ProjectDeletionWarning")
        
        ###########################
        # Resizing according to user's desktop
        ###########################
        self.geo = QtWidgets.QDesktopWidget().screenGeometry()
        ProjectDeletionWarning.resize(self.geo.width()/2.3, self.geo.height()/3)
        ProjectDeletionWarning.setMaximumSize(QtCore.QSize(self.geo.width()/2.3, self.geo.height()/3))

        self.project_deletion_warning_widget = QtWidgets.QWidget(ProjectDeletionWarning)
        self.project_deletion_warning_widget.setObjectName("project_deletion_warning_widget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.project_deletion_warning_widget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.project_deletion_warning_groupbox = QtWidgets.QGroupBox(self.project_deletion_warning_widget)
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
        ProjectDeletionWarning.setCentralWidget(self.project_deletion_warning_widget)

        self.retranslateUi(ProjectDeletionWarning)
        QtCore.QMetaObject.connectSlotsByName(ProjectDeletionWarning)

    def retranslateUi(self, ProjectDeletionWarning):
        _translate = QtCore.QCoreApplication.translate
        ProjectDeletionWarning.setWindowTitle(_translate("ProjectDeletionWarning", "MainWindow"))
        self.ok_pushbutton.setText(_translate("ProjectDeletionWarning", "Ok"))
        self.label.setText(_translate("ProjectDeletionWarning", "Are you sure that you want to permanently delete this project? "))
        self.cancel_pushbutton.setText(_translate("ProjectDeletionWarning", "Cancel"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ProjectDeletionWarning = QtWidgets.QMainWindow()
    ui = Ui_ProjectDeletionWarning()
    ui.setupUi(ProjectDeletionWarning)
    ProjectDeletionWarning.show()
    sys.exit(app.exec_())
