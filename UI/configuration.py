from PySide6.QtWidgets import QMessageBox
from PySide6.QtWidgets import QComboBox
from PySide6.QtWidgets import QFormLayout
from PySide6.QtWidgets import (QMainWindow, QPushButton, QWidget, QVBoxLayout, 
                                QLabel, QTextEdit, QLineEdit, QHBoxLayout, QListWidget, QStackedWidget)
from PySide6.QtWidgets import QLabel
from PySide6.QtCore import (Qt, QTimer)

class configurationMiku(QMainWindow):
    def __init__(self, main_window=None):
        super().__init__(main_window)
        self.main_window = main_window
        self.setWindowTitle("Configuration")
        self.resize(800, 550)
        self.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint)

        # Central Widget
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        # Layout
        layout = QHBoxLayout(main_widget)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)

        # Left Menu List
        self.menu_list = QListWidget()
        self.menu_list.addItems(["General", "AI Prompt", "Model", "About"])
        self.menu_list.setFixedWidth(180)
        layout.addWidget(self.menu_list)

        # Right Stacked Pages
        self.stacked_widget = QStackedWidget()
        layout.addWidget(self.stacked_widget)

        # Select first page by default
        self.menu_list.setCurrentRow(0)

        self.apply_miku_stylesheet()

        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        layout = QHBoxLayout(main_widget)

        self.menu_list = QListWidget()
        self.menu_list.addItems(["General", "AI Prompt", "Model", "About"])
        layout.addWidget(self.menu_list)

        self.page_widget = QWidget()
        layout.addWidget(self.page_widget)

        self.stacked_widget = QStackedWidget()
        self.stacked_widget.addWidget(self.crear_page_general())
        self.stacked_widget.addWidget(self.crear_page_ai_prompt())
        self.stacked_widget.addWidget(self.crear_page_model())
        self.stacked_widget.addWidget(self.crear_page_about())
            
        self.menu_list.currentRowChanged.connect(self.stacked_widget.setCurrentIndex)
            
        layout.addWidget(self.menu_list)
        layout.addWidget(self.stacked_widget)

    def crear_page_general(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.addWidget(QLabel("<h2>General Settings</h2>"))
        form = QFormLayout()
        self.idiomas = ["Español", "English"]
        
        self.combo_idioma = QComboBox()
        self.combo_idioma.addItems(self.idiomas)
        form.addRow("Idioma:", self.combo_idioma)
        
        self.input_name = QLineEdit()
        form.addRow("Name", self.input_name)
        
        layout.addLayout(form)

        self.button_guardar = QPushButton("Guardar")
        self.button_guardar.clicked.connect(self.guardar_configuracion)
        layout.addWidget(self.button_guardar)

        self.button_salir = QPushButton("Salir")
        self.button_salir.clicked.connect(self.close)
        layout.addWidget(self.button_salir)

        return page

    def guardar_configuracion(self):
        self.miku_idiom = self.combo_idioma.currentText()
        self.user_name = self.input_name.text()
        QMessageBox.information(self, "Configuración guardada", "Configuración guardada correctamente")
        
    def send_config(self):
        idiom = getattr(self, 'miku_idiom', '')
        if not idiom:
            idiom = 'Español'
        name = getattr(self, 'user_name', '')
        if not name:
            name = 'Usuario'
        return idiom, name

    def salir(self):
        self.close()

    def get_miku_idiom(self):
        return self.miku_idiom

    def get_user_name(self):
        return self.user_name

    def crear_page_ai_prompt(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.addWidget(QLabel("<h2>AI Prompt Settings</h2>"))
        return page

    def crear_page_model(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.addWidget(QLabel("<h2>Model Settings</h2>"))
        return page

    def crear_page_about(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.addWidget(QLabel("<h2>About Settings</h2>"))
        return page

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
            QListWidget {
                background-color: #1a1d1f;
                border: 2px solid #252e32;
                border-radius: 8px;
                padding: 5px;
                color: #e6eceb;
            }
            QListWidget::item {
                padding: 10px;
                border-radius: 6px;
                margin: 3px 0px;
                font-weight: bold;
                color: #e6eceb;
            }
            QListWidget::item:selected {
                background-color: #39c5bb;
                color: #121516;
            }
            QListWidget::item:hover:!selected {
                background-color: #2b3337;
                color: #39c5bb;
            }
            QTextEdit {
                background-color: #1a1d1f; /* Dark Panel Background */
                border: 2px solid #252e32;
                border-radius: 8px;
                padding: 8px;
                color: #e6eceb;
            }
            QTextEdit:focus {
                border: 2px solid #39c5bb;
            }
            QLineEdit {
                background-color: #1a1d1f;
                border: 2px solid #252e32;
                border-radius: 6px;
                padding: 8px;
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
                padding: 8px 16px;
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


                
                
                


                
                
            

        


