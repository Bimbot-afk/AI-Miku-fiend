from PySide6.QtWidgets import QCheckBox
from PySide6.QtGui import QIcon
import json
import os
from PySide6.QtWidgets import QMessageBox
from PySide6.QtWidgets import QComboBox
from PySide6.QtWidgets import QFormLayout
from PySide6.QtWidgets import (QMainWindow, QPushButton, QWidget, QVBoxLayout, 
                                QLabel, QTextEdit, QLineEdit, QHBoxLayout, QListWidget, QStackedWidget, QFrame)
from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt
import os
from dotenv import load_dotenv, set_key
import ctypes
from tools.path_utils import get_asset_path

ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("miku_friend")

load_dotenv()

class configurationMiku(QMainWindow):
    def __init__(self, main_window=None):
        super().__init__(main_window)
        self.main_window = main_window
        self.setWindowIcon(QIcon(get_asset_path("assets/Miku1/m2/NoOutline/Pngs/m2UpScale.png")))
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
        self.menu_list.addItems(["General", "Advanced Options", "About"])
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
        from core.miku_config_manager import load_soul_prompt, load_soul_data, load_model_config
        
        # Load from Markdown files and config.json
        self.base_prompt = load_soul_prompt()
        
        soul_data = load_soul_data()
        self.miku_idiom = soul_data.get("idiom", "Español")
        self.user_name = soul_data.get("name", "Usuario")
        self.user_city = soul_data.get("city", "Bogotá")
        self.personalizated_promt = soul_data.get("personalizated_promt", "")
        self.miku_personality = soul_data.get("miku_personality", "Miku classic")
        
        model_config = load_model_config()
        self.miku_temperature = model_config.get("temperature", 0.3)
        self.miku_top_p = model_config.get("top_p", 0.6)
        self.miku_model = model_config.get("model", "nex-agi/nex-n2-pro:free")
        self.secondary_model_name = model_config.get("secondary_model", "nex-agi/nex-n2-pro:free")
        self.focus_mode = model_config.get("focus_mode", False)
        
        self.api_key = os.getenv("api_key", "")
        self.server_url = os.getenv("url_api_key", "")

    def save_config(self):
        from core.miku_config_manager import save_soul_prompt, save_soul_data, save_model_config
        
        import sys
        if getattr(sys, 'frozen', False):
            env_path = os.path.join(sys._MEIPASS, ".env")
        else:
            env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env")

        try:
            # Save configuration to respective markdown files and JSON config
            save_soul_prompt(self.base_prompt)
            
            save_soul_data({
                "name": self.user_name,
                "idiom": self.miku_idiom,
                "city": self.user_city,
                "personalizated_promt": self.personalizated_promt,
                "miku_personality": self.miku_personality
            })
            
            save_model_config({
                "model": self.miku_model,
                "temperature": self.miku_temperature,
                "top_p": self.miku_top_p,
                "secondary_model": self.secondary_model_name,
                "focus_mode": self.focus_mode
            })
            
            with open(env_path, "w", encoding="utf-8") as f:
                f.write(f"api_key={self.api_key}\n")
                f.write(f"url_api_key={self.server_url}\n")
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

        self.input_city = QLineEdit()
        self.input_city.setText(self.user_city)
        form.addRow("City", self.input_city)

        self.input_prompt = QTextEdit()
        self.input_prompt.setPlaceholderText("Personalizated Prompt")
        self.input_prompt.setText(self.personalizated_promt)
        form.addRow("Personalizated Prompt", self.input_prompt)

        self.input_personalities = QComboBox()
        self.input_personalities.addItems(self.personalities)
        self.input_personalities.setCurrentText(self.miku_personality)
        form.addRow("Personalities", self.input_personalities)

        self.check_box_focus_mode = QCheckBox("Focus mode")
        self.check_box_focus_mode.setChecked(self.focus_mode)
        form.addRow("Focus mode", self.check_box_focus_mode)
        
        self.input_api_key = QLineEdit()
        self.input_api_key.setText(self.api_key)
        form.addRow("API Key", self.input_api_key)

        self.input_server_url = QLineEdit()
        self.input_server_url.setText(self.server_url)
        form.addRow("Server URL", self.input_server_url)
             
        layout.addLayout(form)

        self.button_guardar = QPushButton("Guardar")
        self.button_guardar.clicked.connect(self.guardar_configuracion)
        layout.addWidget(self.button_guardar)    

        self.button_salir = QPushButton("Salir")
        self.button_salir.clicked.connect(self.close)
        layout.addWidget(self.button_salir)

        return page

    def guardar_configuracion(self):
        # Guardar valores
        self.miku_idiom = self.combo_idioma.currentText()
        self.user_name = self.input_name.text()
        self.user_city = self.input_city.text()
        self.personalizated_promt = self.input_prompt.toPlainText()
        self.miku_personality = self.input_personalities.currentText()
        self.api_key = self.input_api_key.text()
        self.server_url = self.input_server_url.text()
        self.secondary_model_name = self.secondary_model_selection.text()
        self.focus_mode = self.check_box_focus_mode.isChecked()
        
        # Guardar valores de configuración avanzada
        try:
            self.miku_temperature = float(self.tempature.text())
        except ValueError:
            self.miku_temperature = 0.3
            
        try:
            self.miku_top_p = float(self.top_p.text())
        except ValueError:
            self.miku_top_p = 0.6
            
        self.miku_model = self.model_selection.text()
        self.base_prompt = self.prompt_base_config.toPlainText()
        
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

    def get_user_city(self):
        if not hasattr(self, 'user_city'):
            self.load_config()
        return self.user_city

    def get_personalizated_promt(self):
        if not hasattr(self, 'personalizated_promt'):
            self.load_config()
        return self.personalizated_promt

    def get_miku_temperature(self):
        if not hasattr(self, 'miku_temperature'):
            self.load_config()
        return self.miku_temperature

    def get_miku_top_p(self):
        if not hasattr(self, 'miku_top_p'):
            self.load_config()
        return self.miku_top_p

    def get_miku_model(self):
        if not hasattr(self, 'miku_model'):
            self.load_config()
        return self.miku_model

    def get_base_prompt(self):
        if not hasattr(self, 'base_prompt'):
            self.load_config()
        return self.base_prompt

    def get_secondary_model_name(self):
        if not hasattr(self, 'secondary_model_name'):
            self.load_config()
        return self.secondary_model_name

    def crear_page_model(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.addWidget(QLabel("<h2>Advanced Options</h2>"))
        
        self.warning_text = """<font color='red'>Warning: You can really f*ck it and burn everything, be carefull with what you do >:(.</font>"""
        layout.addWidget(QLabel(self.warning_text))
        
        form = QFormLayout()
        
        # Temperatura
        self.tempature = QLineEdit()
        self.tempature.setText(str(self.miku_temperature))
        form.addRow("Temperature:", self.tempature)

        # Top P
        self.top_p = QLineEdit()
        self.top_p.setText(str(self.miku_top_p))
        form.addRow("Top P:", self.top_p)

        # Model Selection
        self.model_selection = QLineEdit()
        self.model_selection.setText(self.miku_model)
        form.addRow("Model:", self.model_selection)

        # Secondary Model Selection
        self.secondary_model_selection = QLineEdit()
        self.secondary_model_selection.setText(self.secondary_model_name)
        form.addRow("Secondary Model:", self.secondary_model_selection)

        # Base Prompt text area
        self.prompt_base_config = QTextEdit()
        self.prompt_base_config.setPlaceholderText("Base Prompt")
        self.prompt_base_config.setText(self.base_prompt)
        form.addRow("Base Prompt:", self.prompt_base_config)
        
        layout.addLayout(form)
        return page



    def crear_page_about(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(10, 5, 10, 5)
        layout.setSpacing(12)

        # Title
        title = QLabel("<h2>About Settings</h2>")
        title.setStyleSheet("color: #39c5bb; font-weight: bold; margin-bottom: 5px;")
        layout.addWidget(title)

        # Stylesheet for card panels
        card_style = """
            QFrame {
                background-color: #1a1d1f;
                border: 2px solid #252e32;
                border-radius: 8px;
            }
            QLabel {
                border: none;
                background-color: transparent;
                color: #e6eceb;
            }
        """

        # Card 1: Project Info
        card_project = QFrame()
        card_project.setStyleSheet(card_style)
        layout_proj = QVBoxLayout(card_project)
        layout_proj.setContentsMargins(15, 12, 15, 12)
        
        proj_title = QLabel("<h3>Project Information</h3>")
        proj_title.setStyleSheet("color: #39c5bb; font-weight: bold;")
        proj_desc = QLabel("This project was created for a Hack Club competition.<br/>"
                           "Designed and developed by <b>Emanuel Martinez</b>.")
        proj_desc.setWordWrap(True)
        
        layout_proj.addWidget(proj_title)
        layout_proj.addWidget(proj_desc)
        layout.addWidget(card_project)

        # Card 2: Links
        card_links = QFrame()
        card_links.setStyleSheet(card_style)
        layout_links = QVBoxLayout(card_links)
        layout_links.setContentsMargins(15, 12, 15, 12)
        
        links_title = QLabel("<h3>Useful Links</h3>")
        links_title.setStyleSheet("color: #39c5bb; font-weight: bold;")
        
        links_desc = QLabel(
            "• 🔗 <a href='https://github.com/Bimbot-afk/AI-Miku-fiend' style='color: #39c5bb; text-decoration: underline;'>GitHub Repository</a><br/>"
            "• 💬 <a href='https://hackclub.enterprise.slack.com/archives/D0ATFQU6B7C' style='color: #39c5bb; text-decoration: underline;'>Emanuel's Slack</a><br/>"
            "• 🎨 <a href='https://justdenk.itch.io/miku-style-pixel-art-fanmade-free' style='color: #39c5bb; text-decoration: underline;'>Pixel Art illustrations by JustDenk</a>"
        )
        links_desc.setOpenExternalLinks(True)
        links_desc.setWordWrap(True)
        
        layout_links.addWidget(links_title)
        layout_links.addWidget(links_desc)
        layout.addWidget(card_links)

        # Card 3: Legal & Thanks
        card_legal = QFrame()
        card_legal.setStyleSheet(card_style)
        layout_legal = QVBoxLayout(card_legal)
        layout_legal.setContentsMargins(15, 12, 15, 12)
        
        legal_title = QLabel("<h3>Legal Disclaimer & Credits</h3>")
        legal_title.setStyleSheet("color: #39c5bb; font-weight: bold;")
        
        legal_desc = QLabel(
            "This is a fan work based on Hatsune Miku.<br/>"
            "Hatsune Miku © Crypton Future Media, INC. 2007.<br/>"
            "Used under the Piapro Character License / creator guidelines.<br/><br/>"
            "<i>Thanks for using my project! (≧◡≦)</i>"
        )
        legal_desc.setWordWrap(True)
        
        layout_legal.addWidget(legal_title)
        layout_legal.addWidget(legal_desc)
        layout.addWidget(card_legal)

        # Add spacer at the bottom
        layout.addStretch()

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
            

        


