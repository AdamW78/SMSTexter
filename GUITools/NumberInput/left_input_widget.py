from PySide6 import QtCore, QtWidgets

import constants
from GUITools.NumberInput.drag_line_edit import DragLineEdit
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
        self.radio_buttons = self.radio_button_setup()
        # Phone number input setup
        self.input_number = QtWidgets.QLineEdit()
        self.input_number.textChanged[str].connect(self.onChanged)
        self.input_number.setPlaceholderText("Enter phone number.")
        # File input setup
        # self.input_file = MultiNumWidget()
        # self.input_file.hide()
        self.file_dialog = QtWidgets.QFileDialog()
        self.numbers_path_edit = DragLineEdit()
        self.browse_button = QtWidgets.QPushButton("Browse...")
        self.browse_button.clicked.connect(self.open_file_dialog)
        self.numbers_path_edit.hide()
        self.browse_button.hide()
        self.layout.addWidget(self.numbers_path_edit, 1, 0)
        self.layout.addWidget(self.browse_button, 2, 0)
        # Add widgets to layout
        self.layout.addWidget(self.radio_buttons, 0, 0)
        self.layout.addWidget(self.input_number, 1, 0)
        #self.layout.addWidget(self.input_file, 1, 0)

    def radio_button_setup(self):
        """
        Method for set up of radio buttons in main window
        :return:
        """
        # Create radio buttons widget
        radio_buttons = QtWidgets.QWidget(self)
        radio_buttons.layout = QtWidgets.QHBoxLayout(radio_buttons)
        radio_button_1 = QtWidgets.QRadioButton("Single number")
        radio_button_1.setChecked(True)
        radio_button_2 = QtWidgets.QRadioButton("Multiple numbers")
        radio_button_1.toggled.connect(self.rb1_toggle)
        radio_button_2.toggled.connect(self.rb2_toggle)
        radio_buttons.layout.addWidget(radio_button_1, 0)
        radio_buttons.layout.addWidget(radio_button_2, 1)
        return radio_buttons

    @QtCore.Slot()
    def open_file_dialog(self):
        self.file_dialog.show()
        if self.file_dialog.exec_():
            fileNames = self.file_dialog.selectedFiles()
            self.numbers_path_edit.setText(fileNames[0])
            constants.PHONE_NUMBERS_PATH = fileNames[0]

    @QtCore.Slot()
    def rb1_toggle(self):
        """
        Method called when single-number radio button is toggled

        :return:
        """
        # Set mode to single phone number
        self.mode = 0
        self.input_number.show()
        self.numbers_path_edit.hide()
        self.browse_button.hide()

    @QtCore.Slot()
    def rb2_toggle(self):
        """
        Method called when multiple-number radio button is toggled

        :return:
        """
        self.mode = 1
        self.numbers_path_edit.show()
        self.browse_button.show()
        self.input_number.hide()

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
        if self.mode == 0:
            return constants.PHONE_NUMBER
        return constants.PHONE_NUMBERS_PATH
