import os
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QProgressBar, QMessageBox, QFormLayout
)
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QIcon
from core.miku_config_manager import load_soul_data, save_soul_data
import tools.files_watcher as flw
from dotenv import load_dotenv

class WorkerThread(QThread):
    finished = Signal()

    def run(self):
        flw.files_watcher_main()
        self.finished.emit()

class FirstAppScreen(QWidget):
    def __init__(self, main_window_callback):
        super().__init__()
        self.main_window_callback = main_window_callback
        self.setWindowTitle("Configuración Inicial - Miku Friend")
        # Ensure path uses relative paths or robust paths
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        icon_path = os.path.join(base_dir, "assets", "Miku1", "m2", "NoOutline", "Pngs", "m2UpScale.png")
        self.setWindowIcon(QIcon(icon_path))
        self.resize(450, 300)
        self.setStyleSheet("""
            QWidget { background-color: #121516; color: #e6eceb; font-family: 'Segoe UI', Arial; }
            QLineEdit { background-color: #1e2324; border: 1px solid #39c5bb; padding: 5px; border-radius: 4px; }
            QPushButton { background-color: #39c5bb; color: #121516; padding: 8px; border-radius: 4px; font-weight: bold; }
            QPushButton:hover { background-color: #4ad6cc; }
            QProgressBar { border: 1px solid #39c5bb; border-radius: 4px; text-align: center; color: white; }
            QProgressBar::chunk { background-color: #39c5bb; }
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)

        title = QLabel("Bienvenido a Miku Friend")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #39c5bb; margin-bottom: 15px;")
        layout.addWidget(title)

        form_layout = QFormLayout()
        form_layout.setSpacing(10)

        # Cargar valores actuales
        soul_data = load_soul_data()
        current_idiom = soul_data.get("idiom", "Español")

        load_dotenv()
        current_api = os.getenv("api_key", "")
        current_url = os.getenv("url_api_key", "https://openrouter.ai/api/v1")

        self.input_idiom = QLineEdit(current_idiom)
        self.input_api = QLineEdit(current_api)
        self.input_api.setEchoMode(QLineEdit.Password)  # Ocultar API Key si el usuario prefiere
        self.input_url = QLineEdit(current_url)

        form_layout.addRow(QLabel("Idioma:"), self.input_idiom)
        form_layout.addRow(QLabel("API Key:"), self.input_api)
        form_layout.addRow(QLabel("URL (Opcional):"), self.input_url)

        layout.addLayout(form_layout)

        self.start_button = QPushButton("Iniciar Miku Friend")
        self.start_button.clicked.connect(self.on_start)
        layout.addWidget(self.start_button)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0) # Indeterminate progress bar
        self.progress_bar.hide()
        layout.addWidget(self.progress_bar)
        
        self.status_label = QLabel("Revisando archivos...")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.hide()
        layout.addWidget(self.status_label)

        self.setLayout(layout)

    def on_start(self):
        idiom = self.input_idiom.text().strip()
        api_key = self.input_api.text().strip()
        url = self.input_url.text().strip()
        
        if not api_key:
            QMessageBox.warning(self, "Advertencia", "Por favor ingresa tu API Key.")
            return

        # Guardar idioma
        soul_data = load_soul_data()
        soul_data["idiom"] = idiom
        save_soul_data(soul_data)

        import sys
        if getattr(sys, 'frozen', False):
            env_path = os.path.join(sys._MEIPASS, ".env")
        else:
            env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")
        with open(env_path, "w", encoding="utf-8") as f:
            f.write(f"api_key={api_key}\n")
            f.write(f"url_api_key={url}\n")

        os.environ["api_key"] = api_key
        os.environ["url_api_key"] = url

        # Ocultar inputs y mostrar barra
        self.start_button.hide()
        self.input_idiom.setDisabled(True)
        self.input_api.setDisabled(True)
        self.input_url.setDisabled(True)
        
        self.progress_bar.show()
        self.status_label.show()

        # Iniciar thread para fileswatcher
        self.worker = WorkerThread()
        self.worker.finished.connect(self.on_worker_finished)
        self.worker.start()

    def on_worker_finished(self):
        self.close()
        self.main_window_callback()
