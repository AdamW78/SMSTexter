from PySide6 import QtWidgets, QtCore

import constants
from GUITools.NumberInput.drag_line_edit import DragLineEdit


class MultiNumWidget(QtWidgets.QWidget):

    def __init__(self):
        super(MultiNumWidget, self).__init__()
        # Create combo box for file input
        self.layout = QtWidgets.QHBoxLayout(self)




