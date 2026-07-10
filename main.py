from PySide6 import QtCore
import sys
from PySide6.QtWidgets import (QApplication)
from UI.MainWindow import MainWindow
from UI.first_app_screen import FirstAppScreen
import UI.timmer_app # IMPORTANTE: Se importa aquí para inicializar el timer en el Hilo Principal
import tools.files_watcher # IMPORTANTE: Se importa para inicializar señales de popups en Hilo Principal
import tools.files_watcher as flw
from dotenv import load_dotenv

load_dotenv()
window = None

def start_main_app():
    global window
    window = MainWindow()
    window.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    first_screen = FirstAppScreen(start_main_app)
    first_screen.show()
    
    app.exec()