import sys
from PySide6.QtWidgets import QApplication
from UI.MainWindow import MainWindow

app = QApplication(sys.argv)
try:
    window = MainWindow()
    from UI.configuration import configurationMiku
    conf = configurationMiku(window)
    print("Configuration window instantiated successfully!")
except Exception as e:
    import traceback
    traceback.print_exc()
