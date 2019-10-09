from PyQt5 import QtCore, QtGui, QtWidgets

import UiView


from Figure10OutputFieldView import Ui_Figure10OutputFieldView
from Figure11CommentView import Ui_Figure11CommentView
from Figure12AnalysisResultReview import Ui_Figure12AnalysisResultReview

class UiMain(UiView.Ui_BEAT):
    def setupUi(self, BEAT):
        super().setupUi(BEAT)
        print("hi")
        self.dynamic_run_button.setDisabled(True)
        self.dynamic_stop_button.setDisabled(True)

        #QtCore.QMetaObject.connectSlotsByName(MainWindow)

        #########################################################################################
        # Project Tab Functions
        #########################################################################################
        '''
        Project Tab Listeners
        '''
        #calls new_project if new_project_button is clicked
        self.new_project_button.clicked.connect(self.new_project)
        #calls remove_project if delete_project_button is clicked
        self.delete_project_button.clicked.connect(self.remove_project)
        #calls save_project if save_project_button is clicked 
        self.save_project_button.clicked.connect(self.save_project)
        #calls browse_path if file_browse_button is clicked
        self.file_browse_button.clicked.connect(self.browse_path)
        
        '''
        Analysis Tab Listeners 
        '''
        #calls enable_dynamic_analysis after static_run_button is clicked
        self.static_run_button.clicked.connect(self.enable_dynamic_analysis)
        #calls analysis_result aft er analysis_result_button is clicked
        self.analysis_result_button.clicked.connect(self.analysis_result)
        #calls comment_view after comment_button is clicked
        self.comment_button.clicked.connect(self.comment_view)
        #calls output_field after output_field_button is clicked
        self.output_field_button.clicked.connect(self.output_field)

        '''
        Plugin Management Tab Listeners
        '''
        #calls save_plugin if detailed_plugin_view_save_button is clicked
        self.detailed_plugin_view_save_button.clicked.connect(self.save_plugin)
        #calls remove_plugin  if detailed_plugin_view_delete_button is clicked
        self.detailed_plugin_view_delete_button.clicked.connect(self.remove_plugin)
        #calls browse_plugin_structure if plugin_structure_browse_button is clicked
        self.plugin_structure_browse_button.clicked.connect(self.browse_plugin_structure)
        #calls browse_plugin_dataset if plugin_predefined_data_set_browse_button is clicked
        self.plugin_predefined_data_set_browse_button.clicked.connect(self.browse_plugin_dataset)

        '''
        Points of Interest Tab Listeners
        '''

        '''
        Documentation Tab Listeners
        '''

        QtCore.QMetaObject.connectSlotsByName(BEAT)
        #self.tabWidget.addTab(EmbTerminal(), "EmbTerminal")

        self.detailed_point_of_interest_view_type_dropdown.addItem("a;l", "hi")

    #########################################################################################
    # Project Tab Functions
    #########################################################################################

    '''
    Shows the Detailed Project View after the New button is clicked in Project
    '''
    def new_project(self):
        self.detailed_project_view_groupbox.show()
        self.label.show()
    '''
    Removes a project after it has been selected and the Delete button is clicked in Project
    '''
    def remove_project(self):
        listItems = self.project_list.selectedItems()
        if not listItems: return        
        for item in listItems:
           self.project_list.takeItem(self.project_list.row(item))
    '''
    Adds a project name to the projdynamic_runect list within Project
    '''
    def save_project(self):
        temp = self.project_name_text.text()
        self.project_list.addItem(temp)
    '''
    Opens the file browser and writes the selected file's filepath in file_path_lineedit 
    '''
    def browse_path(self):
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName()
        self.file_path_lineedit.setText(file_path)

    #########################################################################################
    # Analysis Tab Functions
    #########################################################################################
    '''
    Enables Run and Stop buttons for dynamic analysis
    '''
    def enable_dynamic_analysis(self):
        ui.dynamic_run_button.setDisabled(False)
        ui.dynamic_stop_button.setDisabled(False)
    '''
    Opens Figure12AnalysisResultReview
    '''
    def analysis_result(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_Figure12AnalysisResultReview()
        self.ui.setupUi(self.window)
        self.window.show()
    '''
    Opens Ui_Figure10OutputFieldView
    '''
    def output_field(self): 
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_Figure10OutputFieldView()
        self.ui.setupUi(self.window) 
        self.window.show()
    '''
    Opens Ui_Figure11CommentView
    '''
    def comment_view(self): 
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_Figure11CommentView()
        self.ui.setupUi(self.window)
        self.window.show()

    #########################################################################################
    # Plugin Management Tab Functions
    #########################################################################################

    '''
    Adds a plugin name to the plugin list in Plugin Management 
    '''
    def save_plugin(self):
        self.plugin_view_plugin_listwidget.addItem(self.plugin_name_lineedit.text())
    '''
    Removes a selected plugin from the plugin list within Plugin Management 
    '''
    def remove_plugin(self):
        listItems = self.plugin_view_plugin_listwidget.selectedItems()
        if not listItems: return        
        for item in listItems:
           self.plugin_view_plugin_listwidget.takeItem(self.plugin_view_plugin_listwidget.row(item))
    '''
    Opens the file browser and writes the selected file's filepath in plugin_structure_filepath_lineedit 
    '''
    def browse_plugin_structure(self):
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName()
        self.plugin_structure_filepath_lineedit.setText(file_path)
    '''
    Opens the file browser and writes the selected file's filepath in plugin_predefined_data_set_lineedit 
    '''
    def browse_plugin_dataset(self):
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName()
        self.plugin_predefined_data_set_lineedit.setText(file_path)

  

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    BEAT = QtWidgets.QGroupBox()
    ui = UiMain()

    ui.setupUi(BEAT)
    BEAT.show()
    sys.exit(app.exec_())
