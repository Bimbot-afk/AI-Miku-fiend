from PySide6.QtCore import QThread
from PySide6.QtWidgets import (QApplication, QMainWindow, QPushButton, QWidget, QVBoxLayout, QLabel, QMenu)
from PySide6.QtCore import (QSize, Qt, QPoint)
from PySide6.QtGui import (QImage, QPixmap, QIcon, QAction, QMovie)
from UI.ChatbotWindowMiku import ChatbotWindowMiku
from UI.configuration import configurationMiku
from UI.miku_cmd import MikuCMD
import ctypes

ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("miku_friend")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Miku Friend")
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setWindowIcon(QIcon("C:/Users/emar0/Desktop/Proyectos/miku_friend/assets/Miku1/m2/NoOutline/Pngs/m2UpScale.png"))
        self.chat_open = None
        self.cmd_window = None
        self.config_window = None
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.derecha_inferior_ventana = self.frameGeometry().bottomRight()
        self.posicion_inicial = self.derecha_inferior_ventana
        self.resize(250, 250)
        self.move(self.posicion_inicial)

        label = QLabel()
        self.movie = QMovie("C:/Users/emar0/Desktop/Proyectos/miku_friend/assets/Miku1/m2/NoOutline/Gifs/m2.gif")
        label.setMovie(self.movie)
        self.movie.start()
        label.resize(100,100)

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_menu)

        self.setCentralWidget(label)

    def show_menu(self, pos):
        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu {
                background-color: #121516;
                color: #e6eceb;
                border: 2px solid #39c5bb;
                border-radius: 8px;
                padding: 6px;
            }
            QMenu::item {
                background-color: transparent;
                padding: 6px 28px 6px 20px;
                margin: 2px 2px;
                border-radius: 4px;
                font-family: 'Segoe UI', 'Arial', sans-serif;
                font-size: 10pt;
                font-weight: bold;
            }
            QMenu::item:selected {
                background-color: #39c5bb;
                color: #121516;
            }
            QMenu::separator {
                height: 1px;
                background-color: #e35b8f;
                margin: 5px 10px;
            }
        """)

        menu.addAction(QAction("Open Chat", self, triggered=self.open_chat))
        menu.addAction(QAction("Open Command Line", self, triggered=self.open_command_line))
        menu.addAction(QAction("Configuration", self, triggered=self.open_configuration))
        menu.addAction(QAction("Exit", self, triggered=self.close))
        menu.exec(self.mapToGlobal(pos))

    def open_chat(self):
        if self.chat_open is None:
            self.chat_open = ChatbotWindowMiku(self)

        self.chat_open.show()
        self.chat_open.raise_()
        self.chat_open.activateWindow()

    def open_command_line(self):
        if self.cmd_window is None:
            self.cmd_window = MikuCMD(self)

        self.cmd_window.show()
        self.cmd_window.raise_()
        self.cmd_window.activateWindow()

    def open_configuration(self):
        if self.config_window is None:
            self.config_window = configurationMiku(self)

        self.config_window.show()
        self.config_window.raise_()
        self.config_window.activateWindow()

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            self.show_menu(event.pos())
        elif event.button() == Qt.MouseButton.LeftButton:
            self.posicion_inicial = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()
        
    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self.posicion_inicial)
            event.accept()