from PySide6.QtCore import QThread, Signal
from UI.miku_cmd import MikuCMD
from UI.configuration import configurationMiku
import core.cmd_brain as cmd_brain
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

        self.question_y_n = (
        "Nesecitas un comando de la siguiente lista? responde solo if yes 'SI' if no answer 'NO' IF 'SI' cual:"
        "/Save (You save something important that should be remembered for the future)"
        )

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
        self.personalizated_promt = ""
        self.miku_temperature = 0.3
        self.miku_top_p = 0.6
        self.miku_model = "nex-agi/nex-n2-pro:free"
        self.base_prompt = (
            "Eres Hatsune Miku. Sé natural, breve (máx 2 frases) en {miku_idiom}. "
            "Usa kaomojis, no abuses de ellos, nunca emojis. Llama a {user_name} por su nombre. "
            "Sé siempre Miku, jamás menciones ser IA. {personalizated_promt} Tienes una personalidad: {miku_personality}. "
            "Contexto/Memoria de eventos pasados: {memory_str} "
            "No digas cosas que no se te solicitan, se directa a la pregunta o mensaje"
        )
        config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")
        if os.path.exists(config_path):
            try:
                with open(config_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.miku_idiom = data.get("idiom", "Español")
                    self.user_name = data.get("name", "Usuario")
                    self.personalizated_promt = data.get("personalizated_promt", "")
                    self.miku_personality = data.get("miku_personality", "Miku classic")
                    self.miku_temperature = data.get("temperature", 0.3)
                    self.miku_top_p = data.get("top_p", 0.6)
                    self.miku_model = data.get("model", "nex-agi/nex-n2-pro:free")
                    self.base_prompt = data.get("base_prompt", self.base_prompt)
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
        p = self.base_prompt
        p = p.replace("{miku_idiom}", self.miku_idiom)
        p = p.replace("{user_name}", self.user_name)
        p = p.replace("{personalizated_promt}", self.personalizated_promt)
        p = p.replace("{miku_personality}", self.miku_personality)
        p = p.replace("{memory_str}", memory_str)
        return p

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

        # 4.1 needs a comand?
        try:
            response_cmd_needed = self.client.chat.send(
                model="z-ai/glm-4.5-air:free",
                messages=full_messages + [{"role": "user", "content": self.question_y_n}],
                temperature=0.0,
                top_p=1.0,
                max_tokens=20,
            )
            msg_content = response_cmd_needed.choices[0].message.content
            cmd_content = msg_content.strip() if msg_content is not None else "NO"
        except Exception as e:
            print(f"Error checking command needed: {e}")
            cmd_content = "NO"
        
        if self.client is None or self.client.sdk_configuration.client is None:
            self.load_env()
        
        try:
            response = self.client.chat.send(
                model=self.miku_model, 
                messages=full_messages,
                temperature=self.miku_temperature,
                top_p=self.miku_top_p
            )
            answer = response.choices[0].message.content
        except Exception as e:
            print(f"Error en el chat de Miku: {e}")
            self.finished_response.emit("error")
            return

        # Check command needed
        if "SI" in cmd_content or "/Save" in cmd_content:
            try:
                from tools import open_txt_file
                open_txt_file.save_memory()
                self.finished_response.emit("miku have saved the memory")
            except Exception as e:
                print(f"Error saving memory: {e}")
                self.finished_response.emit(answer)
        else:
            self.finished_response.emit(answer)

        # 5. Generar o actualizar la memoria a largo plazo en segundo plano.
        # Solo lo hacemos si el historial tiene 5 o más mensajes, y solo una vez cada 5 mensajes.
        if len(self.message_history) >= 5 and len(self.message_history) % 5 == 0:
            self.update_long_memory()