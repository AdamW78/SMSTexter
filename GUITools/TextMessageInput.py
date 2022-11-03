from PySide6 import QtCore
from PySide6.QtWidgets import *
from PySide6.QtCore import *

import constants


class TextMessageInput(QWidget):

    def __init__(self, status_output: QLabel, variables: QGroupBox):
        """

        """
        super(TextMessageInput, self).__init__()
        self.num_vars = 0
        self.status_output = status_output
        self.variables = variables
        self.var_objs = []
        self.layout = QVBoxLayout(self)
        self.label = QLabel("Text Message")
        self.plain_text_input = QPlainTextEdit()
        self.plain_text_input.setPlaceholderText("Hello world!")
        self.plain_text_input.textChanged.connect(self.onTextChange)
        self.layout.addWidget(self.label, 0)
        self.layout.addWidget(self.plain_text_input, 1)

    @QtCore.Slot()
    def onTextChange(self):
        # Store current text from plaintext input and from output QLabel
        cur_text = self.plain_text_input.toPlainText()
        constants.MESSAGE = cur_text
        # Iterate through every variable object to make sure it still exists in the text input
        for obj in self.var_objs:
            if cur_text.find("{"+obj.text()+"}") == -1:
                # It does not still exist - hide, remove from var_objs, decrement num_vars
                # Check if num_vars is now 0 - if yes, hide variables QGroupBox
                obj.hide()
                self.num_vars -= 1
                self.var_objs.remove(obj)
                if self.num_vars == 0:
                    self.variables.hide()
        status_output_text = self.status_output.text()
        # Get number of characters "{" and "}", respectively
        left_b = cur_text.count("{")
        right_b = cur_text.count("}")
        # Check if the message contains either a "{" or a "}"
        if left_b != 0 or right_b != 0:
            # Message contains either a "{" or a "}"
            # Check if the number of right brackets does not equal num of left brackets
            if right_b != left_b:
                # Numbers do not match, warn user on-screen
                self.status_output.setText("Warning: unmatched \"{\" or \"}\"!")
            # Number of left and right brackets match
            else:
                # Check if currently being warned about unmatching "{" and "}"
                if status_output_text == "Warning: unmatched \"{\" or \"}\"!":
                    # Change the warning text back to normal
                    self.status_output.setText("Waiting to send text...")
                # Check if the self.variables QGroupBox is hidden
                if self.variables.isHidden():
                    # Show the self.variables QGroupBox
                    self.variables.show()
                # Number of left brackets is the number of variables to use
                self.num_vars = left_b
                # Iterate through each set of braces
                for i in range(self.num_vars):
                    # Split text at first left brace
                    text_list_prelim = cur_text.split("{", 1)
                    # Split text at first right brace
                    text_list = text_list_prelim[1].split("}", 1)
                    # Store text in-between braces - this is the variable name
                    var_name = text_list[0]
                    # Create empty list literal named existing_vars
                    existing_vars = []
                    # For each variable object in the variable display
                    for var in self.var_objs:
                        # Fetch the variable object's text and append it to existing_vars
                        existing_vars.append(var.text())
                    # Update the value cur_text to include everything past the
                    # user-defined variable
                    cur_text = text_list[1]
                    # Check if our current found variable is in existing_vars
                    if var_name not in existing_vars:
                        # It is not in existing_vars
                        # Create a variable QLabel with the var_name text as the name
                        label = QLabel(var_name)
                        # Add the newly created QLabel to the var_objs list for tracking
                        self.var_objs.append(label)
                        # Add the newly created QLabel to the QGroupBox self.variables
                        # layout at the position current index in range(self.num_vars)
                        self.variables.layout().addWidget(label, i)
        # The message contains neither a right curly brace nor a left curly brace
        else:
            # Check if self.variables QGroupBox is NOT hidden
            if not self.variables.isHidden():
                # Hide the self.variables QGroupBox
                self.variables.hide()
            # Check if the user is currently being warned about unmatching "{" and "}"
            # or if the user has a message warning about a failed text send
            if status_output_text == "Warning: unmatched \"{\" or \"}\"!" \
                    or status_output_text == "Error: Unmatched \"{\" or \"}\"! Text not sent!":
                self.status_output.setText("Waiting to send text...")

    @property
    def get_num_vars(self):
        return self.num_vars
