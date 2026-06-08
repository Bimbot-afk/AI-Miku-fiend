from PySide6.QtCore import QThread, Signal
from UI.configuration import configurationMiku
import json
import os
from openrouter import OpenRouter
from dotenv import load_dotenv


class consultar_miku(QThread):
    # La señal que enviará la respuesta de vuelta a la UI
    finished_response = Signal(str)

    def __init__(self, message_history, long_term_memory_list):
        super().__init__()
        self.message_history = message_history
        # Usamos una referencia a la lista de la UI para que persista
        self.long_term_memory = long_term_memory_list 
        self.message_history_short = []

    def update_long_memory(self):
        # Solo resumimos si el historial creció y tenemos suficiente contexto
        if len(self.message_history) >= 5:
            # Resumimos los mensajes anteriores al historial corto
            history_to_summarize = self.message_history[:-5] if len(self.message_history) > 5 else self.message_history
            history_message = [{
                "role": "system", 
                "content": f"resume esta conversacion en español en una frase corta para memoria a largo plazo: {history_to_summarize}"
            }]
            try:
                response = self.client.chat.send(
                    model="nvidia/nemotron-3-ultra-550b-a55b:free", 
                    messages=history_message,
                    temperature=0.3,
                    top_p=0.6
                )
                answer = response.choices[0].message.content
                # Actualizamos la memoria mutable en su lugar
                self.long_term_memory.clear()
                self.long_term_memory.append(answer)
            except Exception as e:
                print(f"Error al generar memoria a largo plazo: {e}")

    def set_memory(self):
        # Limitamos el historial corto que se envía directamente al LLM
        self.message_history_short = self.message_history[-5:]

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

    def load_env(self):
        env_in_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "env", ".env")
        env_in_root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env")
        env_path = env_in_folder if os.path.exists(env_in_folder) else env_in_root
        
        load_dotenv(env_path, override=True)
        self.client = OpenRouter(
            api_key=os.getenv("api_key"),
            server_url=os.getenv("url_api_key")
        )

    def base_miku_base_prompt(self):
        memory_str = self.long_term_memory[0] if self.long_term_memory else "Ninguna"
        miku_base_prompt = (
            f"Eres Hatsune Miku. Sé natural, breve (máx 2 frases) en {self.miku_idiom}."
            f" Usa kaomojis, no abuses de ellos, nunca emojis. Llama a {self.user_name} por su nombre. "
            f"Sé siempre Miku, jamás menciones ser IA. {self.personalizated_promt} Tienes una personalidad: {self.miku_personality}. "
            f"Contexto/Memoria de eventos pasados: {memory_str}"
            "No digas cosas que no se te solicitan, se directa a la pregunta o mensaje"
        )
        return miku_base_prompt

    def run(self):
        # 1. Cargar variables de entorno y crear cliente
        self.load_env()
        # 2. Cargar configuración de Miku
        self.miku_config()
        self.clean_personality_input()
        # 3. Preparar memoria
        self.set_memory()
        
        # 4. Enviar prompt (primero respondemos para no hacer esperar al usuario)
        full_messages = [{'role': 'system', 'content': self.base_miku_base_prompt()}] + self.message_history_short
        
        try:
            response = self.client.chat.send(
                model="liquid/lfm-2.5-1.2b-instruct:free", 
                messages=full_messages,
                temperature=0.3,
                top_p=0.6
            )
            answer = response.choices[0].message.content
            self.finished_response.emit(answer)
        except Exception as e:
            print(f"Error en el chat de Miku: {e}")
            self.finished_response.emit("error")
            return

        # 5. Generar o actualizar la memoria a largo plazo en segundo plano.
        # Solo lo hacemos si el historial tiene 5 o más mensajes, y solo una vez cada 5 mensajes.
        if len(self.message_history) >= 5 and len(self.message_history) % 5 == 0:
            self.update_long_memory()