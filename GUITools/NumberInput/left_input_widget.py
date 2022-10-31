from PySide6 import QtCore, QtWidgets

import constants
from GUITools.NumberInput.multi_num_widget import MultiNumWidget


class LeftInputWidget(QtWidgets.QWidget):

    def __init__(self):
        # Call parent constructor
        super(LeftInputWidget, self).__init__()
        """
        Method called on instantiation
        Adds everything to layout
        """
        self.layout = QtWidgets.QGridLayout(self)
        # Set up variables to check if texting one or more phone numbers
        self.mode = 0
        # Radio button setup
        self.radio_button_1 = QtWidgets.QRadioButton("Single number")
        self.radio_button_1.setChecked(True)
        self.radio_button_2 = QtWidgets.QRadioButton("Multiple numbers")
        # Phone number input setup
        self.input_number = QtWidgets.QLineEdit()
        self.input_number.textChanged[str].connect(self.onChanged)
        self.input_number.setPlaceholderText("Enter phone number.")
        # File input setup
        self.input_file = MultiNumWidget()
        # self.input_file.textChanged[str].connect(self.onPathChange)
        # self.input_file.setPlaceholderText("Drag your file here!")
        # self.input_file.hide()

        # Add widgets to layout
        self.layout.addWidget(self.radio_button_1, 0, 0)
        self.layout.addWidget(self.input_number, 0, 1)
        self.layout.addWidget(self.radio_button_2, 1, 0)
        self.layout.addWidget(self.input_file, 1, 1)
        self.radio_button_1.toggled.connect(self.rb1_toggle)
        self.radio_button_2.toggled.connect(self.rb2_toggle)

    @QtCore.Slot()
    def rb1_toggle(self):
        """
        Method called when single-number radio button is toggled

        :return:
        """
        # Set mode to single phone number
        self.mode = 0

    @QtCore.Slot()
    def rb2_toggle(self):
        """
        Method called when multiple-number radio button is toggled

        :return:
        """
        self.mode = 1

    @QtCore.Slot()
    def get_cur_mode(self):
        """
        Getter method for single or multi mode

        :return:
        """
        return self.mode

    @QtCore.Slot()
    def onChanged(self, text):
        """
        Method called when phone number input changes - updates constants.PHONE_NUMBER

        :param text: String phone number input text
        """
        constants.PHONE_NUMBER = text

    @QtCore.Slot()
    def onPathChange(self, text: str):
        """
        Method called when list file input changes - updates c

        :param text:
        :return:
        """
        constants.PHONE_NUMBERS_PATH = text

    @QtCore.Slot()
    def getCurNumPath(self) -> str:
        """
        Method used for returning current number or path
        
        :return: String single phone number or filepath
        """
        # Check if using single number
        if self.radio_button_1.isChecked():
            return constants.PHONE_NUMBER
        return constants.PHONE_NUMBERS_PATH
