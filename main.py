"""
Main module  - should actually be run
"""
import sys
from PySide6 import QtWidgets
from GUITools.main_window import TexterWindow

if __name__ == "__main__":
    if __name__ == "__main__":
        app = QtWidgets.QApplication([])
        main_window = TexterWindow()
        main_window.show()
        sys.exit(app.exec())

