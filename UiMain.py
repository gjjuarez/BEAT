from PyQt5 import QtCore, QtGui, QtWidgets

import UiView


from Figure10OutputFieldView import Ui_Figure10OutputFieldView
from Figure11CommentView import Ui_Figure11CommentView
from Figure12AnalysisResultReview import Ui_Figure12AnalysisResultReview

class UiMain(UiView.Ui_BEAT):
    def setupUi(self, BEAT):
        super().setupUi(BEAT)
        print("hi")

        #QtCore.QMetaObject.connectSlotsByName(MainWindow)

    #########################################################################################
    # Project Tab Functions
    #########################################################################################

  

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    BEAT = QtWidgets.QGroupBox()
    ui = UiMain()
    #UiView.dynamic_run_button.setDisabled(True)
    #UiView.dynamic_stop_button.setDisabled(True)
    ui.setupUi(BEAT)
    BEAT.show()
    sys.exit(app.exec_())
