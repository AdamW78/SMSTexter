from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *


class DragLineEdit(QLineEdit):
    # constructor
    def __init__(self):
        super().__init__()
        self.setPlaceholderText("Path to phone numbers...")
        # enabling accept drops
        self.setAcceptDrops(True)

    # creating drag enter event to receive text
    def dragEnterEvent(self, e):

        # checking format of the text
        if e.mimeData().hasFormat('text / plain'):
            # accepting the text
            e.accept()

        else:
            # rejecting the text
            e.ignore()

    # drop event to showing the text to label
    def dropEvent(self, e):

        # setting text to the label
        self.setText(e.mimeData().text())