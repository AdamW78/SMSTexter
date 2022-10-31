from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from GUITools.central_widget import SMSTexterWidget


class TexterWindow(QMainWindow):

    def __init__(self):
        """
        Constructor for main window
        """
        super(TexterWindow, self).__init__()
        widget = SMSTexterWidget()
        self.setCentralWidget(widget)
