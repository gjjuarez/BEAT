from PyQt5 import QtCore

import UiView
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QInputDialog, QApplication, QLineEdit, QMainWindow, QWidget, QPushButton, QAction, QLineEdit, QMessageBox

from PyQt5.QtCore import QDir

from Figure11CommentView import Ui_Figure11CommentView
from Figure12AnalysisResultReview import Ui_Figure12AnalysisResultReview
from ArchitectureError import Ui_ArchitectureError
from PyQt5.QtWidgets import QListWidgetItem
from Terminal import EmbTerminalLinux

from radare2_scripts import radare_commands_interface
from PyQt5 import QtGui
import data_manager
import os.path
from os import path
import threading
import time

class UiMain(UiView.Ui_BEAT):
    global staticIsRun
    staticIsRun = False

    valid_extensions = ["exe", "dll"]

    def setupUi(self, BEAT):
        super().setupUi(BEAT)
        #self.file_path_lineedit.setEd
        ###########################
        # Resizing according to user's desktop
        ###########################
        self.geo = QtWidgets.QDesktopWidget().screenGeometry()
        BEAT.resize(self.geo.width(), self.geo.height())

        BEAT.setMaximumSize(QtCore.QSize(16777215, 16777215))

        #User cannot delete unselected project
        self.delete_project_button.setDisabled(True)

        self.run_button.setDisabled(True)

        #User cannot edit project fields without creating a new project
        self.project_name_text.setDisabled(True)
        self.project_desc_text.setDisabled(True)
        self.file_path_lineedit.setDisabled(True)
        self.save_project_button.setDisabled(True)

        # User cannot run dynamic in the beginning of the program
        self.dynamic_run_button.setDisabled(True)
        self.dynamic_stop_button.setDisabled(True)
        self.Poi_stacked_Widget.setCurrentIndex(2)

        # Fill the Project list from mongo
        self.fill_projects()

        self.update_plugin_list()

        self.terminal = EmbTerminalLinux(self.detailed_point_of_interest_view_groupbox)
        self.terminal.setGeometry(QtCore.QRect(15, 310, 561, 90))
        self.terminal.setObjectName("Terminal")

        self.stacked = QtWidgets.QStackedWidget()
        self.stacked.addWidget(self.terminal)

        self.setCurrentProject()

        self.populate_pois_in_poi()
        #########################################################################################
        # Project Tab Functions
        #########################################################################################
        '''
        Project Tab Listeners
        '''
        # calls new_project if new_project_bsutton is clicked
        self.new_project_button.clicked.connect(self.new_project)
        # calls remove_project if delete_project_button is clicked
        self.delete_project_button.clicked.connect(self.project_deletion_message)
        # calls save_project if save_project_button is clicked
        self.save_project_button.clicked.connect(self.save_project)
        # calls browse_path if file_browse_button is clicked
        self.file_browse_button.clicked.connect(self.browse_path)
        # self.delete_project_button.connect(self.delete_current_project)

        '''
        Analysis Tab Listeners 
        '''
        # calls enable_dynamic_analysis after static_run_button is clicked
        # self.static_run_button.clicked.connect(self.enable_dynamic_analysis)
        #self.static_run_button.clicked.connect(self.analysis_running_frame.show)
        # calls analysis_result aft er analysis_result_button is clicked
        self.analysis_result_button.clicked.connect(self.analysis_result)
        # calls comment_view after comment_button is clicked
        self.comment_button.clicked.connect(self.comment_view)

        self.run_button.clicked.connect(self.run_command_from_cmd)

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
        self.plugin_view_plugin_listwidget.itemClicked.connect(self.populate_pois_in_plugin)
        self.plugin_view_plugin_listwidget.itemClicked.connect(self.populate_name_and_description)

        #Allows you to create a new plugin
        self.plugin_view_new_button.clicked.connect(self.new_plugin)

        '''
        Points of Interest Tab Listeners
        '''        
        self.detailed_point_of_interest_view_type_dropdown.clear()
        self.detailed_point_of_interest_view_type_dropdown.addItems(["Function","String", "Variable", "DLL"])
        #self.detailed_point_of_interest_view_save_button.clicked.connect(self.add_poi_to_plugin)

        self.detailed_point_of_interest_view_type_dropdown.currentIndexChanged.connect(self.poi_type_changed_in_poi)
        self.detailed_point_of_interest_view_save_button.clicked.connect(self.save_poi)

        self.detailed_point_of_interest_view_existing_plugin_dropdown.currentIndexChanged.connect(self.change_plugin_in_poi)
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
        self.type_dropdown.clear()
        self.type_dropdown.addItem("All")
        self.type_dropdown.addItem("Function Call")
        self.type_dropdown.addItem("Variables")
        self.type_dropdown.addItem("Strings")
        # sets breakpoints on currently checked items
        self.points_of_interest_list_widget.itemChanged.connect(self.remove_breakpoints) #this is breaking the program when you search something
        # runs dynamic analysis on breakpoints then updates ui
        self.dynamic_run_button.clicked.connect(self.set_right_breakpoint)
        self.dynamic_run_button.clicked.connect(self.display_dynamic_info)
        # self.dynamic_run_button.clicked.connect(self.set_auto_breakpoint)
        #self.dynamic_run_button.clicked.connect(self.run_dynamic_then_display)
        # match detailed view with left column when selected
        self.points_of_interest_list_widget.itemClicked.connect(self.match_selected_POI)

        QtCore.QMetaObject.connectSlotsByName(BEAT)
        self.project_list.itemClicked.connect(self.project_selected)

    #########################################################################################
    # QMessageBox Warning Functions
    #########################################################################################
    def project_deletion_message(self):
        name = self.project_list.currentItem().text()
        buttonReply = QMessageBox.question(BEAT, 'PyQt5 message',
            "Are you sure you want to permanently delete this project?", QMessageBox.Cancel | QMessageBox.Yes, QMessageBox.Cancel)
        if buttonReply == QMessageBox.Yes:
            data_manager.delete_project_given_name(name)
            # clear page
            self.clear_detailed_project_view()
            self.project_list.clear()
            self.fill_projects()
            print("Done Removing Project:", name)
            # disable deletion
            self.delete_project_button.setDisabled(True)



    # def plugin_deletion_message(self):
    #     listItems = self.plugin_view_plugin_listwidget.selectedItems()
    #     if not listItems: return
    #     buttonReply = QMessageBox.question(BEAT, 'PyQt5 message',
    #         "Are you sure you want to permanently delete this plugin?", QMessageBox.Cancel | QMessageBox.Yes, QMessageBox.Cancel)
    #     if buttonReply == QMessageBox.Yes:
    #         for item in listItems:
    #             self.plugin_view_plugin_listwidget.takeItem(self.plugin_view_plugin_listwidget.row(item))
    #             data_manager.delete_plugin_given_name(item)

    #########################################################################################
    # Project Tab Functions
    #########################################################################################
    def project_selected(self):
        to_find = self.project_list.currentItem().text()
        name, desc, path, bin_info = data_manager.get_project_from_name(to_find)
        data_manager.update_current_project(name, desc, path, bin_info)
        # enable deletion
        self.delete_project_button.setDisabled(False)
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
        self.project_name_text.setStyleSheet("color: gray;")
        self.project_name_text.setReadOnly(True)
        # fill description test
        self.project_desc_text.setText(desc)
        self.project_desc_text.setReadOnly(False)
        # fill path text
        self.file_path_lineedit.setText(path)
        self.file_path_lineedit.setStyleSheet("color: gray;")
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
        self.clear_detailed_project_view()

        self.project_name_text.setDisabled(False)
        self.project_name_text.setReadOnly(False)

        self.project_desc_text.setDisabled(False)
        self.project_desc_text.setReadOnly(False)

       # self.file_path_lineedit.setDisabled(False)
        self.file_path_lineedit.setReadOnly(False)

        self.save_project_button.setDisabled(False)
        self.file_browse_button.setDisabled(False)


    '''
    Clears all the input fields from the detailed project view
    '''
    def clear_detailed_project_view(self):
        self.project_name_text.setText("")
        self.project_desc_text.setText("")
        self.file_path_lineedit.setText("")
        self.binary_file_properties_value_listwidget.clear()

    '''
    Removes a project after it has been selected and the Delete button is clicked in Project
    '''

    def remove_project(self):
        name = self.project_list.currentItem().text()
        data_manager.delete_project_given_name(name)
        self.project_list.clear()
        self.binary_file_properties_value_listwidget.clear()
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
            buttonReply = QMessageBox.warning(BEAT, 'x86 Architecture Error',
                                               "The selected binary is not of x86 architecture.", QMessageBox.Ok, QMessageBox.Ok)
            return
            '''
            self.window = QtWidgets.QMainWindow()
            self.ui = Ui_ArchitectureError()
            self.ui.setupUi(self.window)
            self.window.show()
            '''

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
            self.binary_file_properties_value_listwidget.setStyleSheet("color: gray;")
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
        self.dynamic_run_button.setDisabled(False)
        self.dynamic_stop_button.setDisabled(False)
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
        from PyQt5 import QtGui
        current_item = self.points_of_interest_list_widget.currentItem()
        current_item_text = str(current_item.text())
        print(current_item_text)

        # retrieves comment and poi type
        comment, poi_type = data_manager.get_comment_from_name(current_item_text)

        comment_title = "Comment for POI " + current_item_text

        if not comment:
            comment = " "

        updated_comment, save = QInputDialog().getMultiLineText(BEAT, comment_title,
                                          "Comment:", comment)
        if save:
            print(updated_comment)
            data_manager.add_comment(current_item_text, poi_type, updated_comment)


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



    def static_analysis(self):
        radare_commands_interface.run_static_analysis()
        self.process_window.close()
    '''
    Runs analysis and displayss results
    '''
    def analyze_and_display_POI(self):
        self.run_button.setDisabled(False)
        try:
            x, y, z, a = data_manager.getCurrentProjectInfo()

        except:
            self.msg_error = QMessageBox(QMessageBox.Question, "No Project Error", "There must be a project set to run static analysis", QMessageBox.Ok)
            self.msg_error.exec()
            return

        self.process_window = QtWidgets.QProgressDialog("Running Static Analysis...", None, 0,0)
        self.detailed_points_of_interest_listWidget.clear()
        self.points_of_interest_list_widget.clear()

        t = threading.Thread(target=self.static_analysis)
        t.start()
        self.process_window.exec()

        global staticIsRun
        staticIsRun = True
        # Check What box is check  
        # Switch Cases to see what method is called
        display_value = str(self.type_dropdown.currentText())
        self.display_POI(display_value)
        self.enable_dynamic_analysis()


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
            self.read_and_display_global_variables()
        elif display_value == "All":
            self.read_and_display_all_functions()
            # variables displayed with functions instead
            self.read_and_display_global_variables()
            # self.read_and_display_all_imports()
            self.read_and_display_all_strings()

    def set_right_breakpoint(self):
        display_value = str(self.type_dropdown.currentText())

        if display_value == "All":
            print("Have to do things here")
            self.set_auto_breakpoint_at_string()
        elif display_value == "Strings":
            self.set_auto_breakpoint_at_string()
        elif display_value == "Function Call":
            self.set_auto_breakpoint_at_function()

    def set_auto_breakpoint_at_all(self):
        print("Setting breakpoints")
        strings = data_manager.get_strings()

        for strg in strings:
            addr = strg["Address"]
            radare_commands_interface.set_breakpoint_at_strings(addr)

    def set_auto_breakpoint_at_string(self):
        print("Setting breakpoints")
        strings = data_manager.get_strings()
        functions = data_manager.get_functions()
        variables = data_manager.get_variables()

        for func in functions:
            radare_commands_interface.set_breakpoint_at_function(func['Binary Section'])
            for var in variables:
                if func['Function Name'] == var["Function Name"]:
                    radare_commands_interface.set_breakpoint_for_var_inside_function(var["Address"])

        for strg in strings:
            addr = strg["Address"]
            radare_commands_interface.set_breakpoint_at_strings(addr)

    def set_auto_breakpoint_at_function(self):
        print("Setting breakpoints")
        for i in range(self.points_of_interest_list_widget.count()):
            radare_commands_interface.set_breakpoint_at_function(self.points_of_interest_list_widget.item(i).text())

    def remove_breakpoints(self, item):
        functions = data_manager.get_functions()
        for func in functions:
            if func['Function Name'] == item.text():
                addr_location = func['Binary Section']

        if item.checkState() == 2:  # if item is checked
            # radare_commands_interface.remove_breakpoint_at_function(item.text())
            radare_commands_interface.remove_breakpoint_at_function(addr_location)
        elif item.checkState() == 0:
            radare_commands_interface.set_breakpoint_at_function(addr_location)

    def display_dynamic_info(self):
        things = radare_commands_interface.dynamicAnalysis()
        for t in things:
            self.detailed_points_of_interest_dynamic_info_listWidget.addItem(t)


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
                    paramTypes = paramTypes + " " + pt
            except TypeError:
                paramTypes = ""

            paramOrder = ""
            try:
                for pt in func["Parameter Order"]:
                    paramOrder = paramOrder + " " + pt
            except TypeError:
                paramOrder = ""

            paramValue = ""
            try:
                for pt in func["Parameter Value"]:
                    paramValue = paramValue + " " + pt
            except TypeError:
                paramValue = ""

            callFrom = ""
            try:
                for pt in func["Call From"]:
                    callFrom = callFrom + " " + pt
            except TypeError:
                callFrom = ""

            returnVal = ""
            if func['Return Value']:
                returnVal = func['Return Value']

            returnType = ""
            if func['Return Type']:
                returnType = func['Return Type']
            item = QListWidgetItem("Function name: " + func['Function Name'] + "\n"
                                   + '\tReturn Type: ' + returnType + "\n"
                                   + '\tReturn Value: ' + returnVal + "\n"
                                   + '\tAddress: ' + func['Address'] + "\n"
                                   + '\tParameter Order: ' + paramOrder + "\n"
                                   + '\tParameter Type: ' + paramTypes + "\n"
                                   + '\tParameter Value: ' + paramValue + "\n"
                                   + '\tBinary Section: ' + func['Binary Section'] + "\n"
                                   + '\tCalled From: ' + callFrom)
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
                varItem = QListWidgetItem("\tLocal Variable Name: " + var["Variable Name"] + "\n"
                                          "\t\tType: " + var["Variable Type"] + "\n"
                                          "\t\tValue: " + var["Variable Value"] + "\n"
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

    def read_and_display_global_variables(self):
        variables = data_manager.get_global_variables()

        for var in variables:
            item = QListWidgetItem("Variable name: " + var['Variable Name'] + "\n"
                                   + '\tVariable Size: ' + var['Variable Size'] + "\n"
                                   + '\tVariable Value: ' + var['Variable Value'] + "\n"
                                   + '\tAddress: ' + var['Address'])
            self.detailed_points_of_interest_listWidget.addItem(item)
        self.display_global_variables_in_left_column()

    def display_global_variables_in_left_column(self):
        variables = data_manager.get_global_variables()

        for var in variables:
            value = var["Variable Name"]

            item = QListWidgetItem(value)

            # item.setCheckState(QtCore.Qt.Unchecked)
            self.points_of_interest_list_widget.addItem(item)

    def search_POI(self):
        text = str(self.points_of_interest_line_edit.text())
        if len(text) is not 0:
            search_result = self.points_of_interest_list_widget.findItems(text, QtCore.Qt.MatchContains)
            for item in range(self.points_of_interest_list_widget.count()):
                self.points_of_interest_list_widget.item(item).setHidden(True)
            for item in search_result:
                item.setHidden(False)
        else:
            for item in range(self.points_of_interest_list_widget.count()):
                self.points_of_interest_list_widget.item(item).setHidden(False)

    # this method highlights the searched POI but breaks the program because it somehow calls the remove breakpoints method with the current listener it has
    # def search_POI(self):
    #     # clear background in left column
    #     for i in range(self.points_of_interest_list_widget.count()):
    #         self.points_of_interest_list_widget.item(i).setBackground(QtGui.QBrush(QtCore.Qt.color0))
    #     # clear background for detailed view
    #     for i in range(self.detailed_points_of_interest_listWidget.count()):
    #         self.detailed_points_of_interest_listWidget.item(i).setBackground(QtGui.QBrush(QtCore.Qt.color0))
    #
    #     display_value = str(self.points_of_interest_line_edit.text())
    #     # don't search if empty string
    #     if display_value == "":
    #         return
    #     # highlights search in left column
    #     search_result = self.points_of_interest_list_widget.findItems(display_value, QtCore.Qt.MatchContains)
    #     if len(search_result) > 0:
    #         for item in search_result:
    #             item.setBackground(QtGui.QBrush(QtCore.Qt.magenta))
    #     # highlights search in detailed view
    #     search_result = self.detailed_points_of_interest_listWidget.findItems(display_value, QtCore.Qt.MatchContains)
    #     if len(search_result) > 0:
    #         for item in search_result:
    #             item.setBackground(QtGui.QBrush(QtCore.Qt.magenta))

    #########################################################################################
    # Plugin Management Tab Functions
    #########################################################################################

    '''
    Allows you to add new plugins
    '''
    def new_plugin(self):
        self.plugin_structure_filepath_lineedit.setReadOnly(False)
        self.plugin_predefined_data_set_lineedit.setReadOnly(False)
        self.plugin_name_lineedit.setReadOnly(False)
        self.plugin_description_textedit.setReadOnly(False)
        self.points_of_interest_list_textedit.setReadOnly(False)

    '''
    Adds a plugin name to the plugin list in Plugin Management 
    '''
    def save_plugin(self):
        print('in save plugin')
        if self.plugin_name_lineedit.text() == "" or self.plugin_description_textedit.toPlainText() == "":
            print('error')
            self.msg_error = QMessageBox(QMessageBox.Question, "Name and Description Error",
                                         "Plugin name or description are empty", QMessageBox.Ok)
            self.msg_error.exec()
            return
        elif self.plugin_structure_filepath_lineedit.text() != "" and self.plugin_predefined_data_set_lineedit.text() == "":
            print('about to call xmlparser')
            import xmlparser
            xmlparser.parse_xml_plugin(self.plugin_structure_filepath_lineedit.text())

        elif self.plugin_predefined_data_set_lineedit.text() != "" and self.plugin_structure_filepath_lineedit.text() == "":
            print('about to call xmlparser')
            import xmlparser
            xmlparser.parse_xml_poi(self.plugin_predefined_data_set_lineedit.text(), self.plugin_name_lineedit.text(), self.plugin_description_textedit.toPlainText())

        elif self.plugin_structure_filepath_lineedit.text() != "" and self.plugin_predefined_data_set_lineedit.text() != "":
            print('error')
            self.msg_error = QMessageBox(QMessageBox.Question, "Unclear plugin type Error",
                                         "Too many fields are filled out", QMessageBox.Ok)
            self.msg_error.exec()
            return

        else:
            print("1234")
            name = self.plugin_name_lineedit.text()
            desc = self.plugin_description_textedit.toPlainText()
            self.plugin_view_plugin_listwidget.addItem(name)
            data_manager.save_plugin(name,desc)
        self.update_plugin_list()

        self.plugin_structure_filepath_lineedit.clear()
        self.plugin_predefined_data_set_lineedit.clear()
        self.plugin_name_lineedit.clear()
        self.plugin_description_textedit.clear()
        self.points_of_interest_list_textedit.clear()

        self.plugin_structure_filepath_lineedit.setReadOnly(True)
        self.plugin_predefined_data_set_lineedit.setReadOnly(True)
        self.plugin_name_lineedit.setReadOnly(True)
        self.plugin_description_textedit.setReadOnly(True)
        self.points_of_interest_list_textedit.setReadOnly(True)

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
           data_manager.delete_plugin_given_name(item.text())

        self.plugin_structure_filepath_lineedit.clear()
        self.plugin_predefined_data_set_lineedit.clear()
        self.plugin_name_lineedit.clear()
        self.plugin_description_textedit.clear()
        self.points_of_interest_list_textedit.clear()
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

    # def add_poi_to_plugin(self):
    #     print("Populating POIs in Plugin tab")
    #     plugin = str(self.detailed_point_of_interest_view_existing_plugin_dropdown.currentText())
    #     poi_type = str(self.detailed_point_of_interest_view_type_dropdown.currentText())
    #     to_add = self.point_of_interest_content_area_textedit.toPlainText()
    #     if poi_type == "Function":
    #         data_manager.add_function_to_plugin(plugin,to_add)
    #     elif poi_type == "String":
    #         data_manager.add_string_to_plugin(plugin,to_add)
    #     elif poi_type == "Variable":
    #         data_manager.add_variable_to_plugin(plugin,to_add)
    #     elif poi_type == "DLL":
    #         data_manager.add_dll_to_plugin(plugin,to_add)
    #     elif poi_type == "Packet Protocol":
    #         data_manager.add_packet_to_plugin(plugin,to_add)
    #     elif poi_type == "Struct":
    #         data_manager.add_struct_to_plugin(plugin,to_add)
    #
    #     self.point_of_interest_content_area_textedit.clear()
    #     self.populate_pois_in_poi()

        #data_manager.add_string_to_plugin(plugin,poi_type)
    def populate_pois_in_poi(self):
        print("Populating POIs in POI tab")
        to_find = str(self.detailed_point_of_interest_view_existing_plugin_dropdown.currentText())
        # save current plugin name in data manager
        print("--to_find", to_find)

        self.point_of_interest_view_listwidget.clear()

        if to_find == "": return
        try:
            print("Lookinf for strings")
            strings = data_manager.get_pois_from_plugin_and_type(to_find, "string")
        except:
            print("no strings found")
            strings = ""
        try:
            functions = data_manager.get_pois_from_plugin_and_type(to_find, "function")
        except:
            functions = ""
        try:
            variables = data_manager.get_pois_from_plugin_and_type(to_find, "variable")
        except:
            variables = ""
        try:
            dll = data_manager.get_pois_from_plugin_and_type(to_find, "dll")
        except:
            dll = ""


        if strings is not None:
            for s in strings:
                self.point_of_interest_view_listwidget.addItem(QListWidgetItem("String:"+ str(s)))
        if functions is not None:
            for f in functions:
                self.point_of_interest_view_listwidget.addItem(QListWidgetItem("Function:"+ str(f)))
        if variables is not None:
            for v in variables:
                self.point_of_interest_view_listwidget.addItem(QListWidgetItem("Variables:"+ str(v)))
        if dll is not None:
            for d in dll:
                self.point_of_interest_view_listwidget.addItem(QListWidgetItem("DLL:"+ str(d)))

    def populate_name_and_description(self):
        print("HERE")
        try:
            to_find = self.plugin_view_plugin_listwidget.currentItem().text()
            print(to_find)
            name, desc = data_manager.get_plugin_from_name(to_find)
            print("zxcvbnm")
            print(name)
            print(desc)
            # self.plugin_name_lineedit.setText(name)
            # self.plugin_description_textedit.clear(desc)
        except:
            return

    def poi_type_changed_in_poi(self):
        poi_detected = str(self.detailed_point_of_interest_view_type_dropdown.currentText())
        # ["Function","String", "Variable", "DLL"]
        if poi_detected == "Function":
            self.Poi_stacked_Widget.setCurrentIndex(2)
        elif poi_detected == "String":
            self.Poi_stacked_Widget.setCurrentIndex(3)
        elif poi_detected == "Variable":
            self.Poi_stacked_Widget.setCurrentIndex(0)
        elif poi_detected == "DLL":
            self.Poi_stacked_Widget.setCurrentIndex(1)

    def change_plugin_in_poi(self):
        self.populate_pois_in_poi()
        
    def run_command_from_cmd(self):
        cmd = self.terminal_input.text()
        if cmd  == "":
            self.msg_error = QMessageBox(QMessageBox.Question, "No Command Error", "A command must be given to run", QMessageBox.Ok)
            self.msg_error.exec()
            return
        result = radare_commands_interface.run_cmd(cmd).split('{}')
        self.detailed_points_of_interest_dynamic_info_listWidget.addItem(result)

    def save_poi(self):
        poi_detected = str(self.detailed_point_of_interest_view_type_dropdown.currentText())
        plugin = str(self.detailed_point_of_interest_view_existing_plugin_dropdown.currentText())
        # ["Function","String", "Variable", "DLL"]
        if poi_detected == "Function":
            name = self.poi_function_name_lineedit.text()
            type = self.poi_function_parameter_lineedit.text()
            
            return_val = self.poi_function_returntype_lineedit.text()

            data_manager.add_function_to_plugin(plugin, name, type, return_val)

            self.poi_function_name_lineedit.setText("")
            self.poi_function_parameter_lineedit.setText("")
            self.poi_function_returntype_lineedit.setText("")

        elif poi_detected == "String":
            name = self.poi_string_name_lineedit.text()

            data_manager.add_string_to_plugin(plugin,name)

            self.poi_string_name_lineedit.setText("")


        elif poi_detected == "Variable":
            name = self.poi_variable_name_lineedit.text()
            var_type = self.poi_variable_type_lineedit.text()
            data_manager.add_variable_to_plugin(plugin,name, var_type)

            self.poi_variable_name_lineedit.setText("")
            self.poi_variable_type_lineedit.setText("")

        elif poi_detected == "DLL":
            print("geting dlllllllllllllllllllllllll :D")
            name = self.poi_dll_libraryname_lineedit.text()
            print(name)
            data_manager.add_dll_to_plugin(plugin, name)

            self.poi_dll_libraryname_lineedit.setText("")

        #self.point_of_interest_content_area_textedit.clear()
        self.populate_pois_in_poi()

    def populate_pois_in_plugin(self):
        #self.points_of_interest_list_textedit()
        try:
            to_find = self.plugin_view_plugin_listwidget.currentItem().text()
            data_manager.set_current_plugin(to_find)

            try:
                strings = data_manager.get_pois_from_plugin_and_type(to_find, "string")
            except:
                strings = ""
            try:
                functions = data_manager.get_pois_from_plugin_and_type(to_find, "function")
            except:
                functions = ""
            try:
                variables = data_manager.get_pois_from_plugin_and_type(to_find, "variable")
            except:
                variables = ""
            try:
                dll = data_manager.get_pois_from_plugin_and_type(to_find, "dll")
            except:
                dll = ""

            self.points_of_interest_list_textedit.clear()
            self.points_of_interest_list_textedit.append("Strings:"+ str(strings)+ "\n")
            self.points_of_interest_list_textedit.append("Functions:"+ str(functions)+ "\n")
            self.points_of_interest_list_textedit.append("Variables:"+ str(variables)+ "\n")
            self.points_of_interest_list_textedit.append("DLLs:"+ str(dll)+ "\n")
        except:
            return


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    BEAT = QtWidgets.QGroupBox()
    ui = UiMain()

    ui.setupUi(BEAT)
    #ui.new_project()
    BEAT.show()
    sys.exit(app.exec_())
