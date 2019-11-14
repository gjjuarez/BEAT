from PyQt5 import QtCore

import UiView
from PyQt5 import QtWidgets

from Figure10OutputFieldView import Ui_Figure10OutputFieldView
from Figure11CommentView import Ui_Figure11CommentView
from Figure12AnalysisResultReview import Ui_Figure12AnalysisResultReview
from ProjectDeletionWarning import Ui_ProjectDeletionWarning
from PointofInterestDeletionWarning import Ui_PointofInterestDeletionWarning
from PluginDeletionWarning import Ui_PluginDeletionWarning
from ArchitectureError import Ui_ArchitectureError
from PyQt5.QtWidgets import QListWidgetItem
from Terminal import EmbTerminalLinux

from radare2_scripts import radare_commands_interface
from PyQt5 import QtGui
import data_manager
import os.path
from os import path

class UiMain(UiView.Ui_BEAT):
    global staticIsRun
    staticIsRun = False

    valid_extensions = ["exe", "dll"]

    def setupUi(self, BEAT):
        super().setupUi(BEAT)

        # User cannot run dynamic in the beginning of the program
        self.dynamic_run_button.setDisabled(True)
        self.dynamic_stop_button.setDisabled(True)

        # Fill the Project list from mongo
        self.fill_projects()

        self.update_plugin_list()

        self.terminal = EmbTerminalLinux(self.detailed_point_of_interest_view_groupbox)
        self.terminal.setGeometry(QtCore.QRect(15, 310, 561, 90))
        self.terminal.setObjectName("Terminal")

        self.stacked = QtWidgets.QStackedWidget()
        self.stacked.addWidget(self.terminal)

        self.setCurrentProject()

        #########################################################################################
        # Project Tab Listeners
        #########################################################################################
        '''
        Project Tab Listeners
        '''
        # calls new_project if new_project_bsutton is clicked
        self.new_project_button.clicked.connect(self.new_project)
        # calls project_deletion_warning if delete_project_button is clicked
        self.delete_project_button.clicked.connect(self.project_deletion_warning)
        # calls save_project if save_project_button is clicked
        self.save_project_button.clicked.connect(self.save_project)
        # calls browse_path if file_browse_button is clicked
        self.file_browse_button.clicked.connect(self.browse_path)
        # self.delete_project_button.connect(self.delete_current_project)

        '''
        Analysis Tab Listeners 
        '''
        # calls enable_dynamic_analysis after static_run_button is clicked
        self.static_run_button.clicked.connect(self.enable_dynamic_analysis)
        # calls analysis_result aft er analysis_result_button is clicked
        self.analysis_result_button.clicked.connect(self.analysis_result)
        # calls comment_view after comment_button is clicked
        self.comment_button.clicked.connect(self.comment_view)
        # calls output_field after output_field_button is clicked
        self.output_field_button.clicked.connect(self.output_field)

        '''
        Plugin Management Tab Listeners
        '''
        # calls save_plugin if detailed_plugin_view_save_button is clicked
        self.detailed_plugin_view_save_button.clicked.connect(self.save_plugin)
        # calls remove_plugin  if detailed_plugin_view_delete_button is clicked
        self.detailed_plugin_view_delete_button.clicked.connect(self.remove_plugin)
        # calls browse_plugin_structure if plugin_structure_browse_button is clicked
        self.plugin_structure_browse_button.clicked.connect(self.browse_plugin_structure)
        # calls browse_plugin_dataset if plugin_predefined_data_set_browse_button is clicked
        self.plugin_predefined_data_set_browse_button.clicked.connect(self.browse_plugin_dataset)

        '''
        Points of Interest Tab Listeners
        '''
        self.detailed_point_of_interest_view_save_button.clicked.connect(self.add_poi_to_plugin)

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
        self.points_of_interest_list_widget.itemChanged.connect(self.remove_breakpoints)
        # runs dynamic analysis on breakpoints then updates ui
        self.dynamic_run_button.clicked.connect(self.set_auto_breakpoint)
        self.dynamic_run_button.clicked.connect(self.run_dynamic_then_display)
        # match detailed view with left column when selected
        self.points_of_interest_list_widget.itemClicked.connect(self.match_selected_POI)

        QtCore.QMetaObject.connectSlotsByName(BEAT)
        self.detailed_point_of_interest_view_type_dropdown.clear()
        self.detailed_point_of_interest_view_type_dropdown.addItems(["Function","String", "Variable", "DLL", "Packet Protocol", "Struct"])
        self.project_list.itemClicked.connect(self.project_selected)

    #########################################################################################
    # Project Tab Functions
    #########################################################################################
    def project_selected(self):
        to_find = self.project_list.currentItem().text()
        name, desc, path, bin_info = data_manager.get_project_from_name(to_find)
        data_manager.update_current_project(name, desc, path, bin_info)
        self.setCurrentProject()

    def setCurrentProject(self):
        name, desc, path, bin_info = data_manager.getCurrentProjectInfo()
        data_manager.initialize_POI_collections(name)

        # If no project set...
        if name == "":
            BEAT.setWindowTitle("BEAT")
        else:
            BEAT.setWindowTitle("BEAT - [PROJECT]: " + name + "    [BINARY]: " + path.split("/")[-1])
        # fill name text
        self.project_name_text.setText(name)
        self.project_name_text.setReadOnly(True)
        # fill description test
        self.project_desc_text.setText(desc)
        self.project_desc_text.setReadOnly(True)
        # fill path text
        self.file_path_lineedit.setText(path)
        self.file_path_lineedit.setReadOnly(True)
        # disable buttons
        self.save_project_button.setDisabled(True)
        self.file_browse_button.setDisabled(True)
        # fill binary info
        self.fill_binary_info(bin_info)

    '''
    Sets settings for new project viewer
    '''

    def new_project(self):
        # self.detailed_project_view_groupbox.show()
        # self.label.show()

        self.project_name_text.setText("")
        self.project_name_text.setReadOnly(False)

        self.project_desc_text.setText("")
        self.project_desc_text.setReadOnly(False)

        self.file_path_lineedit.setText("")
        self.file_path_lineedit.setReadOnly(False)

        self.save_project_button.setDisabled(False)
        self.file_browse_button.setDisabled(False)

    '''
    Removes a project after it has been selected and the Delete button is clicked in Project
    '''

    '''
    Opens Figure12AnalysisResultReview
    
    def analysis_result(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_Figure12AnalysisResultReview()
        self.ui.setupUi(self.window)
        self.window.show()
    '''

    def project_deletion_warning(self): 
        print("Entered method")
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_ProjectDeletionWarning()
        self.ui.setupUi(self.window)
        self.widow.show() 
        self.ui.ok_pushbutton.connect(remove_project)
        self.ui.cancel_pushbutton.connect(self.close)

    def remove_project(self):
        name = self.project_list.currentItem().text()
        data_manager.delete_project_given_name(name)
        self.project_list.clear()
        self.fill_projects()
        print("Done Removing Project:", name)
        self.new_project()

    '''
    Fills projects list
    '''
    def fill_projects(self):
        self.project_list.clear()
        self.project_list.addItems(data_manager.get_project_names())

    '''
    Adds a project name to the projdynamic_runect list within Project
    '''

    def save_project(self):
        name = self.project_name_text.text()
        desc = self.project_desc_text.text()
        path = self.file_path_lineedit.text()
        bin_info = self.check_binary_arch(path)
        # check if the binary is correct architecture before saving
        if bin_info == None:  # display error window
            self.window = QtWidgets.QMainWindow()
            self.ui = Ui_ArchitectureError()
            self.ui.setupUi(self.window)
            self.window.show()
        else:
            data_manager.save_project(name, desc, path, bin_info)
            data_manager.update_current_project(name, desc, path, bin_info)
            self.fill_projects()
            self.setCurrentProject()

    def check_binary_arch(self, path):
        binary_info = radare_commands_interface.parse_binary(path)
        if 'arch' in binary_info and binary_info['arch'] == 'x86':
            self.file_path_lineedit.setText(path)
            self.fill_binary_info(binary_info)
            return binary_info
        else:
            return None

    '''
    Opens the file browser and writes the selected file's filepath in file_path_lineedit 
    '''

    def browse_path(self):
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName()
        self.file_path_lineedit.setText(file_path)

    def fill_binary_info(self, bi):
        self.binary_file_properties_value_listwidget.clear()
        try:
            self.binary_file_properties_value_listwidget.addItems([bi['os'], bi['bintype'],
                                                                   bi['machine'], bi['class'],
                                                                   bi['bits'], bi['lang'],
                                                                   bi['canary'], bi['crypto'],
                                                                   bi['nx'], bi['pic'],
                                                                   bi['relocs'], bi['relro'],
                                                                   bi['stripped']])
        except KeyError:
            print("Failed to add binary info")
            return
        print("Done filling binary info")

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
    Opens Ui_Figure11CommentView and will show comments for selected POI 
    if the comment exists
    '''
    def comment_view(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_Figure11CommentView()
        self.ui.setupUi(self.window)
        self.window.show()

        current_item = self.points_of_interest_list_widget.currentItem()
        current_item_name = current_item.text() + ".txt"
        comment = open(current_item_name, "r+")

        looking_for_comment = self.points_of_interest_list_widget.currentRow()
        for line in comment:
            comment_number = line.split(" ", 1)[0]
            if comment_number == str(looking_for_comment):
                print("something there")
                self.ui.comment_textedit.setText(line)
        comment.close()
        self.ui.save_button.clicked.connect(self.save_comment(comment))
        self.ui.clear_button.clicked.connect(self.clear_comment)

        # This looks for if comments already exits for a line
        '''
        if path.exists("comment.txt"):
            comment = open("comment.txt", "r+")
            looking_for_comment = self.points_of_interest_list_widget.currentRow()
            for line in comment:
                comment_number = line.split(" ", 1)[0]
                if comment_number == str(looking_for_comment):
                    print("something there")
                    self.ui.comment_textedit.setText(line)
        comment.close()
        self.ui.save_button.clicked.connect(self.save_comment)
        self.ui.clear_button.clicked.connect(self.clear_comment)
        '''

    '''
    Saves comments to text file
    '''
    def save_comment(self, comment):
        comment = open(comment, "a+")
        text = self.ui.comment_textedit.toPlainText()
        comment.write("%d " % self.points_of_interest_list_widget.currentRow())
        comment.write(text + "\n")
        print(text)
        comment.close()

    '''
    Works with save_comment to overwrite a comment that has already been placed 
    on a POI  AND DOESNT WORK
    '''
    def replace_line(self, file_name, line_num, text):
        if not text:
            '''Do nothing'''
            print("Do nothing")
        else:
            print("SHOULD REPLACE HERE")
            '''lines = open(file_name, 'r').readlines()
            lines[line_num] = text
            out = open(file_name, 'w')
            out.writelines(lines)
            out.close()'''

    '''
    Clears a comment from the POI
    '''
    def clear_comment(self):
        with open("comment.txt", "r+") as f:
            new_f = f.readlines()
            f.seek(0)
            for line in new_f:
                if self.ui.comment_textedit.toPlainText() not in line:
                    f.write(line)
            f.truncate()
        self.ui.comment_textedit.clear()
    '''
    Runs analysis and displayss results
    '''
    def analyze_and_display_POI(self):
        self.detailed_points_of_interest_listWidget.clear()
        self.points_of_interest_list_widget.clear()
        radare_commands_interface.run_static_analysis()
        # self.terminal.begin()
        # self.stacked.setCurrentWidget(self.terminal)
        # self.terminal.begin_static()
        global staticIsRun
        staticIsRun = True
        # Check What box is check  
        # Switch Cases to see what method is called
        display_value = str(self.type_dropdown.currentText())
        self.display_POI(display_value)

    def match_selected_POI(self):
        row = self.points_of_interest_list_widget.currentRow()
        currentItem = self.points_of_interest_list_widget.currentItem()
        if not currentItem:
            return
        if currentItem.isSelected():
            self.detailed_points_of_interest_listWidget.itemAt(0, row).setSelected(True)
            self.detailed_points_of_interest_listWidget.setCurrentRow(row)

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
            # variables displayed with functions instead
            # self.read_and_display_all_variables()
            # self.read_and_display_all_imports()
            self.read_and_display_all_strings()

    # This function got deprecated.
    # def set_breakpoint(self, item):
    #     print("Setting breakpoint")
    #     if item.checkState() == 2:  # if item is checked
    #         radare_commands_interface.set_breakpoint_at_function(item.text())
    #     else:  # item is unchecked
    #         radare_commands_interface.remove_breakpoint_at_function(item.text())

    def set_auto_breakpoint(self):
        print("Setting breakpoints")
        for i in range(self.points_of_interest_list_widget.count()):
            radare_commands_interface.set_breakpoint_at_function(self.points_of_interest_list_widget.item(i).text())

    def remove_breakpoints(self, item):
        if item.checkState() == 2:  # if item is checked
            radare_commands_interface.remove_breakpoint_at_function(item.text())
        elif item.checkState() == 0:
            radare_commands_interface.set_breakpoint_at_function(item.text())

    def run_dynamic_then_display(self):
        # radare_commands_interface.run_dynamic_and_update()
        self.dynamic_run_button.setDisabled(True)
        self.dynamic_stop_button.setDisabled(False)
        print("Running dynamic analysis!")
        
        # self.terminal.kill_process()
        # self.terminal = EmbTerminalLinux(self.detailed_point_of_interest_view_groupbox)
        # self.terminal.setGeometry(QtCore.QRect(15, 310, 561, 90))
        # self.terminal.setObjectName("Terminal")
        # self.terminal.begin_dynamic()
        print("Done with dynamic analysis!")
        self.change_displayed_POI()  # updates ui
        self.dynamic_run_button.setDisabled(False)
        self.dynamic_stop_button.setDisabled(True)

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
        # functions = open("functions.txt", "r")
        functions = data_manager.get_functions()

        for func in functions:
            # item = QListWidgetItem("Function name: " + func['Function Name'])
            paramTypes = ""
            try:
                for pt in func["Parameter Type"]:
                    paramTypes = paramTypes + pt
            except TypeError:
                paramTypes = "n/a"

            paramOrder = ""
            try:
                for pt in func["Parameter Type"]:
                    paramOrder = paramOrder + pt
            except TypeError:
                paramOrder = "n/a"

            returnVal = "n/a"
            if func['Return Value']:
                returnVal = func['Return Value']

            returnType = "n/a"
            if func['Return Type']:
                returnVal = func['Return Type']

            item = QListWidgetItem("Function name: " + func['Function Name'] + "\n"
                                   + '\tReturn Type: ' + returnType + "\n"
                                   + '\tReturn Value: ' + returnVal + "\n"
                                   + '\tBinary Section: ' + func['Binary Section'] + "\n"
                                   + '\tParameter Order: ' + paramOrder)
            # + '\tParameter Type' + paramTypes)
            self.detailed_points_of_interest_listWidget.addItem(item)
            # display all variables related to current function
            # varIndex = self.read_and_display_variables_with_functions(varIndex)
            self.read_and_display_variables_with_functions(func["Function Name"])
        # functions.close()
        self.display_functions_in_left_column()

    def read_and_display_variables_with_functions(self, func_name):
        # display all variables related to current function
        variables = data_manager.get_variables()
        for var in variables:
            if func_name == var["Function Name"]:
                varItem = QListWidgetItem("\tVariable Name: " + var["Variable Name"] + "\n"
                                          "\t\tVariable Type: " + var["Variable Type"] + "\n"
                                          "\t\tVariabel Value: " + var["Variable Value"] + "\n"
                                          "\t\tAddress: " + var["Address"])
                self.detailed_points_of_interest_listWidget.addItem(varItem)

    def read_and_display_variables_with_functions_left_column(self, func_name):
        variables = data_manager.get_variables()
        # display all variables related to current function
        for var in variables:
            if func_name == var["Function Name"]:
                varItem = QListWidgetItem("   " + var["Variable Name"])
                self.points_of_interest_list_widget.addItem(varItem)

    def display_functions_in_left_column(self):
        # breakPoints = radare_commands_interface.get_all_breakpoints()
        functions = data_manager.get_functions()
        for func in functions:
            item = QListWidgetItem(func["Function Name"])

            # Don't know if we need this following line
            # item.setFlags(item.flags()|QtCore.Qt.ItemIsUserCheckable)
            item.setCheckState(QtCore.Qt.Unchecked)
            self.points_of_interest_list_widget.addItem(item)

            # display all variables related to current function
            self.read_and_display_variables_with_functions_left_column(func["Function Name"])

    def read_and_display_all_strings(self):
        strings = data_manager.get_strings()
        for strg in strings:
            value = strg["String Value"]
            section = strg["Section"]
            addr = strg["Address"]

            item = QListWidgetItem("String: " + value + "\n"
                                   + '\tBinary Section: ' + section + "\n"
                                   + '\tAddress: ' + addr)
            self.detailed_points_of_interest_listWidget.addItem(item)
        self.display_strings_in_left_column()

    def display_strings_in_left_column(self):
        strings = data_manager.get_strings()

        for strg in strings:
            value = strg["String Value"]

            item = QListWidgetItem(value)

            # item.setCheckState(QtCore.Qt.Unchecked)
            self.points_of_interest_list_widget.addItem(item)

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
            # line = line.split(" ", 1)[-1]
            line = line.split(" ")[1]
            item = QListWidgetItem(line)

            # Don't know if we need this following line
            # item.setFlags(item.flags()|QtCore.Qt.ItemIsUserCheckable)

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
        name = self.plugin_name_lineedit.text()
        desc = self.plugin_description_textedit.toPlainText()
        self.plugin_view_plugin_listwidget.addItem(name)
        data_manager.save_plugin(name,desc)
        self.update_plugin_list()

    def update_plugin_list(self):
        plugins = data_manager.get_plugin_names()

        self.plugin_view_plugin_listwidget.clear()
        self.plugin_view_plugin_listwidget.addItems(plugins)

        self.existing_plugin_dropdown.clear()
        self.existing_plugin_dropdown.addItems(plugins)

        self.detailed_point_of_interest_view_existing_plugin_dropdown.clear()
        self.detailed_point_of_interest_view_existing_plugin_dropdown.addItems(plugins)
    '''
    Removes a selected plugin from the plugin list within Plugin Management 
    '''
    def remove_plugin(self):
        listItems = self.plugin_view_plugin_listwidget.selectedItems()
        if not listItems: return
        for item in listItems:
           self.plugin_view_plugin_listwidget.takeItem(self.plugin_view_plugin_listwidget.row(item))
           data_manager.delete_plugin_given_name(item)
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

    def add_poi_to_plugin(self):
        plugin = str(self.detailed_point_of_interest_view_existing_plugin_dropdown.currentText())
        poi_type = str(self.detailed_point_of_interest_view_type_dropdown.currentText())
        if poi_type == "Function":
            data_manager.add_function_to_plugin(plugin,poi_type)
        elif poi_type == "String":
            data_manager.add_string_to_plugin(plugin,poi_type)
        elif poi_type == "Variable":
            data_manager.add_variable_to_plugin(plugin,poi_type)
        elif poi_type == "DLL":
            data_manager.add_dll_to_plugin(plugin,poi_type)
        elif poi_type == "Packet Protocol":
            data_manager.add_packet_to_plugin(plugin,poi_type)
        elif poi_type == "Struct":
            data_manager.add_struct_to_plugin(plugin,poi_type)

        #data_manager.add_string_to_plugin(plugin,poi_type)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    BEAT = QtWidgets.QGroupBox()
    ui = UiMain()

    ui.setupUi(BEAT)
    ui.new_project()
    BEAT.show()
    sys.exit(app.exec_())