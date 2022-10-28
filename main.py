"""
Main module  - should actually be run
"""
import sys
from PySide6 import QtWidgets
from GUITools.gui_file import SMSTexterWidget

if __name__ == "__main__":
    if __name__ == "__main__":
        app = QtWidgets.QApplication([])
        widget = SMSTexterWidget()
        widget.resize(800, 600)
        widget.show()
        sys.exit(app.exec())

