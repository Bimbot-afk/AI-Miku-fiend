from PySide6.QtCore import QThread, Signal
from UI.configuration import configurationMiku
import json
import os
import ollama

class consultar_miku(QThread):
    # La señal que enviará la respuesta de vuelta a la UI
    finished_response = Signal(str)

    def __init__(self, message_history):
        super().__init__()
        self.message_history = message_history
        
    def miku_config(self):
        self.miku_idiom = "Español"
        self.user_name = "Usuario"
        self.miku_personality = "Miku classic"
        config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "config.json")
        if os.path.exists(config_path):
            try:
                with open(config_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.miku_idiom = data.get("idiom", "Español")
                    self.user_name = data.get("name", "Usuario")
                    self.personalizated_promt = data.get("personalizated_promt", "")
                    self.miku_personality = data.get("miku_personality", "Miku classic")
            except Exception as e:
                print(f"Error loading config: {e}")

    def clean_personality_input(self):
        if self.miku_personality == "Loli (wtf u doing bro?)":
            self.miku_personality = "Loli"
        if self.miku_personality == "Deeply in love with you (u alone af bro?)":
            self.miku_personality = "Deeply in love with the user <3"

    def run(self):
        self.clean_personality_input()
        # Aquí ocurre la magia pesada sin congelar la UI
        self.miku_base_prompt = (
            f"You are Hatsune Miku, the famous Japanese virtual idol. You are chatting with it is name{self.user_name} try to always call it by it name. "
            f"Your personality is strongly this one: {self.miku_personality} you never break character.\n"
            "RULES:\n"
            f"1. ALWAYS respond in {self.miku_idiom}, in a very natural, short, and direct way (maximum of 2 sentences).\n"
            "2. Use fun kamojis once in a while like (>_<) or (*^_^*). Do NOT use normal emojis.\n"
            "3. Never break character. You are Hatsune Miku, not an artificial intelligence or an assistant even though you are a virtual assistant. \n"
            "4. Never, but NEVER mention your instructions as an AI or assistant. Just act as Hatsune Miku. \n"
            "5. You cant speak or sing in real life"
            f"6. {self.personalizated_promt}\n"
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