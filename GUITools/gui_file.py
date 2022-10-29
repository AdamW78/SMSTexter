import random
import sys

from PySide6 import QtCore, QtWidgets

import constants
from GUITools.NumberInput.drag_button import DragButton
from sms_texter import SMSTexter


class SMSTexterWidget(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.poop = False
        self.fag = ""
        self.setWindowTitle("AW Development SMS Texter")
        self.button = QtWidgets.QPushButton("Click to send automated text")
        self.radio_button_1 = QtWidgets.QRadioButton("Single number")
        self.radio_button_1.setChecked(True)
        self.radio_button_2 = QtWidgets.QRadioButton("Multiple numbers")
        self.input_number = QtWidgets.QLineEdit()
        self.input_number.textChanged[str].connect(self.onChanged)
        self.input_number.setPlaceholderText("Enter phone number.")
        self.input_file = DragButton(self)
        self.input_file.textChanged[str].connect(self.onPathChange)
        self.input_file.setPlaceholderText("Drag your file here!")
        self.layout = QtWidgets.QGridLayout(self)
        self.layout.addWidget(self.radio_button_1, 0, 0)
        self.layout.addWidget(self.input_number, 0, 1)
        self.layout.addWidget(self.radio_button_2, 1, 0)
        self.layout.addWidget(self.input_file, 1, 1)
        self.layout.addWidget(self.button)
        self.input_file.hide()
        self.button.clicked.connect(self.magic)
        self.radio_button_1.toggled.connect(self.show_hide)
        self.radio_button_2.toggled.connect(self.show_hide_alt)

    @QtCore.Slot()
    def magic(self):
        if self.poop:
            print(self.fag)
            texter = SMSTexter(self.fag)
        else:
            texter = SMSTexter(constants.PHONE_NUMBER)
        texter.send_message()

    @QtCore.Slot()
    def show_hide(self):
        self.input_number.show()
        self.input_file.hide()
        self.poop = False

    @QtCore.Slot()
    def show_hide_alt(self):
        self.input_file.show()
        self.input_number.hide()
        self.poop = True

    @QtCore.Slot()
    def onChanged(self, text):
        constants.PHONE_NUMBER = text

    @QtCore.Slot()
    def onPathChange(self, text):
        self.fag = text
