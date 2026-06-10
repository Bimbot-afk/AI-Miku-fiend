from PySide6.QtCore import QThread, Signal
from UI.miku_cmd import MikuCMD
from UI.configuration import configurationMiku
import core.cmd_brain as cmd_brain
import json
import os
import ollama
from openrouter import OpenRouter
from dotenv import load_dotenv



class consultar_miku(QThread):
    # La señal que enviará la respuesta de vuelta a la UI
    finished_response = Signal(str)
    # Señal para enviar logs a la consola de la UI
    log_signal = Signal(str)

    def __init__(self, message_history, long_term_memory_list):
        super().__init__()
        self.message_history = message_history
        # Usamos una referencia a la lista de la UI para que persista
        self.long_term_memory = long_term_memory_list 
        self.message_history_short = []
        self.miku_local_brain = "phi3:3.8b"

        self.list_commands = [
            "/Save",
            "/Read"
        ]

        self.question_y_n = (
            "Nesecitas un comando de la siguiente lista? responde SOLO Y SOLO if yes 'SI' if no answer 'NO' IF 'SI' cual:\n"
            "NO RESPONDAS NADA MAS, SOLO EL COMANDO Y ARGUMENTO\n"
            "/Save you have 3 options: soul(tu nucleo solo tocalo cuando sea estrictamente necesario para no romperte), memory(informacion relevante del momento para recordar en el futuro), session(conversation actual),\n"
            "/Read you have 3 options: soul(tu nucleo solo tocalo cuando sea estrictamente necesario para no romperte), memory(informacion relevante del momento para recordar en el futuro), session(conversation actual),"
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
        from core.miku_config_manager import load_soul_prompt, load_memory_data, load_model_config
        
        # Load from Markdown files and config.json
        self.base_prompt = load_soul_prompt()
        
        memory_data = load_memory_data()
        self.miku_idiom = memory_data.get("idiom", "Español")
        self.user_name = memory_data.get("name", "Usuario")
        self.personalizated_promt = memory_data.get("personalizated_promt", "")
        self.miku_personality = memory_data.get("miku_personality", "Miku classic")
        
        model_config = load_model_config()
        self.miku_temperature = model_config.get("temperature", 0.3)
        self.miku_top_p = model_config.get("top_p", 0.6)
        self.miku_model = model_config.get("model", "nex-agi/nex-n2-pro:free")

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
        #1.1 que nivel de memoria se va a usar
        self.memory_level = ""
        # 2. Cargar configuración de Miku
        self.miku_config()
        self.clean_personality_input()
        # 3. Preparar memoria
        self.set_memory()
        
        # 4. Enviar prompt (primero respondemos para no hacer esperar al usuario)
        full_messages = [{'role': 'system', 'content': self.base_miku_base_prompt()}] + self.message_history_short

        # Obtener el último mensaje del usuario como cadena de texto y limpiar variables
        message_to_ollama = ""
        for msg in reversed(self.message_history):
            if msg.get('role') == 'user':
                message_to_ollama = msg.get('content', '')
                break

        # 4.1 needs a comand?
        cmd_content = "NO"
        system_prompt = (
            "Determine if the user's last message requires executing a command from the list below.\n\n"
            "Available commands:\n"
            "- /Save soul (e.g., 'save in your soul...', 'update your core...')\n"
            "- /Save memory (e.g., 'remember that...', 'save that my dog is named...')\n"
            "- /Save session (e.g., 'save this chat...', 'save the session...')\n"
            "- /Read soul\n"
            "- /Read memory\n"
            "- /Read session\n\n"
            "Response rules:\n"
            "- If it requires a command, respond EXACTLY in this format: YES <command> <argument> (e.g., YES /Save memory)\n"
            "- If it DOES NOT require any command, respond only: NO\n"
            "Do not include any explanation, greetings, or extra text."
        )

        try:
            log_msg = f"[OLLAMA] Checking command requirements using local model: {self.miku_local_brain}"
            self.log_signal.emit(log_msg)
            print(log_msg)

            # Query local Ollama
            response = ollama.chat(
                model=self.miku_local_brain,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Mensaje del usuario: {message_to_ollama}"}
                ],
                options={
                    "temperature": 0.0,
                    "top_p": 1.0,
                    "num_predict": 20
                }
            )
            cmd_content = response['message']['content'].strip()
            log_msg = f"[OLLAMA] Command decision: {cmd_content}"
            self.log_signal.emit(log_msg)
            print(log_msg)
        except Exception as e:
            warn_msg = f"[SYSTEM] Ollama local call failed: {e}. Falling back to Web API."
            self.log_signal.emit(warn_msg)
            print(warn_msg)
            
            # Fallback to OpenRouter (Web API)
            try:
                fallback_model = "poolside/laguna-xs.2:free"
                self.log_signal.emit(f"[WEB API] Checking command requirements using OpenRouter ({fallback_model})...")
                print(f"[WEB API] Checking command requirements using OpenRouter ({fallback_model})...")
                response_cmd_needed = self.client.chat.send(
                    model=fallback_model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": f"Mensaje del usuario: {message_to_ollama}"}
                    ],
                    temperature=0.0,
                    top_p=1.0,
                    max_tokens=20,
                )
                msg_content = response_cmd_needed.choices[0].message.content
                cmd_content = msg_content.strip() if msg_content is not None else "NO"
                log_msg = f"[WEB API] Command decision: {cmd_content}"
                self.log_signal.emit(log_msg)
                print(log_msg)
            except Exception as ex:
                err_msg = f"[SYSTEM] Web API fallback also failed: {ex}"
                self.log_signal.emit(err_msg)
                print(err_msg)
                cmd_content = "NO"
        
        if self.client is None or self.client.sdk_configuration.client is None:
            self.load_env()
        
        try:
            web_msg = f"[WEB API] Querying response from {self.miku_model}..."
            self.log_signal.emit(web_msg)
            print(web_msg)

            response = self.client.chat.send(
                model=self.miku_model, 
                messages=full_messages,
                temperature=self.miku_temperature,
                top_p=self.miku_top_p
            )
            answer = response.choices[0].message.content

            resp_msg = f"[WEB API] Miku response: {answer}"
            self.log_signal.emit(resp_msg)
            print(resp_msg)
        except Exception as e:
            err_msg = f"[SYSTEM] Error in Miku chat: {e}"
            self.log_signal.emit(err_msg)
            print(err_msg)
            self.finished_response.emit("error")
            return
        
        def wich_level_of_memory(cmd_content):
            cmd_lower = cmd_content.lower()
            if "soul" in cmd_lower:
                self.memory_level = "soul:"
            elif "session" in cmd_lower:
                self.memory_level = "session:"
            else:
                self.memory_level = "memory:"
            return self.memory_level
            
        # Check /save
        if "SI" in cmd_content or "YES" in cmd_content or "yes" in cmd_content or "/Save" in cmd_content or "/save" in cmd_content:
            memory_level = wich_level_of_memory(cmd_content)
            try:
                # Obtener el último mensaje del usuario para guardar como memoria
                user_msg = ""
                if self.message_history_short:
                    for msg in reversed(self.message_history_short):
                        if msg.get('role') == 'user':
                            user_msg = msg.get('content', '')
                            break
                if not user_msg and self.message_history:
                    for msg in reversed(self.message_history):
                        if msg.get('role') == 'user':
                            user_msg = msg.get('content', '')
                            break

                from tools import open_txt_file
                
                if memory_level == "soul:":
                    open_txt_file.save_soul(user_msg)
                elif memory_level == "session:":
                    open_txt_file.save_memory_session(user_msg)
                elif memory_level == "memory:":
                    open_txt_file.save_general_memorie(user_msg)
                
                log_msg = f"[COMMAND] /Save executed successfully. Saved text: '{user_msg}'"
                self.log_signal.emit(log_msg)
                print(log_msg)
                self.finished_response.emit(answer)
            except Exception as e:
                err_msg = f"[SYSTEM] Error saving memory: {e}"
                self.log_signal.emit(err_msg)
                print(err_msg)
                self.finished_response.emit(answer)
        else:
            self.finished_response.emit(answer)

        # Check /read
        if "SI" in cmd_content and "/read"  in cmd_content:
            pass

        # 5. Generar o actualizar la memoria a largo plazo en segundo plano.
        if len(self.message_history) >= 5 and len(self.message_history) % 5 == 0:
            self.update_long_memory()