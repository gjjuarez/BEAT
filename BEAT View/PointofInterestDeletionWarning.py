# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PointofInterestDeletionWarning.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_PointofInterestDeletionWarning(object):
    def setupUi(self, PointofInterestDeletionWarning):
        PointofInterestDeletionWarning.setObjectName("PointofInterestDeletionWarning")
        
        ###########################
        # Resizing according to user's desktop
        ###########################
        self.geo = QtWidgets.QDesktopWidget().screenGeometry()
        PointofInterestDeletionWarning.resize(self.geo.width()/2.3, self.geo.height()/3)
        PointofInterestDeletionWarning.setMaximumSize(QtCore.QSize(self.geo.width()/2.3, self.geo.height()/3))

        self.widget = QtWidgets.QWidget(PointofInterestDeletionWarning)
        self.widget.setObjectName("widget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.widget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.poi_deletion_warning_groupbox = QtWidgets.QGroupBox(self.widget)
        self.poi_deletion_warning_groupbox.setTitle("")
        self.poi_deletion_warning_groupbox.setObjectName("poi_deletion_warning_groupbox")
        self.gridLayout = QtWidgets.QGridLayout(self.poi_deletion_warning_groupbox)
        self.gridLayout.setObjectName("gridLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 2, 1, 1)
        self.ok_pushbutton = QtWidgets.QPushButton(self.poi_deletion_warning_groupbox)
        self.ok_pushbutton.setObjectName("ok_pushbutton")
        self.gridLayout.addWidget(self.ok_pushbutton, 4, 2, 1, 1)
        self.label = QtWidgets.QLabel(self.poi_deletion_warning_groupbox)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 0, 0, 1, 1)
        self.cancel_pushbutton = QtWidgets.QPushButton(self.poi_deletion_warning_groupbox)
        self.cancel_pushbutton.setObjectName("cancel_pushbutton")
        self.gridLayout.addWidget(self.cancel_pushbutton, 4, 0, 1, 1)
        self.gridLayout_2.addWidget(self.poi_deletion_warning_groupbox, 0, 0, 1, 1)
        PointofInterestDeletionWarning.setCentralWidget(self.widget)

        self.retranslateUi(PointofInterestDeletionWarning)
        QtCore.QMetaObject.connectSlotsByName(PointofInterestDeletionWarning)

    def retranslateUi(self, PointofInterestDeletionWarning):
        _translate = QtCore.QCoreApplication.translate
        PointofInterestDeletionWarning.setWindowTitle(_translate("PointofInterestDeletionWarning", "MainWindow"))
        self.ok_pushbutton.setText(_translate("PointofInterestDeletionWarning", "Ok"))
        self.label.setText(_translate("PointofInterestDeletionWarning", "Are you sure that you want to permanently delete this point of interest? "))
        self.cancel_pushbutton.setText(_translate("PointofInterestDeletionWarning", "Cancel"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    PointofInterestDeletionWarning = QtWidgets.QMainWindow()
    ui = Ui_PointofInterestDeletionWarning()
    ui.setupUi(PointofInterestDeletionWarning)
    PointofInterestDeletionWarning.show()
    sys.exit(app.exec_())
