from PySide6 import QtCore
from PySide6.QtWidgets import *
from PySide6.QtCore import *

import constants


class TextMessageInput(QWidget):

    def __init__(self):
        """

        """
        super(TextMessageInput, self).__init__()
        self.layout = QVBoxLayout(self)
        self.label = QLabel("Text Message")
        self.plain_text_input = QPlainTextEdit()
        self.plain_text_input.setPlaceholderText("Hello world!")
        self.plain_text_input.textChanged.connect(self.onTextChange)
        self.layout.addWidget(self.label, 0)
        self.layout.addWidget(self.plain_text_input, 1)

    @QtCore.Slot()
    def onTextChange(self):
        constants.MESSAGE = self.plain_text_input.toPlainText()

