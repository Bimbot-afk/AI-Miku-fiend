import sys
import os
import traceback

def handle_exception(exc_type, exc_value, exc_traceback):
    error_msg = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
    try:
        with open("crash_log.txt", "a") as f:
            f.write(error_msg + "\n")
        import ctypes
        ctypes.windll.user32.MessageBoxW(0, f"Error fatal detectado. Por favor envia esto al desarrollador:\n\n{error_msg}", "Error MikuFriend", 0x10)
    except:
        pass
    sys.exit(1)

sys.excepthook = handle_exception

from PySide6 import QtCore
from PySide6.QtWidgets import (QApplication)
from UI.MainWindow import MainWindow
from UI.first_app_screen import FirstAppScreen
import UI.timmer_app # IMPORTANTE: Se importa aquí para inicializar el timer en el Hilo Principal
import tools.files_watcher # IMPORTANTE: Se importa para inicializar señales de popups en Hilo Principal
import tools.files_watcher as flw
import os
from dotenv import load_dotenv

def get_env_path():
    if getattr(sys, 'frozen', False):
        return os.path.join(sys._MEIPASS, ".env")
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")

load_dotenv(get_env_path(), override=True)
window = None

def start_main_app():
    global window
    window = MainWindow()
    window.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Si ya hay API Key en el .env, asumimos que ya pasó el setup
    import os
    if os.getenv("api_key") and os.getenv("api_key").strip() != "":
        start_main_app()
    else:
        first_screen = FirstAppScreen(start_main_app)
        first_screen.show()
    
    app.exec()