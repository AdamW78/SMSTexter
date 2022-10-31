"""
Main window module for texting GUI
"""
from PySide6 import QtCore, QtWidgets

import constants
from GUITools.NumberInput import number_reader
from GUITools.NumberInput.left_input_widget import LeftInputWidget
from sms_texter import SMSTexter


class SMSTexterWidget(QtWidgets.QWidget):

    def __init__(self):
        """
        Method called on instantiation of SMSTexterWidget
        """
        # Call parent constructor
        super().__init__()
        # Set the window title
        self.setWindowTitle("AW Development SMS Texter")
        # Create text send button
        self.button = QtWidgets.QPushButton("Click to send automated text")
        # Create main layout object
        self.layout = QtWidgets.QGridLayout(self)
        self.layout.addWidget(self.button, 1, 0.5)
        # Create widget used for obtaining target phone number input
        self.input_widget = LeftInputWidget()
        self.layout.addWidget(self.input_widget, 0, 0)
        # Connect text send button to actual text send method
        self.button.clicked.connect(self.send_text)
        # Create fields to be used when texts are sent for memory re-usage
        self.sms_texter_single = None
        self.sms_texter_multi = None

    @QtCore.Slot()
    def send_text(self):
        """
        Method run when user clicks "SEND"

        :return:
        """
        cur_num_path = self.input_widget.getCurNumPath()
        mode = self.input_widget.get_cur_mode()
        # Check if radio button 1 is checked
        if mode == 0:
            # Check if we have NOT already instantiated a single-number SMSTexter object
            # OR if the SMSTexter we instantiated does NOT have the phone number currently entered
            if self.sms_texter_single is None or \
                    self.sms_texter_single.phone_number() != constants.PHONE_NUMBER:
                # We have not created a single-number SMSTexter object OR it is out-of-date
                # Update field with new one now
                self.sms_texter_single = SMSTexter(constants.PHONE_NUMBER)
            # We have an up-to-date single-number SMSTexter, call send_message()
            self.sms_texter_single.send_message()
        # Radio button 2 is checked, multiple texts will be sent
        else:
            # Check if we have NOT already instantiated a multi-number SMSTexter object
            # OR if the multi-number SMSTexter that already exists is out-of-date
            num_list = number_reader.read(constants.PHONE_NUMBERS_PATH)
            if self.sms_texter_multi is None or self.sms_texter_multi.phone_number() == num_list:
                # We have not created a multi-number SMSTexter or it is out-of-date
                # Update field with new one now
                self.sms_texter_multi = SMSTexter(num_list)
            # We have an up-to-date multi-number SMSTexter, call send_message()
            self.sms_texter_multi.send_message()
