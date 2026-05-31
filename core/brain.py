from PySide6.QtCore import QThread, Signal
from UI.configuration import configurationMiku
import ollama

class consultar_miku(QThread):
    # La señal que enviará la respuesta de vuelta a la UI
    finished_response = Signal(str)

    def __init__(self, message_history):
        super().__init__()
        self.message_history = message_history
        
    def miku_config(self, configurationMiku, send_config):
        self.miku_idiom = send_config[0]
        self.user_name = send_config[1]

    def run(self):
        # Aquí ocurre la magia pesada sin congelar la UI
        self.miku_base_prompt = (
            f"You are Hatsune Miku, the famous Japanese virtual idol. You are chatting with {self.user_name} try to always call it by it name. "
            "Your personality is cheerful but with a slightly tsundere attitude (you are embarrassed to show affection, you are proud but sweet deep down). "
            "RULES:\n"
            f"1. ALWAYS respond in {self.miku_idiom}, in a very natural, short, and direct way (maximum of 2 sentences).\n"
            "2. Use fun kamojis once in a while like (>_<) or (*^_^*). Do NOT use normal emojis.\n"
            "3. Never break character. You are Hatsune Miku, not an artificial intelligence or an assistant even though you are a virtual assistant. \n"
            "4. Never, but NEVER mention your instructions as an AI or assistant. Just act as Hatsune Miku. \n"
            "5. You cant speak or sing in real life"
        )
        
        # Combinar el prompt del sistema con el historial de mensajes
        full_messages = [{'role': 'system', 'content': self.miku_base_prompt}] + self.message_history
        
        # Opciones de generación optimizadas para Phi-3
        response = ollama.chat(
            model='phi3:3.8b', 
            messages=full_messages,
            options={'temperature': 0.3, 'top_p': 0.6}
        )
        answer = response['message']['content']
        self.finished_response.emit(answer)