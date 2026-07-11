from PySide6.QtCore import QThread, QTimer
from PySide6.QtWidgets import (QApplication, QMainWindow, QPushButton, QWidget, QVBoxLayout, QLabel, QMenu)
from PySide6.QtCore import (QSize, Qt, QPoint)
from PySide6.QtGui import (QImage, QPixmap, QIcon, QAction, QMovie)
from UI.chatbot_miku import ChatbotWindowMiku
from UI.configuration import configurationMiku
from UI.miku_cmd import MikuCMD
from UI.MikuPopup import MikuPopup
from core.notifications_listener import NotificationWorker
from core.brain import consultar_miku
from tools.idle_message import create_idle_message
import ctypes
from tools.path_utils import get_asset_path

ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("miku_friend")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Miku Friend")
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setWindowIcon(QIcon(get_asset_path("assets/Miku1/m2/NoOutline/Pngs/m2UpScale.png")))
        self.chat_open = ChatbotWindowMiku(self) # PRE-CARGADO
        self.cmd_window = None
        self.config_window = None
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.derecha_inferior_ventana = self.frameGeometry().bottomRight()
        self.posicion_inicial = self.derecha_inferior_ventana
        self.resize(250, 250)
        self.move(self.posicion_inicial)

        self.idle_timer = QTimer(self)
        self.miku_idle_timer = 1800000 # 30 minutos
        self.idle_timer.timeout.connect(self.idle_message)
        self.idle_timer.start(self.miku_idle_timer) # Inactividad dinámica

        label = QLabel()
        self.movie = QMovie(get_asset_path("assets/Miku1/m2/NoOutline/Gifs/m2.gif"))
        label.setMovie(self.movie)
        self.movie.start()
        label.resize(100,100)

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_menu)

        self.setCentralWidget(label)

        # Punto Rojo para notificaciones
        ##self.red_dot = QLabel("🔴", self)
        ##self.red_dot.move(200, 20) # Movido a la esquina superior derecha de la ventana
        ##self.red_dot.setStyleSheet("background: transparent; color: red; font-size: 16px;")
        ##self.red_dot.hide()

        # Worker para consultas silenciosas (como reaccionar a notificaciones)
        self.active_agent_workers = []
        self.popups = []

        # Inicializar y arrancar el listener de notificaciones
        self.notification_worker = NotificationWorker()
        self.notification_worker.notification_received.connect(self.handle_notification)
        self.notification_worker.start()

    def handle_notification(self, noti_dict):
        # Proteger: Si Miku está ocupada respondiendo en el chat, ignoramos la notificación
        if hasattr(self, 'chat_open') and self.chat_open.active_workers:
            return
        from core.miku_config_manager import load_soul_data
        idiom = load_soul_data().get("idiom", "Español")
        
        # Crear un prompt para Miku
        prompt = (f"[NUEVA NOTIFICACIÓN DE {noti_dict['app_name']}]\n"
                  f"Título: {noti_dict['title']}\n"
                  f"Mensaje: {noti_dict['content']}\n\n"
                  f"Piensa sobre esto y di algo al respecto de forma breve y natural. [CRITICAL: Escribe tu respuesta obligatoriamente en este idioma: {idiom}]")
        
        message_history = [{'role': 'user', 'content': prompt}]
        
        # Enviar la notificación al cerebro en segundo plano
        worker = consultar_miku(message_history, [])
        self.active_agent_workers.append(worker)
        
        # Cargar configuración si es necesario (así como se hace en el chat normal)
        if self.config_window is None:
            self.config_window = configurationMiku(self)
        worker.miku_config()
        
        worker.finished_response.connect(self.show_miku_reaction)
        worker.finished.connect(lambda: self.cleanup_worker(worker))
        worker.start()

    def show_miku_reaction(self, response):
        if response == "error":
            return
            
        from core.miku_config_manager import load_soul_data
        from core.i18n import get_text
        idiom = load_soul_data().get("idiom", "Español")
        title_text = get_text(idiom, "popup_title")
            
        # Crear un popup y mostrarlo
        popup = MikuPopup(title=title_text, message=response)
        self.popups.append(popup)
        popup.show()

        # Encender el punto rojo
        ##self.red_dot.show()

        # Inyectar el mensaje en el chat SIEMPRE
        miku_html = f'<p style="margin: 4px 0;"><b style="color: #39c5bb;">Miku:</b> {response}</p>'
        self.chat_open.chat_history.append(miku_html)
        self.chat_open.message_history.append({'role': 'assistant', 'content': response})

    def cleanup_worker(self, worker):
        if worker in self.active_agent_workers:
            self.active_agent_workers.remove(worker)

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
        menu.addAction(QAction("Minimize", self, triggered=self.minimize_app))
        menu.addAction(QAction("Exit", self, triggered=self.close_app))
        menu.exec(self.mapToGlobal(pos))

    def open_chat(self):
        ##self.red_dot.hide()
        self.idle_timer.start(self.miku_idle_timer) # Resetear timer

        self.chat_open.show()
        self.chat_open.raise_()
        self.chat_open.activateWindow()

    def open_command_line(self):
        self.idle_timer.start(self.miku_idle_timer) # Resetear timer

        if self.cmd_window is None:
            self.cmd_window = MikuCMD(self)

        self.cmd_window.show()
        self.cmd_window.raise_()
        self.cmd_window.activateWindow()

    def open_configuration(self):
        self.idle_timer.start(self.miku_idle_timer) # Resetear timer

        if self.config_window is None:
            self.config_window = configurationMiku(self)

        self.config_window.show()
        self.config_window.raise_()
        self.config_window.activateWindow()

    def mousePressEvent(self, event):
        self.idle_timer.start(self.miku_idle_timer) # Resetear timer si hace click

        if event.button() == Qt.RightButton:
            self.show_menu(event.pos())
        elif event.button() == Qt.MouseButton.LeftButton:
            self.posicion_inicial = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()
        
    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self.posicion_inicial)
            event.accept()

    def minimize_app(self):
        self.showMinimized()
    
    def close_app(self):
        self.notification_worker.stop()
        self.notification_worker.wait(1500)
        self.close()

    def idle_message(self):
        # Proteger: Si Miku está ocupada respondiendo en el chat, ignoramos el evento de inactividad
        if hasattr(self, 'chat_open') and self.chat_open.active_workers:
            return
        create_idle_message(self)