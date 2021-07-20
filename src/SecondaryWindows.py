import sys
from PyQt5 import QtWidgets, QtGui, QtCore


class SaveDialog(QtWidgets.QDialog):

    def __init__(self):
        super().__init__()

    def dialog(self):
        super().__init__()
        path,filetype = QtWidgets.QFileDialog.getSaveFileName(self, "Save Animation", "",
                                                  "html (*.htm);;gif (*.gif);;mp4 (*.mp4)")
        if path:
            save_info = SaveInfo()
            confirmation = save_info.infoDialog()
            if confirmation:
                return path, filetype
            else:
                return False, False
        else:
            return False, False

class SaveInfo(QtWidgets.QMessageBox):

    def __init__(self):
        super().__init__()

    def infoDialog(self):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Information)
        cancel = msg.addButton(QtWidgets.QMessageBox.Cancel)
        continue_ = msg.addButton("Continue", QtWidgets.QMessageBox.ActionRole)
        msg.setText('<style>div {text-align: left; font-size: 15px; font-weight: normal;}</style> <div>Saving will take a few minutes</div>' )
        msg.setInformativeText("<style>div {text-align: justify;}</style><div>The main window will become<br>unresponsive during this time</div>")
        msg.setWindowTitle("This could take a while...")
        msg.exec()
        if msg.clickedButton() == continue_:
            return True
        else:
            return False


