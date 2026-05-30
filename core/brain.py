from PySide6.QtCore import QThread, Signal
import ollama

class consultar_miku(QThread):
    # La señal que enviará la respuesta de vuelta a la UI
    finished_response = Signal(str)

    def __init__(self, message):
        super().__init__()
        self.message = message

    def run(self):
        # Aquí ocurre la magia pesada sin congelar la UI
        response = ollama.chat(model='phi3:3.8b', messages=[{'role': 'user', 'content': self.message}])
        answer = response['message']['content']
        self.finished_response.emit(answer)