import sys
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QApplication
from PySide6.QtCore import Qt, QTimer, QObject, Signal
import winsound

# Instancia global para evitar múltiples ventanas y recolección de basura
_timer_instance = None

class TimerSignalEmitter(QObject):
    start_signal = Signal(object, object)
    finish_signal = Signal(str, bool)

_emitter = TimerSignalEmitter()

def _on_start_signal(milliseconds, focus_mode):
    global _timer_instance
    if _timer_instance is None:
        _timer_instance = TimerApp()
    _timer_instance.set_timer(milliseconds, focus_mode)
    _timer_instance.show_window()

_emitter.start_signal.connect(_on_start_signal)

def start_timer(milliseconds, focus_mode=""):
    # Emitimos la señal para que la UI se cree de forma segura en el Main Thread
    _emitter.start_signal.emit(milliseconds, focus_mode)
    return "Temporizador iniciado."

class TimerApp(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Frameless and stays on top
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # Small square window
        self.resize(250, 250)
        
        self.time_remaining = 0  # en decimas de segundo
        self.is_focus_mode = False
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        
        self.watcher_timer = QTimer(self)
        self.watcher_timer.timeout.connect(self.check_focus_games)
        
        self.setup_ui()
        
    def check_focus_games(self):
        try:
            from tools import files_watcher
            files_watcher.files_watcher_games()
        except Exception as e:
            print(f"[TIMER] Error ejecutando files_watcher_games: {e}")
        
    def set_timer(self, milliseconds, focus_mode=""):
        self.is_focus_mode = (focus_mode.lower() == "focus")
        if self.is_focus_mode:
            self.header.setText("Miku Focus Timer")
            self.header.setStyleSheet("color: #e35b8f; font-size: 14px; border: none; font-weight: bold;")
        else:
            self.header.setText("Miku Timer")
            self.header.setStyleSheet("color: #39c5bb; font-size: 14px; border: none; font-weight: bold;")
            
        try:
            milis = int(milliseconds)
        except (ValueError, TypeError):
            milis = 60000 # Default 1 min si falla
        self.time_remaining = milis // 100
        
        if self.is_focus_mode:
            # check_interval = tiempo_total / 200 (en milisegundos)
            # Aseguramos que sea al menos 1000ms (1 segundo) para no colapsar la PC
            self.watcher_interval = max(1000, milis // 200)
            self.watcher_timer.start(self.watcher_interval)
        else:
            self.watcher_timer.stop()
            
        self.update_display()
        self.resume_timer()

    def setup_ui(self):
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
        
        # Encabezado (para poder arrastrar)
        self.header = QLabel("Miku Timer")
        self.header.setAlignment(Qt.AlignCenter)
        self.header.setStyleSheet("color: #39c5bb; font-size: 14px; border: none; font-weight: bold;")
        container_layout.addWidget(self.header)
        
        # Número en la mitad (el reloj)
        self.time_label = QLabel("00:00.0")
        self.time_label.setAlignment(Qt.AlignCenter)
        self.time_label.setStyleSheet("""
            color: #e6eceb; 
            font-size: 42px; 
            font-weight: bold; 
            border: none;
        """)
        container_layout.addWidget(self.time_label, stretch=1)
        
        # Contenedor de botones
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(8)
        
        btn_style = """
            QPushButton {
                background-color: #2a2d2f;
                color: #39c5bb;
                border: 1px solid #39c5bb;
                border-radius: 6px;
                padding: 6px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #39c5bb;
                color: #1a1d1f;
            }
            QPushButton:pressed {
                background-color: #2a958b;
            }
        """
        
        self.btn_resume = QPushButton("Iniciar")
        self.btn_resume.setStyleSheet(btn_style)
        self.btn_resume.clicked.connect(self.resume_timer)
        
        self.btn_pause = QPushButton("Pausar")
        self.btn_pause.setStyleSheet(btn_style)
        self.btn_pause.clicked.connect(self.pause_timer)
        
        self.btn_reset = QPushButton("Resetear")
        self.btn_reset.setStyleSheet(btn_style)
        self.btn_reset.clicked.connect(self.reset_timer)
        
        btn_layout.addWidget(self.btn_resume)
        btn_layout.addWidget(self.btn_pause)
        btn_layout.addWidget(self.btn_reset)
        
        container_layout.addLayout(btn_layout)
        
        # Botón de cerrar (estilo MikuPopup)
        self.btn_close = QPushButton("Cerrar")
        self.btn_close.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #e35b8f;
                border: none;
                font-weight: bold;
                margin-top: 5px;
            }
            QPushButton:hover {
                color: #ff1493;
            }
        """)
        self.btn_close.clicked.connect(self.close)
        container_layout.addWidget(self.btn_close)
        
        layout.addWidget(container)
        
        # Variables para arrastrar la ventana sin bordes
        self.drag_pos = None

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if self.drag_pos and event.buttons() == Qt.LeftButton:
            diff = event.globalPosition().toPoint() - self.drag_pos
            self.move(self.pos() + diff)
            self.drag_pos = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, event):
        self.drag_pos = None

    def update_time(self):
        if self.time_remaining > 0:
            self.time_remaining -= 1
            self.update_display()
            if self.time_remaining <= 0:
                self.timer.stop()
                self.watcher_timer.stop()
                self.time_label.setText("00:00.0")
                self.btn_resume.setText("Iniciar")
                
                # Emitir señal de que terminó (seguro, dentro del thread de la UI)
                _emitter.finish_signal.emit("El temporizador ha finalizado.", self.is_focus_mode)
                # Sonido de alarma (pita 3 veces)
                winsound.Beep(1000, 500)
                winsound.Beep(1000, 500)
                winsound.Beep(1000, 1000)
                # Volver a traer la ventana al frente
                self.raise_()
                self.activateWindow()
  

    def update_display(self):
        minutes = (self.time_remaining % 36000) // 600
        seconds = (self.time_remaining % 600) // 10
        tenths = self.time_remaining % 10
            
        time_str = f"{minutes:02d}:{seconds:02d}.{tenths}"
        self.time_label.setText(time_str)

    def resume_timer(self):
        if self.time_remaining > 0:
            self.btn_resume.setText("Reanudar")
            self.timer.start(100) # Se actualiza cada 100ms (0.1 segundos)
            if self.is_focus_mode and hasattr(self, 'watcher_interval'):
                self.watcher_timer.start(self.watcher_interval)

    def pause_timer(self):
        self.timer.stop()
        self.watcher_timer.stop()

    def reset_timer(self):
        self.timer.stop()
        self.watcher_timer.stop()
        self.time_remaining = 0
        self.time_label.setText("00:00.0")
        self.btn_resume.setText("Iniciar")

    def show_window(self):
        self.show()
        self.raise_()
        self.activateWindow()


            
