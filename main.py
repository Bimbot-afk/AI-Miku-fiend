from PySide6 import QtCore
import sys
from PySide6.QtWidgets import (QApplication)
from UI.MainWindow import MainWindow
import UI.timmer_app # IMPORTANTE: Se importa aquí para inicializar el timer en el Hilo Principal
import tools.files_watcher # IMPORTANTE: Se importa para inicializar señales de popups en Hilo Principal
import tools.files_watcher as flw


if __name__ == "__main__":
    flw.files_watcher_main()
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()