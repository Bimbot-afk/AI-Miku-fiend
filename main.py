import sys
import PySide6
from PySide6.QtWidgets import (QApplication, QMainWindow, QPushButton, QWidget, QVBoxLayout, QLabel, QMenu)
from PySide6.QtCore import (QSize, Qt)
from PySide6.QtGui import (QImage, QPixmap, QIcon, QAction)
import os

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Miku Friend")
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.resize(100, 100)

        label = QLabel()
        label.setPixmap(QPixmap("C:/Users/emar0/Desktop/Proyectos/miku_friend/Miku1/m2/NoOutline/Gifs/m2.gif"))
        label.resize(100,100)

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_menu)

        self.setCentralWidget(label)

    def show_menu(self, pos):
        menu = QMenu(self)
        menu.addAction(QAction("Exit", self,triggered = self.close))
        menu.exec(self.mapToGlobal(pos))
    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            self.show_menu(event.pos())
        
        
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
    

