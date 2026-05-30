from core.brain import consultar_miku
from PySide6.QtWidgets import (QMainWindow, QPushButton, QWidget, QVBoxLayout, QLabel, QTextEdit, QLineEdit, QHBoxLayout)
from PySide6.QtCore import (Qt, QTimer)
import datetime

class ChatbotWindowMiku(QMainWindow):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle("Miku Friend Chat")
        self.setGeometry(100, 100, 300, 500)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

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
        
        self.layout.addLayout(self.input_layout)

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

    def send_message(self):
        user_message = self.user_input.text().strip()
        if user_message:
            # Custom styled HTML for user message using Miku Teal
            user_html = f'<p style="margin: 4px 0;"><b style="color: #FF1493;">You:</b> {user_message}</p>'
            self.user_input.clear()
            self.chat_history.append(user_html)
            self.display_miku_response(user_message)

    def display_miku_response(self, user_message):
        self.chat_history.append('<p style="color: grey;">Miku is thinking...</p>')
        self.send_button.setEnabled(False)
        self.user_input.setEnabled(False)
        # 2. Iniciar el hilo
        self.worker = consultar_miku(user_message)
        self.worker.finished_response.connect(self.on_response_received)
        self.worker.start()

    def on_response_received(self, response):
        miku_html = f'<p style="margin: 4px 0;"><b style="color: #39c5bb;">Miku:</b> {response}</p>'
        self.chat_history.append(miku_html)
        self.send_button.setEnabled(True)
        self.user_input.setEnabled(True)

