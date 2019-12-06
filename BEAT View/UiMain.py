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
from Terminal import EmbTerminalLinux

from radare2_scripts import radare_commands_interface
from PyQt5.QtGui import QIcon, QPixmap

import UiHandlers
import os.path
from os import path
import threading
import time

class UiMain(UiView.Ui_BEAT):
    global staticIsRun   

    valid_extensions = ["exe", "dll"]

    def setupUi(self, BEAT):
        super().setupUi(BEAT)
        UiHandlers.set_self(self, BEAT)

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
        UiHandlers.fill_projects()

        # User cannot delete an unselected POI from the POI Tab
        self.detailed_point_of_interest_view_delete_button.setDisabled(True)
        UiHandlers.update_plugin_list()

        self.terminal = EmbTerminalLinux(self.detailed_point_of_interest_view_groupbox)
        self.terminal.setGeometry(QtCore.QRect(15, 310, 561, 90))
        self.terminal.setObjectName("Terminal")

        self.stacked = QtWidgets.QStackedWidget()
        self.stacked.addWidget(self.terminal)

        UiHandlers.setCurrentProject()
        UiHandlers.populate_pois_in_poi()

        self.setup_project_listeners()
        self.setup_plugin_listeners()
        self.setup_poi_listeners()
        self.setup_analysis_listeners()
        self.setup_documentation_listeners()

        QtCore.QMetaObject.connectSlotsByName(BEAT)
        
    def setup_project_listeners(self):
        self.new_project_button.clicked.connect(UiHandlers.new_project)
        # calls remove_project if delete_project_button is clicked
        self.delete_project_button.clicked.connect(UiHandlers.project_deletion_message)
        # calls save_project if save_project_button is clicked
        self.save_project_button.clicked.connect(UiHandlers.save_project)
        # calls browse_path if file_browse_button is clicked
        self.file_browse_button.clicked.connect(UiHandlers.browse_path)
        # self.delete_project_button.connect(self.delete_current_project)
        self.project_list.itemClicked.connect(UiHandlers.project_selected)

    def setup_plugin_listeners(self):
        # calls save_plugin if detailed_plugin_view_save_button is clicked
        self.detailed_plugin_view_save_button.clicked.connect(UiHandlers.save_plugin)
        # calls remove_plugin  if detailed_plugin_view_delete_button is clicked
        self.detailed_plugin_view_delete_button.clicked.connect(UiHandlers.remove_plugin)
        # calls browse_plugin_structure if plugin_structure_browse_button is clicked
        self.plugin_structure_browse_button.clicked.connect(UiHandlers.browse_plugin_structure)
        # calls browse_plugin_dataset if plugin_predefined_data_set_browse_button is clicked
        self.plugin_predefined_data_set_browse_button.clicked.connect(UiHandlers.browse_plugin_dataset)
        self.plugin_view_plugin_listwidget.itemClicked.connect(UiHandlers.populate_pois_in_plugin)
        self.plugin_view_plugin_listwidget.itemClicked.connect(UiHandlers.populate_name_and_description)

        #Allows you to create a new plugin
        self.plugin_view_new_button.clicked.connect(UiHandlers.new_plugin)

    def setup_poi_listeners(self):
        self.detailed_point_of_interest_view_type_dropdown.clear()
        self.detailed_point_of_interest_view_type_dropdown.addItems(["Function","String", "Variable", "DLL"])
        self.detailed_point_of_interest_view_type_dropdown.currentIndexChanged.connect(UiHandlers.poi_type_changed_in_poi)
        self.detailed_point_of_interest_view_save_button.clicked.connect(UiHandlers.save_poi)

        self.detailed_point_of_interest_view_existing_plugin_dropdown.currentIndexChanged.connect(UiHandlers.change_plugin_in_poi)

        self.detailed_point_of_interest_view_delete_button.clicked.connect(UiHandlers.delete_poi)

        self.point_of_interest_view_listwidget.itemClicked.connect(UiHandlers.poi_in_poitab_selected)


    def setup_documentation_listeners(self):
        self.document_view_listwidget.clear()
        self.document_view_listwidget.addItems(['README', 'BEAT Documentation', 'XML Structures', 'Tab Guide'])
        self.point_of_interest_view_search_button.clicked.connect(UiHandlers.search_POI_View)
        self.point_of_interest_view_search_lineedit.returnPressed.connect(UiHandlers.search_POI_View)
        self.document_view_listwidget.itemClicked.connect(UiHandlers.change_doc)
        # searches Project in the left column
        self.project_view_search_button.clicked.connect(UiHandlers.search_Project)
        self.project_search_lineedit.returnPressed.connect(UiHandlers.search_Project)
        # searches Plugin in the left column
        self.plugin_view_search_button.clicked.connect(UiHandlers.search_Plugin)
        self.plugin_view_search_lineedit.returnPressed.connect(UiHandlers.search_Plugin)
        # searches POI View in the left column
        self.point_of_interest_view_search_button.clicked.connect(UiHandlers.search_POI_View)
        self.point_of_interest_view_search_lineedit.returnPressed.connect(UiHandlers.search_POI_View)
        # searches Document in the left column
        self.document_view_search_button.clicked.connect(UiHandlers.search_Document)
        self.document_view_search_lineedit.returnPressed.connect(UiHandlers.search_Document)

    def setup_analysis_listeners(self):
        # calls analysis_result aft er analysis_result_button is clicked
        self.analysis_result_button.clicked.connect(UiHandlers.analysis_result)
        # calls comment_view after comment_button is clicked
        self.comment_button.clicked.connect(UiHandlers.comment_view)

        self.run_button.clicked.connect(UiHandlers.run_command_from_cmd)
                # run static analysis and check which POI to display
        self.static_run_button.clicked.connect(UiHandlers.analyze_and_display_POI)
        # searches POI in the left column
        self.points_of_interest_search_button.clicked.connect(UiHandlers.search_POI)
        self.points_of_interest_line_edit.returnPressed.connect(UiHandlers.search_POI)
        # listens to changes in POI dropdown
        self.type_dropdown.currentIndexChanged.connect(UiHandlers.change_displayed_POI)
        self.type_dropdown.clear()
        self.type_dropdown.addItem("All")
        self.type_dropdown.addItem("Function Call")
        self.type_dropdown.addItem("Variables")
        self.type_dropdown.addItem("Strings")
        self.dynamic_run_button.clicked.connect(UiHandlers.display_dynamic_info)
        self.points_of_interest_list_widget.itemClicked.connect(UiHandlers.match_selected_POI)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    BEAT = QtWidgets.QGroupBox()
    ui = UiMain()
    ui.setupUi(BEAT)
    BEAT.show()
    sys.exit(app.exec_())