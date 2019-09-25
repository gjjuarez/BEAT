from PyQt5 import QtCore, QtGui, QtWidgets
import UiView
class UiMain(UiView.Ui_BEAT):
	def setupIU(BEAT):
		super().setupIU(BEAT)
		self.new_project_button.clicked.connect(self.new_project)

        self.deleat_project_button.clicked.connect(self.remove_project)
        self.File_Browse_Btn.clicked.connect(self.browse_path)
        #save project
        self.pushButton_11.clicked.connect(self.save_project)

        #delete plugin
        self.pushButton_19.clicked.connect(self.remove_plugin)
        # add
        self.pushButton_20.clicked.connect(self.save_plugin)
        #plugin Browse
        self.pushButton_17.clicked.connect(self.browse_plugin_structure)
        self.pushButton_18.clicked.connect(self.browse_plugin_dataset)

        '''
        A O C Button calls
        '''
        self.pushButton_2.clicked.connect(self.analysisResult)
        self.pushButton_7.clicked.connect(self.commentView)
        self.pushButton_4.clicked.connect(self.outputField)
        self.pushButton_21.clicked.connect(self.enableDynamicAnalysis)

        
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def new_project(self):
        self.groupBox_4.show()
        self.label.show()

    def remove_project(self):
        listItems=self.Project_List.selectedItems()
        if not listItems: return        
        for item in listItems:
           self.Project_List.takeItem(self.Project_List.row(item))
    def save_project(self):
        temp = "                     " + self.Project_Name_Text.text()
        self.Project_List.addItem(temp)

    def save_plugin(self):
        self.listWidget_4.addItem(self.lineEdit_18.text())

    def browse_path(self):
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName()
        self.File_Path_Text.setText(file_path)

    def enableDynamicAnalysis(self):
        ui.pushButton_22.setDisabled(False)
        ui.pushButton_23.setDisabled(False)


    def remove_plugin(self):
        listItems=self.listWidget_4.selectedItems()
        if not listItems: return        
        for item in listItems:
           self.listWidget_4.takeItem(self.listWidget_4.row(item))
    def browse_plugin_structure(self):
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName()
        self.lineEdit_16.setText(file_path)
    def browse_plugin_dataset(self):
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName()
        self.lineEdit_17.setText(file_path)

    def analysisResult(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_Figure_12_Analysis_Result_Review()
        self.ui.setupUi(self.window)
        self.window.show()

    def outputField(self): 
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_Figure_10_Output_Field_View()
        self.ui.setupUi(self.window) 
        self.window.show()

    def commentView(self): 
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_Figure_11_Comment_View()
        self.ui.setupUi(self.window)
        self.window.show()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    BEAT = QtWidgets.QGroupBox()
    ui = UiMain()
    ui.points_of_interest_groupBox.hide()
    ui.plugin_management_groupBox.hide()
    ui.analysis_groupBox.hide()
    ui.documentation_groupBox.hide()
    ui.groupBox_4.hide()
    ui.label.hide()
    ui.pushButton_22.setDisabled(True)
    ui.pushButton_23.setDisabled(True)
    ui.setupUi(BEAT)
    BEAT.show()
    sys.exit(app.exec_())