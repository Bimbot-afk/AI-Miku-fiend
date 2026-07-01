from PySide6.QtGui import QIcon
from core.brain import consultar_miku
from PySide6.QtWidgets import (QMainWindow, QPushButton, QWidget, QVBoxLayout, QLabel, QTextEdit, QLineEdit, QHBoxLayout)
from PySide6.QtCore import (Qt, QTimer)
import ctypes

ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("miku_friend")

class ChatbotWindowMiku(QMainWindow):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle("Miku Friend Chat")
        self.setWindowIcon(QIcon("C:/Users/emar0/Desktop/Proyectos/miku_friend/assets/Miku1/m2/NoOutline/Pngs/m2UpScale.png"))
        self.setGeometry(100, 100, 300, 500)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.miku_thinking = False

        # Central Widget since QMainWindow requires a central widget for layouts
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # Create main layout on central widget
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setContentsMargins(12, 12, 12, 12)
        self.layout.setSpacing(10)

        # Chat History Log
        self.chat_history = QTextEdit()
        self.chat_history.setReadOnly(True)
        self.layout.addWidget(self.chat_history)

        # Etiqueta de estado para animaciones de carga
        self.status_label = QLabel("")
        self.status_label.setStyleSheet("color: #888888; font-style: italic; font-size: 11px;")
        self.layout.addWidget(self.status_label)

        # Input and Send layout
        self.input_layout = QHBoxLayout()
        self.input_layout.setSpacing(8)
        
        # Create Line Edit for User Input
        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Text Miku here...")
        self.user_input.returnPressed.connect(self.send_message)
        self.input_layout.addWidget(self.user_input)

        # Create Send Button
        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self.send_message)
        self.input_layout.addWidget(self.send_button)

        #create restart button
        self.restart_button = QPushButton("Restart")
        self.restart_button.clicked.connect(self.restart_chat)
        self.input_layout.addWidget(self.restart_button)
        
        self.layout.addLayout(self.input_layout)

        # Inicializar el historial de conversación
        self.message_history = []
        self.long_term_memory = []
        self.active_workers = []

        # Timer para animación de carga ("Miku is thinking...")
        self.thinking_timer = QTimer(self)
        self.thinking_timer.timeout.connect(self.update_thinking_dots)
        self.thinking_dots_count = 0

        # Apply Hatsune Miku visual design system stylesheet
        self.apply_miku_stylesheet()

    def apply_miku_stylesheet(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #121516; /* Miku Cyber Dark Base */
            }
            QWidget {
                background-color: #121516;
                color: #e6eceb; /* Soft cyber white */
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 13px;
            }
            QTextEdit {
                background-color: #1a1d1f; /* Dark Panel Background */
                border: 2px solid #252e32;
                border-radius: 8px;
                padding: 8px;
                color: #e6eceb;
            }
            QLineEdit {
                background-color: #1a1d1f;
                border: 2px solid #252e32;
                border-radius: 6px;
                padding: 6px;
                color: #e6eceb;
            }
            QLineEdit:focus {
                border: 2px solid #39c5bb; /* Hatsune Miku Teal Border */
            }
            QPushButton {
                background-color: #39c5bb; /* Miku Signature Teal Button */
                color: #121516;
                border: none;
                border-radius: 6px;
                padding: 6px 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #4ee0d6;
            }
            QPushButton:pressed {
                background-color: #2da199;
            }
            QScrollBar:vertical {
                border: none;
                background: #1a1d1f;
                width: 8px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #2b3337;
                min-height: 20px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical:hover {
                background: #39c5bb;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }
        """)

    def restart_chat(self):
        self.thinking_timer.stop()
        self.status_label.setText("")
        for worker in self.active_workers:
            if worker.isRunning():
                worker.quit()
                worker.wait(1000)
        self.active_workers.clear()
        self.message_history = []
        self.long_term_memory = []
        self.chat_history.clear()
        self.chat_history.append('<p style="color: grey;">Chat restarted</p>')
        self.send_button.setEnabled(True)
        self.send_button.setStyleSheet("background-color: #39c5bb;")
        self.user_input.setEnabled(True)
        self.user_input.clear()

    def send_message(self):
        user_message = self.user_input.text().strip()
        if user_message:
            if not hasattr(self, 'weather_fetched'):
                self.weather_fetched = True
                import threading
                from tools.get_weather import get_weather
                threading.Thread(target=get_weather, daemon=True).start()

            # Custom styled HTML for user message using Miku Teal
            user_html = f'<p style="margin: 4px 0;"><b style="color: #FF1493;">You:</b> {user_message}</p>'
            self.user_input.clear()
            self.chat_history.append(user_html)
            
            # Guardar el mensaje en el historial
            self.message_history.append({'role': 'user', 'content': user_message})
                
            self.display_miku_response()

    def display_miku_response(self):
        self.send_button.setEnabled(False)
        self.user_input.setEnabled(True)
        self.send_button.setStyleSheet("background-color: gray;")
        
        # Iniciar animación de carga en la etiqueta de estado
        self.status_label.setText("Miku is thinking.")
        self.thinking_dots_count = 1
        self.thinking_timer.start(500) # Se actualiza cada 500ms
        
        # Iniciar el hilo pasando todo el historial y la memoria a largo plazo
        worker = consultar_miku(self.message_history, self.long_term_memory)
        self.active_workers.append(worker)
        
        # Obtener o instanciar la ventana de configuración en segundo plano si es necesario
        config_window = self.main_window.config_window
        if config_window is None:
            from UI.configuration import configurationMiku
            config_window = configurationMiku(self.main_window)
            self.main_window.config_window = config_window
            
        # Cargar la configuración en el hilo y conectar señales
        worker.miku_config()
        if self.main_window.cmd_window is not None:
            worker.log_signal.connect(self.main_window.cmd_window.append_log)
        worker.finished_response.connect(self.on_response_received)
        worker.finished.connect(lambda: self.cleanup_worker(worker))
        worker.start()


    def on_response_received(self, response):
        self.thinking_timer.stop()
        self.status_label.setText("")

        # mostrar error si no hay api/url
        if response == "error":
            self.chat_history.append('<p style="color: red;">Error: API_KEY o Server URL no encontrado</p>')
            self.send_button.setEnabled(True)
            self.user_input.setEnabled(True)
            self.send_button.setStyleSheet("background-color: #39c5bb;")
            return
        
        # Guardar la respuesta en el historial
        self.message_history.append({'role': 'assistant', 'content': response})
        
        miku_html = f'<p style="margin: 4px 0;"><b style="color: #39c5bb;">Miku:</b> {response}</p>'
        self.chat_history.append(miku_html)
        self.send_button.setEnabled(True)
        self.user_input.setEnabled(True)
        self.send_button.setStyleSheet("background-color: #39c5bb;")

    def update_thinking_dots(self):
        self.thinking_dots_count = (self.thinking_dots_count % 3) + 1
        dots = "." * self.thinking_dots_count
        self.status_label.setText(f"Miku is thinking{dots}")

    def cleanup_worker(self, worker):
        if worker in self.active_workers:
            self.active_workers.remove(worker)

    def closeEvent(self, event):
        self.thinking_timer.stop()
        for worker in self.active_workers:
            if worker.isRunning():
                worker.quit()
                worker.wait(1000)
        self.active_workers.clear()
        event.accept()

