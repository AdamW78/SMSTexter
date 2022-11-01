"""
Main window module for texting GUI
"""
from PySide6 import QtCore, QtWidgets
from schedule import every, cancel_job

import constants
from GUITools.NumberInput import number_reader
from GUITools.NumberInput.left_input_widget import LeftInputWidget
from GUITools.TextMessageInput import TextMessageInput
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
        self.status_output = QtWidgets.QLabel("Waiting to send text...")
        # Create main layout object
        self.layout = QtWidgets.QGridLayout(self)
        self.layout.addWidget(self.button, 1, 1)
        # Create widget used for obtaining target phone number input
        self.input_widget = LeftInputWidget()
        self.layout.addWidget(self.input_widget, 0, 0)
        # Connect text send button to actual text send method
        self.button.clicked.connect(self.send_text)
        # Create fields to be used when texts are sent for memory re-usage
        self.sms_texter_single = None
        self.sms_texter_multi = None
        self.text_input = TextMessageInput()
        self.layout.addWidget(self.text_input, 0, 1)
        self.layout.addWidget(self.status_output, 2, 0)
        self.status_output.setGeometry(100, 100, 100, 100)

    @QtCore.Slot()
    def send_text(self):
        """
        Method run when user clicks "SEND"

        :return:
        """
        mode = self.input_widget.get_cur_mode()
        # Check if radio button 1 is checked
        if mode == 0:
            self.status_output.setText("Sending text to one phone number: "
                                       + constants.PHONE_NUMBER + "...")
            # Check if we have NOT already instantiated a single-number SMSTexter object
            # OR if the SMSTexter we instantiated does NOT have the phone number currently entered
            if self.sms_texter_single is None or \
                    self.sms_texter_single.phone_number() != constants.PHONE_NUMBER:
                # We have not created a single-number SMSTexter object OR it is out-of-date
                # Update field with new one now
                self.sms_texter_single = SMSTexter(constants.PHONE_NUMBER)
            # We have an up-to-date single-number SMSTexter, call send_message()
            self.sms_texter_single.send_message()
            self.status_output.setText("Text sent successfully to " + constants.PHONE_NUMBER + "!")
        # Radio button 2 is checked, multiple texts will be sent
        else:
            self.status_output.setText("Texting all numbers listed in supplied file...")
            # Check if we have NOT already instantiated a multi-number SMSTexter object
            # OR if the multi-number SMSTexter that already exists is out-of-date
            num_list = number_reader.read(constants.PHONE_NUMBERS_PATH)
            if self.sms_texter_multi is None or self.sms_texter_multi.phone_number() == num_list:
                # We have not created a multi-number SMSTexter or it is out-of-date
                # Update field with new one now
                self.sms_texter_multi = SMSTexter(num_list)
            # We have an up-to-date multi-number SMSTexter, call send_message()
            self.sms_texter_multi.send_message()
            self.status_output.setText("Text sent successfully to all numbers in supplied file!")
