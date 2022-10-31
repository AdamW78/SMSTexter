from PySide6 import QtWidgets, QtCore

import constants
from GUITools.NumberInput.drag_line_edit import DragLineEdit


class MultiNumWidget(QtWidgets.QWidget):

    def __init__(self):
        super(MultiNumWidget, self).__init__()
        # Create combo box for file input
        self.layout = QtWidgets.QHBoxLayout(self)
        self.file_dialog = QtWidgets.QFileDialog()
        self.numbers_path_edit = DragLineEdit()
        self.browse_button = QtWidgets.QPushButton("Browse...")
        self.browse_button.clicked.connect(self.open_file_dialog)
        self.layout.addWidget(self.numbers_path_edit, 0)
        self.layout.addWidget(self.browse_button, 0.5)

    @QtCore.Slot()
    def open_file_dialog(self):
        self.file_dialog.show()
        if self.file_dialog.exec_():
            fileNames = self.file_dialog.selectedFiles()
            self.numbers_path_edit.setText(fileNames[0])
            constants.PHONE_NUMBERS_PATH = fileNames[0]




