import data_manager
from PyQt5.QtWidgets import QListWidgetItem
staticIsRun = False
from PyQt5 import QtCore

import UiView
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QInputDialog, QApplication, QLineEdit, QMainWindow, QWidget, QPushButton, QAction, QLineEdit, QMessageBox

from PyQt5.QtCore import QDir

from Figure11CommentView import Ui_Figure11CommentView
from Figure12AnalysisResultReview import Ui_Figure12AnalysisResultReview
from Figure10OutputFieldView import Ui_Figure10OutputFieldView
from ArchitectureError import Ui_ArchitectureError
from PyQt5.QtWidgets import QListWidgetItem

from radare2_scripts import radare_commands_interface
from PyQt5.QtGui import QIcon, QPixmap

import UiHandlers
import os.path
from os import path
import threading
import time

self = ""
BEAT = ""

def set_self(s, b):
    global self
    global BEAT
    self = s
    BEAT = b

def project_deletion_message():
    global self
    name = self.project_list.currentItem().text()
    buttonReply = QMessageBox.question(BEAT, 'PyQt5 message',
        "Are you sure you want to permanently delete this project?", QMessageBox.Cancel | QMessageBox.Yes, QMessageBox.Cancel)
    if buttonReply == QMessageBox.Yes:
        data_manager.delete_project_given_name(name)
        # clear page
        clear_detailed_project_view()
        self.project_list.clear()
        fill_projects()
        print("Done Removing Project:", name)
        # disable deletion
        self.delete_project_button.setDisabled(True)

#########################################################################################
# Project Tab Functions
#########################################################################################
def project_selected():
    global self
    to_find = self.project_list.currentItem().text()
    name, desc, path, bin_info = data_manager.get_project_from_name(to_find)
    data_manager.update_current_project(name, desc, path, bin_info)
    # enable deletion
    self.delete_project_button.setDisabled(False)
    setCurrentProject()

def setCurrentProject():
    global self
    global BEAT
    name, desc, path, bin_info = data_manager.get_current_project_info()
    data_manager.initialize_POI_collections(name)

    # If no project set...
    if name == "":
        BEAT.setWindowTitle("BEAT")
    else:
        BEAT.setWindowTitle("BEAT - [PROJECT]: " + name + "    [BINARY]: " + path.split("/")[-1])
    # fill name text
    self.project_name_text.setText(name)
    self.project_name_text.setDisabled(True)
    # fill description test
    self.project_desc_text.setText(desc)
    self.project_desc_text.setDisabled(True)
    self.project_desc_text.setReadOnly(True)
    # fill path text
    self.file_path_lineedit.setText(path)
    self.file_path_lineedit.setDisabled(True)
    # disable buttons
    self.save_project_button.setDisabled(True)
    self.file_browse_button.setDisabled(True)
    # fill binary info
    fill_binary_info(bin_info)

'''
Sets settings for new project viewer
'''
def new_project():
    global self
    clear_detailed_project_view()

    self.project_name_text.setDisabled(False)
    self.project_desc_text.setDisabled(False)
    self.project_desc_text.setReadOnly(False)
    self.file_path_lineedit.setDisabled(False)
    self.save_project_button.setDisabled(False)
    self.file_browse_button.setDisabled(False)


'''
Clears all the input fields from the detailed project view
'''
def clear_detailed_project_view():
    global self
    self.project_name_text.setText("")
    self.project_desc_text.setText("")
    self.file_path_lineedit.setText("")
    self.binary_file_properties_value_listwidget.clear()

'''
Removes a project after it has been selected and the Delete button is clicked in Project
'''
def remove_project():
    global self
    name = self.project_list.currentItem().text()
    data_manager.delete_project_given_name(name)
    self.project_list.clear()
    self.binary_file_properties_value_listwidget.clear()
    fill_projects()
    print("Done Removing Project:", name)
    new_project()
'''
Fills projects list
'''
def fill_projects():
    global self
    self.project_list.clear()
    self.project_list.addItems(data_manager.get_project_names())

'''
Adds a project name to the projdynamic_runect list within Project
'''
def save_project():
    global self
    name = self.project_name_text.text()
    desc = self.project_desc_text.text()
    path = self.file_path_lineedit.text()
    bin_info = check_binary_arch(path)
    # check if the binary is correct architecture before saving
    if bin_info == None:  # display error window
        buttonReply = QMessageBox.warning(BEAT, 'x86 Architecture Error',
                                           "The selected binary is not of x86 architecture.", QMessageBox.Ok, QMessageBox.Ok)
        return
    else:
        data_manager.save_project(name, desc, path, bin_info)
        data_manager.update_current_project(name, desc, path, bin_info)
        fill_projects()
        setCurrentProject()

def check_binary_arch(path):
    global self
    binary_info = radare_commands_interface.parse_binary(path)
    if 'arch' in binary_info and binary_info['arch'] == 'x86':
        self.file_path_lineedit.setText(path)
        fill_binary_info(binary_info)
        return binary_info
    else:
        return None

'''
Opens the file browser and writes the selected file's filepath in file_path_lineedit 
'''
def browse_path():
    global self
    file_path, _ = QtWidgets.QFileDialog.getOpenFileName()
    self.file_path_lineedit.setText(file_path)

def fill_binary_info(bi):
    global self
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
def enable_dynamic_analysis():
    global self
    self.dynamic_run_button.setDisabled(False)
    self.dynamic_stop_button.setDisabled(False)
'''
Opens Figure12AnalysisResultReview
'''
def analysis_result():
    global self
    self.window = QtWidgets.QMainWindow()
    self.ui = Ui_Figure12AnalysisResultReview()
    self.ui.setupUi(self.window)
    self.window.show()
'''
Opens Ui_Figure10OutputFieldView
'''
def output_field():
    global self
    self.window = QtWidgets.QMainWindow()
    self.ui = Ui_Figure10OutputFieldView()
    self.ui.setupUi(self.window)
    self.window.show()

'''
Opens Ui_Figure11CommentView and will show comments for selected POI 
if the comment exists
'''
def comment_view():
    global self
    global BEAT
    comment_icon = QIcon.fromTheme("accessories-dictionary")
    no_comment_icon = QIcon.fromTheme("accessories-text-editor")

    current_item = self.points_of_interest_list_widget.currentItem()
    current_item_text = str(current_item.text())

    # retrieves comment and poi type
    comment, poi_type = data_manager.get_comment_from_name(current_item_text)

    comment_title = "Comment for POI " + current_item_text

    if not comment:
      comment = " "

    updated_comment, save = QInputDialog().getMultiLineText(BEAT, comment_title,
                                      "Comment:", comment)
    if save:
        data_manager.add_comment(current_item_text, poi_type, updated_comment)
        if not updated_comment or updated_comment == ' ':
            self.points_of_interest_list_widget.currentItem().setIcon(no_comment_icon)
        else:
            self.points_of_interest_list_widget.currentItem().setIcon(comment_icon)


'''
Works with save_comment to overwrite a comment that has already been placed 
on a POI  AND DOESNT WORK
'''
def replace_line(file_name, line_num, text):
    global self
    if not text:
        '''Do nothing'''
        print("Do nothing")


def static_analysis():
    global self
    radare_commands_interface.run_static_analysis()
    self.process_window.close()
'''
Runs analysis and displayss results
'''
def analyze_and_display_POI():
    global self
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

    t = threading.Thread(target=static_analysis)
    t.start()
    self.process_window.exec()

    global staticIsRun
    staticIsRun = True
    # Check What box is check  
    # Switch Cases to see what method is called
    display_value = str(self.type_dropdown.currentText())
    display_POI(display_value)
    enable_dynamic_analysis()


def match_selected_POI():
    global self
    row = self.points_of_interest_list_widget.currentRow()
    currentItem = self.points_of_interest_list_widget.currentItem()
    if not currentItem:
        return
    if currentItem.isSelected():
        self.detailed_points_of_interest_listWidget.itemAt(0, row).setSelected(True)
        self.detailed_points_of_interest_listWidget.setCurrentRow(row)

def change_displayed_POI():
    global self
    global staticIsRun
    if not staticIsRun:
        return
    self.detailed_points_of_interest_listWidget.clear()
    self.points_of_interest_list_widget.clear()
    display_value = str(self.type_dropdown.currentText())
    display_POI(display_value)

def display_POI(display_value):
    if display_value == "Imports":
        read_and_display_all_imports()
    elif display_value == "Strings":
        read_and_display_all_strings()
    elif display_value == "Function Call":
        read_and_display_all_functions()
    elif display_value == "Variables":
        read_and_display_global_variables()
    elif display_value == "All":
        read_and_display_all_functions()
        # variables displayed with functions instead
        read_and_display_global_variables()
        # self.read_and_display_all_imports()
        read_and_display_all_strings()

def set_right_breakpoint():
    display_value = str(self.type_dropdown.currentText())

    if display_value == "All":
        set_auto_breakpoint_at_string()
    elif display_value == "Strings":
        set_auto_breakpoint_at_string()
    elif display_value == "Function Call":
        set_auto_breakpoint_at_function()

def set_auto_breakpoint_at_all():
    global self
    print("Setting breakpoints")
    strings = data_manager.get_strings()

    for strg in strings:
        addr = strg["Address"]
        radare_commands_interface.set_breakpoint_at_strings(addr)

def set_auto_breakpoint_at_string():
    global self
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

def set_auto_breakpoint_at_function():
    global self
    print("Setting breakpoints")
    for i in range(self.points_of_interest_list_widget.count()):
        radare_commands_interface.set_breakpoint_at_function(self.points_of_interest_list_widget.item(i).text())

def remove_breakpoints(item):

    functions = data_manager.get_functions()
    for func in functions:
        if func['Function Name'] == item.text():
            addr_location = func['Binary Section']

    if item.checkState() == 2:  # if item is checked
        # radare_commands_interface.remove_breakpoint_at_function(item.text())
        radare_commands_interface.remove_breakpoint_at_function(addr_location)
    elif item.checkState() == 0:
        radare_commands_interface.set_breakpoint_at_function(addr_location)

def display_dynamic_info():
    global self
    things = radare_commands_interface.dynamicAnalysis()
    for t in things:
        self.detailed_points_of_interest_dynamic_info_listWidget.addItem(t)


'''
Runs analysis and displays results
'''
def run_dynamic_then_display():
    global self
    # radare_commands_interface.run_dynamic_and_update()
    self.dynamic_run_button.setDisabled(True)
    self.dynamic_stop_button.setDisabled(False)
    print("Running dynamic analysis!")
    print("Done with dynamic analysis!")
    change_displayed_POI()  # updates ui
    self.dynamic_run_button.setDisabled(False)
    self.dynamic_stop_button.setDisabled(True)
'''
Opens imports text file and displays it on detailed POI view
'''
def read_and_display_all_imports():
    global self
    imports = open("imports.txt", "r")
    for line in imports.read().split("\n"):
        item = QListWidgetItem(line)
        self.detailed_points_of_interest_listWidget.addItem(item)
    imports.close()
    display_imports_in_left_column()

def display_imports_in_left_column():
    global self
    comment_icon = QIcon.fromTheme("accessories-dictionary")
    no_comment_icon = QIcon.fromTheme("accessories-text-editor")
    imports = open("imports.txt", "r")
    # Start at the index 2 to the end get each line
    for line in imports.read().split("\n")[2:-1]:
        # Separate by spaces and then get the last word
        line = line.split(" ")[-1]
        item = QListWidgetItem(line)
        self.points_of_interest_list_widget.addItem(item)
    imports.close()

def read_and_display_all_functions():
    global self
    functions = data_manager.get_functions()

    for func in functions:
        if func["Analysis Run"] != "static":
            continue
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
        self.detailed_points_of_interest_listWidget.addItem(item)
        # display all variables related to current function
        read_and_display_variables_with_functions(func["Function Name"])
    display_functions_in_left_column()

def read_and_display_variables_with_functions(func_name):
    global self
    # display all variables related to current function
    variables = data_manager.get_variables()
    for var in variables:
        if func_name == var["Function Name"] and var["Analysis Run"] == "static":
            varItem = QListWidgetItem("\tLocal Variable Name: " + var["Variable Name"] + "\n"
                                      "\t\tType: " + var["Variable Type"] + "\n"
                                      "\t\tValue: " + var["Variable Value"] + "\n"
                                      "\t\tAddress: " + var["Address"])
            self.detailed_points_of_interest_listWidget.addItem(varItem)

def read_and_display_variables_with_functions_left_column(func_name):
    global self
    comment_icon = QIcon.fromTheme("accessories-dictionary")
    no_comment_icon = QIcon.fromTheme("accessories-text-editor")

    variables = data_manager.get_variables()
    # display all variables related to current function
    for var in variables:
        if func_name == var["Function Name"] and var["Analysis Run"] == "static":

            value = " " + var["Variable Name"]
            # Checking if poi has a comment
            if not var["Comment"] or var["Comment"] != ' ':
                varItem = QListWidgetItem(no_comment_icon, value)
            else:
                varItem = QListWidgetItem(comment_icon, value)

            self.points_of_interest_list_widget.addItem(varItem)

def display_functions_in_left_column():
    global self
    comment_icon = QIcon.fromTheme("accessories-dictionary")
    no_comment_icon = QIcon.fromTheme("accessories-text-editor")
    functions = data_manager.get_functions()
    for func in functions:
        if func["Analysis Run"] != "static":
            continue
        value = func["Function Name"]

        if not func["Comment"] or func["Comment"] != ' ':
            item = QListWidgetItem(no_comment_icon, value)
        else:
            item = QListWidgetItem(comment_icon, value)
        item.setCheckState(QtCore.Qt.Unchecked)
        self.points_of_interest_list_widget.addItem(item)

        # display all variables related to current function
        read_and_display_variables_with_functions_left_column(func["Function Name"])

def read_and_display_all_strings():
    global self
    strings = data_manager.get_strings()
    for strg in strings:
        value = strg["String Value"]
        section = strg["Section"]
        addr = strg["Address"]

        item = QListWidgetItem("String: " + value + "\n"
                               + '\tBinary Section: ' + section + "\n"
                               + '\tAddress: ' + addr)
        self.detailed_points_of_interest_listWidget.addItem(item)
    display_strings_in_left_column()

def display_strings_in_left_column():
    global self
    comment_icon = QIcon.fromTheme("accessories-dictionary")
    no_comment_icon = QIcon.fromTheme("accessories-text-editor")
    strings = data_manager.get_strings()

    for strg in strings:
        value = strg["String Value"]

        if not strg["Comment"] or strg["Comment"] != ' ':
            item = QListWidgetItem(no_comment_icon, value)
        else:
            item = QListWidgetItem(comment_icon, value)

        self.points_of_interest_list_widget.addItem(item)

def read_and_display_global_variables():
    global self
    variables = data_manager.get_global_variables()

    for var in variables:
        item = QListWidgetItem("Variable name: " + var['Variable Name'] + "\n"
                               + '\tVariable Size: ' + var['Variable Size'] + "\n"
                               + '\tVariable Value: ' + var['Variable Value'] + "\n"
                               + '\tAddress: ' + var['Address'])
        self.detailed_points_of_interest_listWidget.addItem(item)
    display_global_variables_in_left_column()

def display_global_variables_in_left_column():
    global self
    comment_icon = QIcon.fromTheme("accessories-dictionary")
    no_comment_icon = QIcon.fromTheme("accessories-text-editor")

    variables = data_manager.get_global_variables()

    for var in variables:
        value = var["Variable Name"]

        # Checking if poi has a comment
        if not var["Comment"] or var["Comment"] != ' ':
            item = QListWidgetItem(no_comment_icon, value)
        else:
            item = QListWidgetItem(comment_icon, value)

        self.points_of_interest_list_widget.addItem(item)

def search_POI():
    global self
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

#########################################################################################
# Plugin Management Tab Functions
#########################################################################################

'''
Allows you to add new plugins
'''
def new_plugin():
    global self
    self.plugin_structure_filepath_lineedit.setReadOnly(False)
    self.plugin_predefined_data_set_lineedit.setReadOnly(False)
    self.plugin_name_lineedit.setReadOnly(False)
    self.plugin_description_textedit.setReadOnly(False)
    self.points_of_interest_list_textedit.setReadOnly(False)

'''
Adds a plugin name to the plugin list in Plugin Management 
'''
def save_plugin():
    global self
    print('In save plugin...')
    import xmlparser
    if self.plugin_structure_filepath_lineedit.text() != "" and self.plugin_predefined_data_set_lineedit.text() == "":
        print('about to call xmlparser')

        xmlparser.parse_xml_plugin(self.plugin_structure_filepath_lineedit.text())
    elif self.plugin_name_lineedit.text() == "" or self.plugin_description_textedit.toPlainText() == "":
        print('error')
        self.msg_error = QMessageBox(QMessageBox.Question, "Name and Description Error",
                                     "Plugin name or description are empty", QMessageBox.Ok)
        self.msg_error.exec()
        return


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
        name = self.plugin_name_lineedit.text()
        desc = self.plugin_description_textedit.toPlainText()
        self.plugin_view_plugin_listwidget.addItem(name)
        data_manager.save_plugin(name,desc)
    update_plugin_list()

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

def update_plugin_list():
    global self
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
def remove_plugin():
    global self
    listItems = self.plugin_view_plugin_listwidget.selectedItems()
    if not listItems: return

    buttonReply = QMessageBox.question(BEAT, 'Plugin Deletion Warning',
        "Are you sure you want to permanently delete this plugin?", QMessageBox.Cancel | QMessageBox.Yes, QMessageBox.Cancel)
    if buttonReply == QMessageBox.Yes:
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
def browse_plugin_structure():
    global self
    file_path, _ = QtWidgets.QFileDialog.getOpenFileName()
    self.plugin_structure_filepath_lineedit.setText(file_path)
'''
Opens the file browser and writes the selected file's filepath in plugin_predefined_data_set_lineedit 
'''
def browse_plugin_dataset():
    global self
    file_path, _ = QtWidgets.QFileDialog.getOpenFileName()
    self.plugin_predefined_data_set_lineedit.setText(file_path)


def populate_pois_in_poi():
    global self
    print("Populating POIs in POI tab")
    to_find = str(self.detailed_point_of_interest_view_existing_plugin_dropdown.currentText())
    # save current plugin name in data manager
    print("--to_find", to_find)

    self.point_of_interest_view_listwidget.clear()

    if to_find == "":
        return
    try:
        print("Looking for strings...")
        strings = data_manager.get_pois_from_plugin_and_type(to_find, "string")
    except:
        print("No strings found")
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

def populate_name_and_description():
    global self
    try:
        to_find = self.plugin_view_plugin_listwidget.currentItem().text()
        name, desc = data_manager.get_plugin_from_name(to_find)
        self.plugin_name_lineedit.setText(name)
        self.plugin_description_textedit.setText(desc)
    except:
        return

def poi_type_changed_in_poi():
    global self
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

def change_plugin_in_poi():
    global self
    populate_pois_in_poi()
    
def run_command_from_cmd():
    global self
    cmd = self.terminal_input.text()
    if cmd  == "":
        self.msg_error = QMessageBox(QMessageBox.Question, "No Command Error", "A command must be given to run", QMessageBox.Ok)
        self.msg_error.exec()
        return
    result = radare_commands_interface.run_cmd(cmd)#.split('{}')
    self.detailed_points_of_interest_dynamic_info_listWidget.addItem(result)


def poi_in_poitab_selected():
    global self
    self.detailed_point_of_interest_view_delete_button.setDisabled(False)


def delete_poi():
    global self
    buttonReply = QMessageBox.question(BEAT, 'POI Deletion Warning',
                                       "Are you sure you want to permanently delete these Points of Interest?",
                                       QMessageBox.Cancel | QMessageBox.Yes, QMessageBox.Cancel)
    if buttonReply == QMessageBox.Yes:
        name = self.point_of_interest_view_listwidget.currentItem().text()
        plugin = str(self.detailed_point_of_interest_view_existing_plugin_dropdown.currentText())
        a = name.split(":")
        type = a[0]
        poi = a[2].strip(" ',}")
        data_manager.delete_poi_given_plugin_poitype_and_poi(plugin, type, poi)
        populate_pois_in_poi()
        self.detailed_point_of_interest_view_delete_button.setDisabled(True)




def delete_pois():
    global self
    buttonReply = QMessageBox.question(BEAT, 'POI Deletion Warning',
                                       "Are you sure you want to permanently delete these Points of Interest?",
                                       QMessageBox.Cancel | QMessageBox.Yes, QMessageBox.Cancel)
    if buttonReply == QMessageBox.Yes:
        try:
            name = self.point_of_interest_view_listwidget.currentItem().text()
        except:
            self.msg_error = QMessageBox(QMessageBox.Question, "No POI to Delete Error",
                                     "Please select a POI to delete", QMessageBox.Ok)
            self.msg_error.exec()
            return
        plugin = str(self.detailed_point_of_interest_view_existing_plugin_dropdown.currentText())
        a = name.split(":")
        type = a[0]
        poi = a[2].strip(" ',}")
        data_manager.delete_poi_given_plugin_poitype_and_poi(plugin, type, poi)
        populate_pois_in_poi()

def save_poi():
    global self
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
        name = self.poi_dll_libraryname_lineedit.text()
        data_manager.add_dll_to_plugin(plugin, name)

        self.poi_dll_libraryname_lineedit.setText("")

    populate_pois_in_poi()

def populate_pois_in_plugin():
    global self
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
def document_deletion_message():
    global self
    name = self.document_view_listwidget.currentItem().text()
    buttonReply = QMessageBox.question(BEAT, 'PyQt5 message',
        "Are you sure you want to permanently delete this document?", QMessageBox.Cancel | QMessageBox.Yes, QMessageBox.Cancel)
    if buttonReply == QMessageBox.Yes:
        self.document_view_listwidget.clear()
        print("Done Removing Document:", name)
def new_document():
    global self
    self.textbox = QLineEdit(self)
    self.textbox.move(20, 20)
    self.textbox.resize(280,40)
    os.path.join('./', filename + "." + 'txt')
    open(filename, 'a').close()
    self.document_view_listwidget.addItem(filename)
def remove_document():
    global self
    os.remove(self.document_view_listwidget.itemClicked)
    os.removed("Test")
def search_Project():
    global self
    text = str(self.project_search_lineedit.text())
    if len(text) is not 0:
        search_result = self.project_list.findItems(text, QtCore.Qt.MatchContains)
        for item in range(self.project_list.count()):
            self.project_list.item(item).setHidden(True)
        for item in search_result:
            item.setHidden(False)
    else:
        for item in range(self.project_list.count()):
            self.project_list.item(item).setHidden(False)


def fill_documents():
    global self
    for file in os.listdir("./"):
        if file.endswith(".txt"):
            txt_list = os.path.join("", file)
            stripped_txt_list = os.path.splitext(file)[0]
            self.document_view_listwidget.addItem(stripped_txt_list)
def save_document():
    global self
    document = open("README.txt", "a")
    document.write(self.document_content_area_textedit.textChanged.connect(self.document_save_button))

def search_Plugin():
    global self
    text = str(self.plugin_view_search_lineedit.text())
    if len(text) is not 0:
        search_result = self.plugin_view_plugin_listwidget.findItems(text, QtCore.Qt.MatchContains)
        for item in range(self.plugin_view_plugin_listwidget.count()):
            self.plugin_view_plugin_listwidget.item(item).setHidden(True)
        for item in search_result:
            item.setHidden(False)
    else:
        for item in range(self.points_of_interest_list_widget.count()):
            self.points_of_interest_list_widget.item(item).setHidden(False)
        for item in range(self.plugin_view_plugin_listwidget.count()):
            self.plugin_view_plugin_listwidget.item(item).setHidden(False)

def search_POI_View():
    global self
    text = str(self.point_of_interest_view_search_lineedit.text())
    if len(text) is not 0:
        search_result = self.point_of_interest_view_listwidget.findItems(text, QtCore.Qt.MatchContains)
        for item in range(self.point_of_interest_view_listwidget.count()):
            self.point_of_interest_view_listwidget.item(item).setHidden(True)
        for item in search_result:
            item.setHidden(False)
    else:
        for item in range(self.point_of_interest_view_listwidget.count()):
            self.point_of_interest_view_search_lineedit.item(item).setHidden(False)

def search_Document():
    global self
    text = str(self.document_view_search_lineedit.text())
    if len(text) is not 0:
        search_result = self.document_view_listwidget.findItems(text, QtCore.Qt.MatchContains)
        for item in range(self.document_view_listwidget.count()):
            self.document_view_listwidget.item(item).setHidden(True)
        for item in search_result:
            item.setHidden(False)
    else:
        for item in range(self.document_view_listwidget.count()):
            self.document_view_listwidget.item(item).setHidden(False)

# This prints the contents of the documentation files found in the Document View.
def README_document(filename):
    global self
    # This prints the BEAT Documentation Content as a README.
    if filename in 'README':
        with open('README.txt', 'r') as readMe:
            ReadMeString = readMe.read()
    return ReadMeString

def Plugin_document(filename):
    global self
    # This prints the BEAT Documentation Content as a README.
    if filename in 'Plugin':
        with open('test_plugin.txt', 'r') as plugin:
            pluginString = plugin.read()
    return pluginString

def display_ReadMe():
    global self
    self.document_content_area_textedit.setText(README_document('README'))

def display_Plugin():
    global self
    self.document_content_area_textedit.setText(Plugin_document('Plugin'))

def display_documentation():
    global self
    self.document_content_area_textedit.setText(documentation("BEAT Documentation"))

def documentation(filename):
    global self
    if filename in 'BEAT Documentation':
        with open('beat_documentation.txt', 'r') as plugin:
            pluginString = plugin.read()
    return pluginString

def display_tab_guide():

    self.document_content_area_textedit.setText(tab_doc("Tab Guide"))

def tab_doc(filename):
    global self
    if filename in 'Tab Guide':
        with open('tab_guide.txt', 'r') as tab:
            pluginString = tab.read()
    return pluginString

def change_doc():
    global self
    # ['README', 'BEAT Documentation', 'XML Structures', 'Tab Guide']
    doc = self.document_view_listwidget.currentItem().text()
    if doc == "README":
        display_ReadMe()
    if doc == "BEAT Documentation":
        display_documentation()
    if doc == "XML Structures":
        display_Plugin()
    if doc == "Tab Guide":
        display_tab_guide()