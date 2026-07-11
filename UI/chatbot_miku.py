from asyncio import timeouts
from PySide6.QtGui import QIcon
from core.brain import consultar_miku
from PySide6.QtWidgets import (QMainWindow, QPushButton, QWidget, QVBoxLayout, QLabel, QTextEdit, QLineEdit, QHBoxLayout)
from PySide6.QtCore import (Qt, QTimer, QThread, Signal)
import ctypes
import random
from tools.path_utils import get_asset_path

class FilesWatcherWorker(QThread):
    finished_signal = Signal()
    def run(self):
        from tools.files_watcher import files_watcher_main
        files_watcher_main()
        self.finished_signal.emit()

ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("miku_friend")

class ChatbotWindowMiku(QMainWindow):
    def __init__(self, main_window):
        super().__init__()
        from core.miku_config_manager import load_soul_data
        from core.i18n import get_text
        self.idiom = load_soul_data().get("idiom", "Español")
        self.get_text = get_text

        self.main_window = main_window
        self.setWindowTitle("Miku Friend Chat")
        self.setWindowIcon(QIcon(get_asset_path("assets/Miku1/m2/NoOutline/Pngs/m2UpScale.png")))
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
        self.user_input.setPlaceholderText(self.get_text(self.idiom, "placeholder"))
        self.user_input.returnPressed.connect(self.send_message)
        self.input_layout.addWidget(self.user_input)

        # Create Send Button
        self.send_button = QPushButton(self.get_text(self.idiom, "btn_send"))
        self.send_button.clicked.connect(self.send_message)
        self.input_layout.addWidget(self.send_button)

        #create restart button
        self.restart_button = QPushButton(self.get_text(self.idiom, "btn_restart"))
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

        # Conectar el timer para que Miku envíe un mensaje al terminar
        import UI.timmer_app as tmp_app
        tmp_app._emitter.finish_signal.connect(self.on_timer_finished)

    def on_timer_finished(self, msg, is_focus=False):
        if is_focus:
            message = "¡El temporizador de concentración (Focus) ha terminado! Espero que el tiempo haya sido productivo. (≧◡≦)"
        else:
            message = "¡El temporizador ha terminado! (≧◡≦)"
            
        miku_html = f"""
        <div style="margin: 5px 0;">
            <b style="color: #39c5bb;">Miku:</b> 
            <span style="color: #e6eceb;">{message}</span>
        </div>
        """
        self.chat_history.append(miku_html)

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
        self.chat_history.append(f'<p style="color: grey;">{self.get_text(self.idiom, "chat_restarted")}</p>')
        self.send_button.setEnabled(True)
        self.send_button.setStyleSheet("background-color: #39c5bb;")
        self.user_input.setEnabled(True)
        self.user_input.clear()

    def send_message(self):
        user_message = self.user_input.text().strip()
        if user_message:
            if not hasattr(self, 'first_message_handled'):
                self.first_message_handled = True
                self.check_and_run_files_watcher()

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

    def check_and_run_files_watcher(self):
        from tools.files_watcher import dont_burn_tokens
        if not dont_burn_tokens():
            msg = self.get_text(self.idiom, "listing_files")
            self.chat_history.append(f'<p style="color: grey; font-style: italic;">{msg}</p>')
            self.files_watcher_worker = FilesWatcherWorker()
            self.files_watcher_worker.finished_signal.connect(self.on_files_watcher_done)
            self.files_watcher_worker.start()

    def on_files_watcher_done(self):
        msg = self.get_text(self.idiom, "listing_files_done")
        self.chat_history.append(f'<p style="color: grey; font-style: italic;">{msg}</p>')

    def workers_working_brr():
        from agent_f import essay_agent_brain
        if essay_agent_brain.are_workers_working():
            working_messages = [
                1, "miku is working hard >:)",
                2, "miku doesn't stop, no matter what",
                3, "miku would like to be paid more >:( ",
                4, "I'm thinking, I'm thinking",
                5, "Patience",
                6, "Work, work, work, work",
                7, "Miku will do it",
                8, "Almost done",
                9, "Let me cook",
                10, "You should do your own homework >:(" 
            ]
            return working_messages[random.randint(0, len(working_messages) - 1)]
        else:
            pass

    def display_miku_response(self):
        self.send_button.setEnabled(False)
        self.user_input.setEnabled(True)
        self.send_button.setStyleSheet("background-color: gray;")
        
        # Iniciar animación de carga en la etiqueta de estado
        self.status_label.setText(self.get_text(self.idiom, "thinking") + ".")
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
            self.chat_history.append(f'<p style="color: red;">{self.get_text(self.idiom, "error_api")}</p>')
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

    def while_miku_working(self):
        message_of_working = self.workers_working_brr()
        if message_of_working:
            self.remove_last_line_from_chat_history()
            self.chat_history.append('<p style="color: grey;">' + message_of_working + '</p>')
            QTimer.singleShot(5000, self.mi_funcion)
            
    def remove_last_line_from_chat_history(self):
        self.chat_history.pop()
        self.chat_history_display.clear()
        for message in self.chat_history:
            self.chat_history_display.append(message)

    def update_thinking_dots(self):
        self.thinking_dots_count = (self.thinking_dots_count % 3) + 1
        dots = "." * self.thinking_dots_count
        self.status_label.setText(f"{self.get_text(self.idiom, 'thinking')}{dots}")

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

