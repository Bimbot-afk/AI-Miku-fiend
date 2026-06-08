import sys
from PySide6.QtWidgets import (QApplication)
from UI.MainWindow import MainWindow
from dotenv import load_dotenv
import os

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
