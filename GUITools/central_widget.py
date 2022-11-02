"""
Main window module for texting GUI
"""
from PySide6 import QtCore, QtWidgets
from PySide6.QtWidgets import QVBoxLayout
from schedule import every, cancel_job

import constants
from GUITools.NumberInput import number_reader
from GUITools.NumberInput.left_input_widget import LeftInputWidget
from GUITools.TextMessageInput import TextMessageInput
from TwilioText import create_message
from sms_texter import SMSTexter


class SMSTexterWidget(QtWidgets.QWidget):

    def __init__(self):
        """
        Method called on instantiation of SMSTexterWidget
        """
        # Call parent constructor
        super().__init__()
        self.text_mode = 0
        # Set the window title
        self.setWindowTitle("AW Development SMS Texter")
        # Create text send button
        self.radio_buttons_2 = self.radio_button_setup("Text from Email", "Text from Number")
        self.button = QtWidgets.QPushButton("Click to send automated text")
        self.status_output = QtWidgets.QLabel("Waiting to send text...")
        self.radio_buttons_1 = LeftInputWidget(self.status_output)
        self.variables = QtWidgets.QGroupBox("Variables")
        self.variables.setLayout(QVBoxLayout(self.variables))
        # Create main layout object
        self.layout = QtWidgets.QGridLayout(self)
        # Create widget used for obtaining target phone number input
        # Connect text send button to actual text send method
        self.button.clicked.connect(self.send_text)
        # Create fields to be used when texts are sent for memory re-usage
        self.sms_texter_single = None
        self.sms_texter_multi = None
        self.text_input = TextMessageInput(self.status_output, self.variables)
        if self.text_input.get_num_vars == 0:
            self.variables.hide()
        # Add widgets to layout
        self.layout.addWidget(self.button, 3, 1)
        self.layout.addWidget(self.text_input, 1, 1)
        self.layout.addWidget(self.variables, 2, 1)
        self.layout.addWidget(self.status_output, 3, 0)
        self.layout.addWidget(self.radio_buttons_1, 0, 0, 2, 1)
        self.layout.addWidget(self.radio_buttons_2, 0, 1)
        self.status_output.setGeometry(100, 100, 100, 100)

    @QtCore.Slot()
    def send_text(self):
        """
        Method run when user clicks "SEND"

        :return:
        """
        phone_number = constants.PHONE_NUMBER
        message = constants.MESSAGE
        if self.status_output.text() == "Warning: unmatched \"{\" or \"}\"!" \
                or self.status_output.text() == "Error: Unmatched \"{\" or \"}\"! Text not sent!":
            self.status_output.setText("Error: Unmatched \"{\" or \"}\"! Text not sent!")
            return

        # Get mode from radio_buttons_1 QGroupBox - Single-number or multi-number
        mode = self.radio_buttons_1.get_cur_mode()
        # Check if send text using Twilio radio button is enabled
        if self.text_mode == 1:
            # Sending text to single number using Twilio phone number as sender
            if mode == 0:
                self.send_text_twilio(phone_number, message)
            # SEnding text to multiple numbers using Twilio phone number as sender
            else:
                self.status_output.setText("Texting all numbers listed in supplied file...")
                for num in number_reader.read(constants.PHONE_NUMBERS_PATH):
                    if len(num) == 1:
                        self.send_text_twilio(num[0], message)
                    # Fetch message from constant
                    else:
                        user_vars = []
                        for i in range(len(num)):
                            i = int(i)
                            if i == 0:
                                continue
                            user_vars.append(num[i])
                        self.send_text_twilio(num[0], self.format_message(message, user_vars))
        elif mode == 0:
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

    def send_text_twilio(self, phone_number: str, text: str):
        self.status_output.setText("Sending text to one phone number: "
                                   + constants.PHONE_NUMBER + "...")
        create_message.text(phone_number, text)
        self.status_output.setText("Text sent successfully to " + constants.PHONE_NUMBER + "!")

    def radio_button_setup(self, button_1: str, button_2: str):
        """
        Method for set up of radio buttons in main window
        :return:
        """
        # Create radio buttons widget
        radio_buttons = QtWidgets.QGroupBox("Sender")
        radio_buttons.layout = QtWidgets.QHBoxLayout(radio_buttons)
        radio_button_1 = QtWidgets.QRadioButton(button_1)
        radio_button_1.setChecked(True)
        radio_button_2 = QtWidgets.QRadioButton(button_2)
        radio_button_1.toggled.connect(self.set_mode_1)
        radio_button_2.toggled.connect(self.set_mode_2)
        radio_buttons.layout.addWidget(radio_button_1, 0)
        radio_buttons.layout.addWidget(radio_button_2, 1)
        return radio_buttons

    @staticmethod
    def format_message(message: str, user_vars: list) -> str:
        """
        Message used for properly formatting text message with variable
        :param user_vars:
        :param message:
        :return:
        """
        for var in user_vars:
            if message.find("{") != -1:
                split_one = message.split("{", 1)
                split_two = split_one[1].split("}", 1)
                message = split_one[0] + var + split_two[1]
        return message

    @QtCore.Slot()
    def set_mode_1(self):
        self.text_mode = 0
        self.status_output.setText("Switched to email mode!")

    @QtCore.Slot()
    def set_mode_2(self):
        self.text_mode = 1
        self.status_output.setText("Switched to phone number mode!")
