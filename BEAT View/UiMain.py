from PyQt5 import QtCore

import UiView
from PyQt5 import QtWidgets

from Figure10OutputFieldView import Ui_Figure10OutputFieldView
from Figure11CommentView import Ui_Figure11CommentView
from Figure12AnalysisResultReview import Ui_Figure12AnalysisResultReview
from PyQt5.QtWidgets import QListWidgetItem

from radare2_scripts import radare_commands_interface
from PyQt5 import QtGui

class UiMain(UiView.Ui_BEAT):
    global staticIsRun
    staticIsRun = False

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
        '''
        Analysis Run Tab Listeners
        '''
        # run static analysis and check which POI to display
        self.static_run_button.clicked.connect(self.analyze_and_display_POI)
        # searches POI in the left column
        self.points_of_interest_search_button.clicked.connect(self.search_POI)
        self.points_of_interest_line_edit.returnPressed.connect(self.search_POI)
        # listens to changes in POI dropdown
        self.type_dropdown.currentIndexChanged.connect(self.change_displayed_POI)
        # sets breakpoints on currently checked items
        self.points_of_interest_list_widget.itemChanged.connect(self.set_breakpoint)
        # runs dynamic analysis on breakpoints
        self.dynamic_run_button.clicked.connect(radare_commands_interface.run_dynamic_and_update)

        QtCore.QMetaObject.connectSlotsByName(BEAT)

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

    '''
    Runs analysis and displayss results
    '''
    def analyze_and_display_POI(self):
        self.detailed_points_of_interest_listWidget.clear()
        self.points_of_interest_list_widget.clear()
        radare_commands_interface.run_static_analysis()
        radare_commands_interface.extract_all()
        global staticIsRun
        staticIsRun = True
        # Check What box is check
        # Switch Cases to see what method is called
        display_value = str(self.type_dropdown.currentText())
        self.display_POI(display_value)

    def change_displayed_POI(self):
        global staticIsRun
        if not staticIsRun:
            return
        self.detailed_points_of_interest_listWidget.clear()
        self.points_of_interest_list_widget.clear()
        display_value = str(self.type_dropdown.currentText())
        self.display_POI(display_value)

    def display_POI(self, display_value):
        if display_value == "Imports":
            self.read_and_display_all_imports()
        elif display_value == "Strings":
            self.read_and_display_all_strings()
        elif display_value == "Function Call":
            self.read_and_display_all_functions()
        elif display_value == "Variables":
            self.read_and_display_all_variables()
        elif display_value == "All":
            self.read_and_display_all_functions()
            self.read_and_display_all_variables()
            self.read_and_display_all_imports()
            self.read_and_display_all_strings()

    def set_breakpoint(self, item):
        print("Setting breakpoint")
        if item.checkState() == 2:  # if item is checked
            radare_commands_interface.set_breakpoint_at_function(item.text())
        else:  # item is unchecked
            radare_commands_interface.remove_breakpoint_at_function(item.text())

    '''
    Runs analysis and displays results
    '''

    '''
    Opens imports text file and displays it on detailed POI view
    '''
    def read_and_display_all_imports(self):
        imports = open("imports.txt", "r")
        for line in imports.read().split("\n"):
            item = QListWidgetItem(line)
            self.detailed_points_of_interest_listWidget.addItem(item)
        imports.close()
        self.display_imports_in_left_column()

    def display_imports_in_left_column(self):
        imports = open("imports.txt", "r")

        # Start at the index 2 to the end get each line
        for line in imports.read().split("\n")[2:-1]:
            # Separate by spaces and then get the last word
            line = line.split(" ")[-1]
            item = QListWidgetItem(line)
            self.points_of_interest_list_widget.addItem(item)
        imports.close()

    def read_and_display_all_functions(self):
        functions = open("functions.txt", "r")
        for line in functions.read().split("\n"):
            item = QListWidgetItem(line)
            self.detailed_points_of_interest_listWidget.addItem(item)
        functions.close()
        self.display_functions_in_left_column()

    def display_functions_in_left_column(self):
        functions = open("functions.txt", "r")
        breakPoints = radare_commands_interface.get_all_breakpoints()

        # Start at the index 2 to the end get each line
        for line in functions.read().split("\n")[:-1]:
            # Separate by spaces and then get the last word
            line = line.split(" ")[-1]
            item = QListWidgetItem(line)

            # Don't know if we need this following line
            # item.setFlags(item.flags()|QtCore.Qt.ItemIsUserCheckable)
            if line in breakPoints:
                item.setCheckState(QtCore.Qt.Checked)
            else:
                item.setCheckState(QtCore.Qt.Unchecked)
            self.points_of_interest_list_widget.addItem(item)
        functions.close()

    def read_and_display_all_strings(self):
        strings = open("strings.txt", "r")
        for line in strings.read().split("\n"):
            item = QListWidgetItem(line)
            self.detailed_points_of_interest_listWidget.addItem(item)
        strings.close()
        self.display_strings_in_left_column()

    def display_strings_in_left_column(self):
        strings = open("strings.txt", "r")

        # Start at the index 2 to the end get each line
        for line in strings.read().split("\n")[2:-1]:
            # Separate by spaces and then get the last word
            line = line.split(" ", 9)[-1]
            item = QListWidgetItem(line)

            # Don't know if we need this following line
            # item.setFlags(item.flags()|QtCore.Qt.ItemIsUserCheckable)

            # item.setCheckState(QtCore.Qt.Unchecked)
            self.points_of_interest_list_widget.addItem(item)
        strings.close()

    def read_and_display_all_variables(self):
        variables = open("variables.txt", "r")
        for line in variables.read().split("\n"):
            item = QListWidgetItem(line)
            self.detailed_points_of_interest_listWidget.addItem(item)
        variables.close()
        # No method for this yet
        self.display_variables_in_left_column()

    def display_variables_in_left_column(self):
        variables = open("variables.txt", "r")
        variables.readline()  # skip the title for variables

        # Start at the index 2 to the end get each line
        for line in variables.read().split("\n")[:-1]:
            # Separate by spaces and then get the last word
            #line = line.split(" ", 1)[-1]
            line = line.split(" ")[1]
            item = QListWidgetItem(line)

            # Don't know if we need this following line
            #item.setFlags(item.flags()|QtCore.Qt.ItemIsUserCheckable)

            # item.setCheckState(QtCore.Qt.Unchecked)
            self.points_of_interest_list_widget.addItem(item)
        variables.close()

    def search_POI(self):
        # clear background in left column
        for i in range(self.points_of_interest_list_widget.count()):
            self.points_of_interest_list_widget.item(i).setBackground(QtGui.QBrush(QtCore.Qt.color0))
        # clear background for detailed view
        for i in range(self.detailed_points_of_interest_listWidget.count()):
            self.detailed_points_of_interest_listWidget.item(i).setBackground(QtGui.QBrush(QtCore.Qt.color0))

        display_value = str(self.points_of_interest_line_edit.text())
        # don't search if empty string
        if display_value == "":
            return
        # highlights search in left column
        search_result = self.points_of_interest_list_widget.findItems(display_value, QtCore.Qt.MatchContains)
        if len(search_result) > 0:
            for item in search_result:
                item.setBackground(QtGui.QBrush(QtCore.Qt.magenta))
        # highlights search in detailed view
        search_result = self.detailed_points_of_interest_listWidget.findItems(display_value, QtCore.Qt.MatchContains)
        if len(search_result) > 0:
            for item in search_result:
                item.setBackground(QtGui.QBrush(QtCore.Qt.magenta))

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

