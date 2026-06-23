from PySide6.QtCore import QThread, Signal
import re
import os
from openrouter import OpenRouter
from dotenv import load_dotenv
from datetime import datetime
import random
import csv
import io

#modificaciones para la austeridad del modelo :D
#message history: 3

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
        #fecha de hoy en formato texto
        self.today_date = datetime.now().strftime("%Y-%m-%d")

    def update_long_memory(self):
        # Solo resumimos si el historial creció y tenemos suficiente contexto
        if len(self.message_history) >= 3:
            # Resumimos solo los ÚLTIMOS 5 mensajes
            history_to_summarize = self.message_history[-3:]
            
            history_str = ""
            for msg in history_to_summarize:
                if msg.get("role") == "system":
                    continue
                role = "Usuario" if msg.get("role") == "user" else "Miku"
                history_str += f"**{role}**: {msg.get('content', '')}\n"

            history_message = [{
                "role": "system", 
                "content": f"Resume la siguiente conversación en español en una frase corta y concisa para tu memoria a largo plazo:\n\n{history_str}"
            }]
            try:
                response = None
                api_error = None
                for api_retry in range(2):
                    try:
                        response = self.client.chat.send(
                            model=self.secondary_model, 
                            messages=history_message,
                            temperature=0.3,
                            top_p=0.6
                        )
                        break
                    except Exception as e:
                        api_error = e
                        if api_retry == 0:
                            import time; time.sleep(2)
                        else:
                            pass
                if response is None:
                    if api_error is not None:
                        raise api_error
                    raise Exception("Failed to get API response")
                
                if not response.choices or response.choices[0].message.content is None:
                    raise Exception("La API devolvió una respuesta vacía o sin contenido.")
                    
                answer = response.choices[0].message.content
                
                # Append the summary with current date to miku.md
                from tools import open_txt_file
                current_date = datetime.now().strftime("%Y-%m-%d")
                open_txt_file.save_memory_session(f"- **[Resumen - {current_date}]**: {answer.strip()}")
                
                # Reload summaries from miku.md to long_term_memory
                session_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "miku_agent", "miku.md")
                self.long_term_memory.clear()
                if os.path.exists(session_path):
                    with open(session_path, "r", encoding="utf-8") as f:
                        self.long_term_memory.append(f.read().strip())
                        
                log_msg = f"[SYSTEM] Updated long term session memory summary: {answer.strip()}"
                self.log_signal.emit(log_msg)
                print(log_msg)
            except Exception as e:
                print(f"Error al generar memoria a largo plazo: {e}")

    def set_memory(self):
        # Limitamos el historial corto que se envía directamente al LLM
        self.message_history_short = self.message_history[-3:]

    def miku_config(self):
        from core.miku_config_manager import load_soul_prompt, load_soul_data, load_model_config
        
        # Load from Markdown files and config.json
        self.base_prompt = load_soul_prompt()
        
        soul_data = load_soul_data()
        self.miku_idiom = soul_data.get("idiom", "Español")
        self.user_name = soul_data.get("name", "Usuario")
        self.personalizated_promt = soul_data.get("personalizated_promt", "")
        self.miku_personality = soul_data.get("miku_personality", "Miku classic")
        
        model_config = load_model_config()
        self.miku_temperature = model_config.get("temperature", 0.3)
        self.miku_top_p = model_config.get("top_p", 0.6)
        self.miku_model = model_config.get("model", "nex-agi/nex-n2-pro:free")
        self.secondary_model = model_config.get("secondary_model", "nex-agi/nex-n2-pro:free")

        # Load session summaries from miku.md into long_term_memory
        session_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "miku_agent", "miku.md")
        self.long_term_memory.clear()
        
        # Check if today's session header exists in the file, otherwise append it
        current_date = datetime.now().strftime("%Y-%m-%d")
        header_text = f"\n\n## Sesión: {current_date}\n"
        
        if os.path.exists(session_path):
            try:
                with open(session_path, "r", encoding="utf-8") as f:
                    content = f.read()
            except Exception:
                content = ""
        else:
            content = ""
            
        if f"## Sesión: {current_date}" not in content:
            try:
                os.makedirs(os.path.dirname(session_path), exist_ok=True)
                with open(session_path, "a", encoding="utf-8") as f:
                    f.write(header_text)
                content += header_text
            except Exception as e:
                print(f"[SYSTEM] Error appending session header: {e}")
                
        if content.strip():
            self.long_term_memory.append(content.strip())

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
        # 1. Get session summaries (miku.md)
        session_summaries = self.long_term_memory[0] if self.long_term_memory else "Ninguno"
        
        memory_str = (
            f"--- RESÚMENES DE SESIONES ANTERIORES ---\n{session_summaries}\n\n"
        )
        
        p = self.base_prompt
        p = p.replace("{miku_idiom}", self.miku_idiom)
        p = p.replace("{user_name}", self.user_name)
        p = p.replace("{personalizated_promt}", self.personalizated_promt)
        p = p.replace("{miku_personality}", self.miku_personality)
        p = p.replace("{memory_str}", memory_str)
        #insertar fecha
        p = p.replace("{today_date}", self.today_date)

        # Load tool instructions from miku_agent/miku_tools.md
        tools_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "miku_agent", "miku_tools.md")
        system_instruction = ""
        if os.path.exists(tools_path):
            try:
                with open(tools_path, "r", encoding="utf-8") as f:
                    system_instruction = f.read().strip()
            except Exception as e:
                print(f"[SYSTEM] Error loading miku_tools.md: {e}")
        
        if system_instruction:
            p = p + "\n\n[INSTRUCCIÓN DE SISTEMA - HERRAMIENTAS]\n" + system_instruction
            
        return p

    def promt_with_web_results(self):
        p = self.base_prompt
        p = p.replace("{miku_idiom}", self.miku_idiom)
        p = p.replace("{user_name}", self.user_name)
        p = p.replace("{today_date}", self.today_date)
        p += "\n\n[SISTEMA]: Se te ha proporcionado resultados de una búsqueda en la red abajo. Úsalos para responder al usuario de forma natural. NO uses más herramientas."
        return p

    def run(self):
        # 1. Cargar variables de entorno y crear cliente
        self.load_env()
        # 2. Cargar configuración de Miku
        self.miku_config()
        self.clean_personality_input()
        # 3. Preparar memoria
        self.set_memory()

        # 3.1. Si existe un archivo temporal de búsqueda web manual, lo leemos
        web_results_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "miku_agent", "research_results.md")
        manual_web_results = None
        if os.path.exists(web_results_path):
            try:
                with open(web_results_path, "r", encoding="utf-8") as f:
                    manual_web_results = f.read().strip()
                os.remove(web_results_path)
            except Exception as e:
                print(f"[SYSTEM] Error leyendo resultados web: {e}")
        
        # 4. Creation de promt to AI
        if manual_web_results:
            message_to_AI = [{'role': 'system', 'content': self.promt_with_web_results()}] + self.message_history_short
            message_to_AI.append({"role": "system", "content": f"[RESULTADOS DE BÚSQUEDA WEB MANUAL]\n{manual_web_results}"})
        else:
            message_to_AI = [{'role': 'system', 'content': self.base_miku_base_prompt()}] + self.message_history_short
            
        if self.client is None or self.client.sdk_configuration.client is None:
            self.load_env()
        
        for iteration in range(3):
            try:
                web_msg = f"[WEB API] Querying response from {self.miku_model}..."
                self.log_signal.emit(web_msg)
                print(web_msg)

                response = None
                api_error = None
                for api_retry in range(4):
                    try:
                        response = self.client.chat.send(
                            model=self.miku_model, 
                            messages=message_to_AI,
                            temperature=self.miku_temperature,
                            top_p=self.miku_top_p
                        )
                        break
                    except Exception as e:
                        api_error = e
                        if api_retry == 0:
                            fallback_msg = f"[SYSTEM] API error, retrying model {self.miku_model} in 2 seconds..."
                            self.log_signal.emit(fallback_msg)
                            print(fallback_msg)
                            import time; time.sleep(2)
                        else:
                            pass

                
                if response is None:
                    if api_error is not None:
                        raise api_error
                    raise Exception("Failed to get response")
                    
                if not response.choices or response.choices[0].message.content is None:
                    raise Exception("La API devolvió una respuesta vacía o sin contenido.")
                    
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

            # 5. Parsear comandos inline en la respuesta de Miku
            # Formato: output[comando, "argumento", "hecho"]
            output_pattern = re.compile(r'output\s*\[\s*(.*?)\s*\]', re.IGNORECASE | re.DOTALL)
            match_output = output_pattern.search(answer)
            
            # Limpiar la respuesta para que el usuario no vea los comandos técnicos en la UI
            clean_answer = output_pattern.sub('', answer).strip()
            
            if match_output:
                inner_content = match_output.group(1)
                # Reemplazar nuevas líneas en el contenido interno para facilitar el parseo csv
                inner_content_clean = inner_content.replace('\n', ' ').replace('\r', ' ')
                try:
                    # Usamos csv.reader para parsear argumentos que pueden contener comillas y comas internas
                    reader = csv.reader(io.StringIO(inner_content_clean), delimiter=',', quotechar='"', skipinitialspace=True)
                    items = next(reader)
                    
                    if len(items) >= 1:
                        cmd = items[0].strip().lower().lstrip('/') # e.g. "save"
                        arg = items[1].strip().lower() if len(items) >= 2 else ""
                        text = items[2].strip() if len(items) >= 3 else ""
                        
                        if cmd == "save":
                            from tools import open_txt_file
                            if arg == "memory":
                                open_txt_file.save_general_memorie(text)
                                log_msg = f"[COMMAND] Inline SAVE_MEMORY executed. Saved: '{text}'"
                                self.log_signal.emit(log_msg)
                                print(log_msg)
                            elif arg == "session":
                                open_txt_file.save_memory_session(text)
                                log_msg = f"[COMMAND] Inline SAVE_SESSION executed. Saved: '{text}'"
                                self.log_signal.emit(log_msg)
                                print(log_msg)
                            elif arg == "soul":
                                open_txt_file.save_soul(text)
                                log_msg = f"[COMMAND] Inline SAVE_SOUL executed. Saved: '{text}'"
                                self.log_signal.emit(log_msg)
                                print(log_msg)
                                
                            self.finished_response.emit(clean_answer)
                            break

                        elif cmd == "websearch":
                            from tools import web_search
                            log_msg = f"[COMMAND] Inline WEB_SEARCH executed. Searching: '{text}'"
                            self.log_signal.emit(log_msg)
                            print(log_msg)
                            
                            # Realizamos la búsqueda
                            web_search.web_search(text)
                            
                            # Leemos los resultados del archivo que se acaba de crear
                            if os.path.exists(web_search.path_results_file):
                                with open(web_search.path_results_file, "r", encoding="utf-8") as f:
                                    web_results = f.read().strip()
                                web_search.delete_research_file()
                            else:
                                web_results = "No se encontraron resultados o hubo un error."
                                
                            # Cambiar el mensaje del sistema al prompt austero
                            message_to_AI[0] = {'role': 'system', 'content': self.promt_with_web_results()}
                            
                            # Añadir la respuesta del asistente con el tool call
                            message_to_AI.append({"role": "assistant", "content": answer})
                            # Añadir el resultado del tool call como system message para el próximo turno del loop
                            message_to_AI.append({"role": "system", "content": f"[RESULTADO DE BÚSQUEDA WEB]:\n{web_results}\n\nCRÍTICO: Responde al usuario usando esta información y NO vuelvas a usar herramientas."})
                            continue
                            
                        elif cmd == "read":
                            from core.miku_config_manager import load_memory_data
                            log_msg = f"[COMMAND] Inline READ executed. Searching: '{text}'"
                            self.log_signal.emit(log_msg)
                            print(log_msg)
                            
                            all_memories = load_memory_data()
                            found_memories = []
                            if text:
                                keywords = text.lower().split()
                                for mem in all_memories:
                                    if any(kw in mem.lower() for kw in keywords):
                                        found_memories.append(mem)
                            else:
                                found_memories = all_memories
                                # Añadir la respuesta del asistente con el tool call
                            message_to_AI.append({"role": "assistant", "content": answer})
                            # Añadir el resultado del tool call como system message para el próximo turno del loop
                            message_to_AI.append({"role": "system", "content": f"[RESULTADO DE READ - MEMORIA]:\n{found_memories}\n\nUsa esta información para continuar la conversación y responder al usuario. Si no encontraste información, díselo al usuario."})
                            continue

                        ###You can add whatever image u want that make u happy :D

                        elif cmd == "happymiku":
                            log_msg = "[COMMAND] Inline HAPPYMIKU executed."
                            self.log_signal.emit(log_msg)
                            print(log_msg)
                            # Inyectar un gatito feliz
                            root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                            cat_path = os.path.join(root_path, "assets", "cats")
                            if os.path.exists(cat_path):
                                cat_images = [f for f in os.listdir(cat_path) if f.lower().endswith(".png") or f.lower().endswith(".jpg")]
                                if cat_images:
                                    cat_img_path = os.path.join(cat_path, random.choice(cat_images)).replace("\\", "/")
                                    cat_image = f'<br><br><img src="file:///{cat_img_path}" width="200" style="border-radius: 8px;">'
                                    clean_answer += cat_image
                            else:
                                print(f"[SYSTEM] Could not find cat images path: {cat_path}")
                            self.finished_response.emit(clean_answer)
                            break
                            
                except Exception as e:
                    err_msg = f"[SYSTEM] Error processing inline command: {e}"
                    self.log_signal.emit(err_msg)
                    print(err_msg)

            # Si no hubo match, o hubo un error parseando o era un comando desconocido, emitimos respuesta limpia y cortamos loop
            self.finished_response.emit(clean_answer)
            break
        else:
            # Si el loop terminó todas sus iteraciones (por puros continues) y no rompió, emitimos la última respuesta
            self.finished_response.emit(clean_answer)

        # 6. Generar o actualizar la memoria a largo plazo en segundo plano.
        if len(self.message_history) >= 3 and len(self.message_history) % 3 == 0:
            self.update_long_memory()