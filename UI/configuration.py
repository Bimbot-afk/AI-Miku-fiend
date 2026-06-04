import json
import os
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

        # Cargar configuración desde el archivo antes de construir la UI
        self.load_config()

        # Central Widget
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        # Layout
        layout = QHBoxLayout(main_widget)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)

        # Left Menu List
        self.menu_list = QListWidget()
        self.menu_list.addItems(["General", "Model", "About"])
        self.menu_list.setFixedWidth(180)
        layout.addWidget(self.menu_list)

        # Right Stacked Pages
        self.stacked_widget = QStackedWidget()
        layout.addWidget(self.stacked_widget)

        # Agregar las páginas al stacked widget
        self.stacked_widget.addWidget(self.crear_page_general())
        self.stacked_widget.addWidget(self.crear_page_model())
        self.stacked_widget.addWidget(self.crear_page_about())
            
        # Conexiones
        self.menu_list.currentRowChanged.connect(self.stacked_widget.setCurrentIndex)
            
        # Seleccionar la primera página por defecto
        self.menu_list.setCurrentRow(0)

        # Aplicar el estilo
        self.apply_miku_stylesheet()

    def load_config(self):
        config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "config.json")
        self.miku_idiom = "Español"
        self.user_name = "Usuario"
        self.personalizated_promt = "nada"
        self.miku_personality = "Miku classic"
        if os.path.exists(config_path):
            try:
                with open(config_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.miku_idiom = data.get("idiom", "Español")
                    self.user_name = data.get("name", "Usuario")
                    self.personalizated_promt = data.get("personalizated_promt", "nada")
                    self.miku_personality = data.get("miku_personality", "Miku classic")
            except Exception as e:
                print(f"Error loading config: {e}")

    def save_config(self):
        config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "config.json")
        try:
            with open(config_path, "w", encoding="utf-8") as f:
                json.dump({"idiom": self.miku_idiom, "name": self.user_name, "personalizated_promt": self.personalizated_promt, "miku_personality": self.miku_personality}, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Error saving config: {e}")

    def crear_page_general(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.addWidget(QLabel("<h2>General Settings</h2>"))
        form = QFormLayout()
        self.idiomas = ["Español", "English"]

        self.personalities = ["Miku classic", "Rude", "Yandere", "Tsundere", "Loli (wtf u doing bro?)", "Deeply in love with you (u alone af bro?)"]

        self.combo_idioma = QComboBox()
        self.combo_idioma.addItems(self.idiomas)
        self.combo_idioma.setCurrentText(self.miku_idiom)
        form.addRow("Idioma:", self.combo_idioma)
        
        self.input_name = QLineEdit()
        self.input_name.setText(self.user_name)
        form.addRow("Name", self.input_name)

        self.input_prompt = QTextEdit()
        self.input_prompt.setPlaceholderText("Personalizated Prompt")
        self.input_prompt.setText(self.personalizated_promt)
        form.addRow("Personalizated Prompt", self.input_prompt)

        self.input_personalities = QComboBox()
        self.input_personalities.addItems(self.personalities)
        self.input_personalities.setCurrentText(self.miku_personality)
        form.addRow("Personalities", self.input_personalities)

        
        layout.addLayout(form)

        self.button_guardar = QPushButton("Guardar")
        self.button_guardar.clicked.connect(self.guardar_configuracion,)
        layout.addWidget(self.button_guardar)    

        self.button_salir = QPushButton("Salir")
        self.button_salir.clicked.connect(self.close)
        layout.addWidget(self.button_salir)

        return page

    def guardar_configuracion(self):
        self.miku_idiom = self.combo_idioma.currentText()
        self.user_name = self.input_name.text()
        self.personalizated_promt = self.input_prompt.toPlainText()
        self.miku_personality = self.input_personalities.currentText()
        self.save_config()
        QMessageBox.information(self, "Configuración guardada", "Configuración guardada correctamente")
        self.close()
        
    def send_config(self):
        if not hasattr(self, 'miku_idiom') or not hasattr(self, 'user_name'):
            self.load_config()
        return self.miku_idiom, self.user_name

    def salir(self):
        self.close()

    def get_miku_idiom(self):
        if not hasattr(self, 'miku_idiom'):
            self.load_config()
        return self.miku_idiom

    def get_user_name(self):
        if not hasattr(self, 'user_name'):
            self.load_config()
        return self.user_name

    def get_personalizated_promt(self):
        if not hasattr(self, 'personalizated_promt'):
            self.load_config()
        return self.personalizated_promt

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


                
                
                


                
                
            

        


