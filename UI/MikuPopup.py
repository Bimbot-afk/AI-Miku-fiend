import sys
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QApplication
from PySide6.QtCore import Qt, QTimer, QPropertyAnimation, QRect, QEasingCurve
from PySide6.QtGui import QIcon, QPixmap

class MikuPopup(QWidget):
    def __init__(self, title, message, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        self.resize(350, 120)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        
        container = QWidget(self)
        container.setStyleSheet("""
            QWidget {
                background-color: #1a1d1f;
                border: 2px solid #39c5bb;
                border-radius: 12px;
            }
        """)
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(10, 10, 10, 10)
        
        # Header (Title and Close Button)
        header_layout = QHBoxLayout()
        title_label = QLabel(f"<b>{title}</b>")
        title_label.setStyleSheet("color: #39c5bb; font-size: 14px; border: none;")
        header_layout.addWidget(title_label)
        
        header_layout.addStretch()
        
        close_btn = QPushButton("X")
        close_btn.setFixedSize(20, 20)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #e35b8f;
                border: none;
                font-weight: bold;
            }
            QPushButton:hover {
                color: #ff1493;
            }
        """)
        close_btn.clicked.connect(self.close_popup)
        header_layout.addWidget(close_btn)
        
        container_layout.addLayout(header_layout)
        
        # Message body
        msg_label = QLabel(message)
        msg_label.setStyleSheet("color: #e6eceb; font-size: 12px; border: none;")
        msg_label.setWordWrap(True)
        container_layout.addWidget(msg_label)
        
        layout.addWidget(container)
        
        # Position in bottom right corner
        self.position_popup()
        
        # Auto-close after 10 seconds
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.close_popup)
        self.timer.start(10000)

        # Entrance animation
        self.animate_entrance()

    def position_popup(self):
        screen = QApplication.primaryScreen().availableGeometry()
        x = screen.width() - self.width() - 20
        y = screen.height() - self.height() - 20
        self.move(x, y)
        self.target_y = y
        
    def animate_entrance(self):
        screen = QApplication.primaryScreen().availableGeometry()
        start_y = screen.height()
        
        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(500)
        self.animation.setStartValue(QRect(self.x(), start_y, self.width(), self.height()))
        self.animation.setEndValue(QRect(self.x(), self.target_y, self.width(), self.height()))
        self.animation.setEasingCurve(QEasingCurve.OutBack)
        self.animation.start()

    def close_popup(self):
        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(400)
        self.animation.setStartValue(self.geometry())
        screen = QApplication.primaryScreen().availableGeometry()
        self.animation.setEndValue(QRect(self.x(), screen.height() + 20, self.width(), self.height()))
        self.animation.setEasingCurve(QEasingCurve.InBack)
        self.animation.finished.connect(self.close)
        self.animation.start()

    def mousePressEvent(self, event):
        # Click para cerrar más rápido
        if event.button() == Qt.LeftButton:
            self.close_popup()
