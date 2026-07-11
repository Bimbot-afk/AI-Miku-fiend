import os
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt, Signal
import core.cmd_brain as cmd_brain
from tools.path_utils import get_asset_path
from PySide6.QtWidgets import (QMainWindow, QPushButton, QWidget, QVBoxLayout, QLabel, QTextEdit, QLineEdit, QHBoxLayout)
from PySide6.QtCore import (Qt, QTimer)
import ctypes

ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("miku_friend")

class MikuCMD(QMainWindow):
    def __init__(self, main_window=None):
        super().__init__(main_window)
        self.main_window = main_window
        self.setWindowTitle("Hatsune Miku - Command Line Mode")
        self.setGeometry(100, 100, 600, 400)
        self.setWindowIcon(QIcon(get_asset_path("assets/Miku1/m2/NoOutline/Pngs/m2UpScale.png")))
        self.setWindowFlags(Qt.Window)

        # Historial de chat y comando activo
        self.miku_comand = ""
        self.brain = cmd_brain.Brain_cmd()
        self.active_workers = []

        # Central Widget
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        # Layout
        layout = QVBoxLayout(main_widget)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)

        # Chat History
        self.chat_history = QTextEdit()
        self.chat_history.setReadOnly(True)
        layout.addWidget(self.chat_history)

        # Input Area
        input_layout = QHBoxLayout()
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText(">")
        self.input_field.returnPressed.connect(self.send_message)
        input_layout.addWidget(self.input_field)
        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self.send_message)
        input_layout.addWidget(self.send_button)
        layout.addLayout(input_layout)

        # Apply the style
        self.apply_miku_stylesheet()

    def send_message(self):
        user_input = self.input_field.text().strip()
        if not user_input:
            return

        # Mostrar mensaje del usuario
        self.chat_history.append(f"<b>&gt;</b> {user_input}")
        self.input_field.clear()

        # Guardar comando actual
        self.miku_comand = user_input
        self.comand_read()

    def keyPressEvent(self, event):
        # Interceptar Ctrl+C
        if event.key() == Qt.Key_C and (event.modifiers() & Qt.ControlModifier):
            self.chat_history.append("<p style='color: #ff5555;'>Miku stopped the process</p>")
            
            # Detener hilos activos
            for worker in self.active_workers:
                if worker.isRunning():
                    worker.quit()
                    worker.wait(1000)
            self.active_workers.clear()

            # Reactivar controles
            self.input_field.setEnabled(True)
            self.send_button.setEnabled(True)
            self.input_field.setFocus()
            event.accept()
        else:
            super().keyPressEvent(event)

    def append_log(self, text):
        formatted = text
        if text.startswith("[SYSTEM]"):
            formatted = f"<span style='color: #ffb86c;'><b>{text}</b></span>"
        elif text.startswith("[WEB API]"):
            formatted = f"<span style='color: #ff79c6;'><b>{text}</b></span>"
        elif text.startswith("[COMMAND]"):
            formatted = f"<span style='color: #50fa7b;'><b>{text}</b></span>"
        
        self.chat_history.append(formatted)

    def comand_read(self):
        cmd_lower = self.miku_comand.strip().lower()
        if cmd_lower.startswith("/"):
            if cmd_lower.startswith("/save"):
                response = self.brain.decide_comand(self.miku_comand)
                self.chat_history.append(f"<b>Miku_sys:</b> {response}")

            elif cmd_lower.startswith("/read"):
                response = self.brain.decide_comand(self.miku_comand)
                self.chat_history.append(f"<b>Miku_sys:</b> {response}")

            elif cmd_lower.startswith("/web_search"):
                response = self.brain.decide_comand(self.miku_comand)
                self.chat_history.append(f"<b>Miku_sys:</b> {response}")

            elif cmd_lower == "/help":
                self.chat_history.append("<b>System:</b> Commands: /save &lt;text&gt;, /exit, /help")

            elif cmd_lower == "/exit":
                self.close()

            else:
                self.chat_history.append("Unknown command. Type /help to see the list of commands")

    def send_comand_to_brain(self):
        return self.miku_comand
            

    def on_response_received(self):
        response = self.send_comand_to_brain()
        self.chat_history.append(response)

    def apply_miku_stylesheet(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #121516;
            }
            QTextEdit {
                background-color: #1a1d1f;
                border: 2px solid #252e32;
                border-radius: 8px;
                padding: 8px;
                color: #e6eceb;
            }
            QLineEdit {
                background-color: #1a1d1f;
                border: 2px solid #252e32;
                border-radius: 6px;
                padding: 8px;
                color: #e6eceb;
            }
            QLineEdit:focus {
                border: 2px solid #39c5bb;
            }
            QPushButton {
                background-color: #39c5bb;
                color: #121516;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #4ee0d6;
            }
            QPushButton:pressed {
                background-color: #2da199;
            }
        """)
