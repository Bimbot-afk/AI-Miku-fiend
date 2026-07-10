import psutil
import os
import requests
from core.miku_config_manager import load_model_config
from UI.timmer_app import TimerApp
from UI.MikuPopup import show_miku_popup

def is_focus_mode():
    model_config = load_model_config()
    if model_config.get("focus_mode", False):
        return True
    else:
        return False

def files_watcher_main():
    if not dont_burn_tokens():
        list_all_important_files()
        organize_files_by_types()
    else:
        print("Programs file already exists, skipping organization.")

def dont_burn_tokens():
    json_path = os.path.join(path_results, "organized_programs.json")
    if os.path.exists(json_path):
        return True
    else:
        return False

from PySide6.QtCore import QObject, Signal

class PopupSignalEmitter(QObject):
    popup_signal = Signal(str, str)

_popup_emitter = PopupSignalEmitter()

def _on_popup_signal(title, message):
    show_miku_popup(title, message)

_popup_emitter.popup_signal.connect(_on_popup_signal)

def miku_popup_emit(title: str, message: str):
    _popup_emitter.popup_signal.emit(title, message)
    print(f"[NOTIFICATION] {title}: {message}")


def files_watcher_games(): ##yes its names just as the file, absolute cinema, im the real fallout
    import json
    json_path = os.path.join(path_results, "organized_programs.json")
    games_list = []
    
    # Intentar cargar el JSON generado
    if os.path.exists(json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                games_list = data.get("Games", data.get("Juegos", []))
            except json.JSONDecodeError:
                print("Error: El JSON de programas no es válido.")

    # Eliminar o comentar este print para no spamear la consola cada 7 segundos
    # print(f"Buscando los siguientes juegos: {games_list}")

    for proc in psutil.process_iter(['pid', 'name']):
        try:
            pinfo = proc.info
            proc_name = pinfo.get('name', '').lower()
            
            for g in games_list:
                g_lower = g.lower()
                proc_base = proc_name.replace(".exe", "")
                
                # Ignorar procesos sin nombre o muy cortos que dan falsos positivos
                if not proc_base or len(proc_base) <= 3:
                    continue
                    
                g_clean = g_lower.replace(" ", "")
                proc_clean = proc_base.replace(" ", "")
                
                # Extraer la palabra clave principal del juego (ej. de "Roblox Player" sacamos "roblox")
                g_words = g_lower.split()
                main_word = g_words[0] if g_words else ""
                # Si la primera palabra es un artículo ("El", "The"), usamos la segunda
                if len(main_word) <= 3 and len(g_words) > 1:
                    main_word = g_words[1]
                
                match1 = g_clean in proc_clean
                match2 = (proc_clean in g_clean and len(proc_clean) > 4)
                match3 = (len(main_word) > 3 and main_word in proc_clean)
                
                # Si se cumple cualquier condición (especialmente si contiene la palabra clave)
                if match1 or match2 or match3:
                    info = f"¡Juego detectado! PID: {pinfo['pid']} | Nombre: {pinfo['name']}"
                    print(info)
                    if is_focus_mode():
                        proc.kill()
                        miku_popup_emit("CONCENTRATE AHORA >:C", f"He cerrado {g_clean} por tu bien.")
                    else:
                        miku_popup_emit("Hey", f"He detectado que tienes abierto {g_clean}")
                    break
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

path_results = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "miku_agent")
file_programs = os.path.join(path_results, "programs.md")

def create_programs_md():
    os.makedirs(path_results, exist_ok=True)
    
def list_all_important_files():
    # Directorios comunes donde están los accesos directos de juegos y programas
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    start_menu_path = os.path.join(os.environ.get("APPDATA", ""), r"Microsoft\Windows\Start Menu\Programs")
    start_menu_all_path = r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs"
    
    routes_to_scan = [desktop_path, start_menu_path, start_menu_all_path]
    app_names = set()
    
    for route in routes_to_scan:
        if not os.path.exists(route):
            continue
        for root, dirs, files in os.walk(route):
            for file in files:
                if file.lower().endswith('.lnk') or file.lower().endswith('.url'):
                    base_name = os.path.splitext(file)[0]
                    # Evitar atajos basura comunes
                    if base_name.lower() not in ["desinstalar", "uninstall", "ayuda", "help"]:
                        app_names.add(base_name)
                    
    with open(file_programs, "w", encoding="utf-8") as f:
        for name in sorted(app_names):
            f.write(f"{name}\n")
    print("done collecting apps")

def organize_files_by_types():
    prompt = """
    Act as a computer expert. Your task is to organize a given list of program names into categories based on their program type (e.g., Games, Productivity, System, Utilities, Browsers, etc.).

    CRITICAL RULES:
    1. You MUST return the result exclusively in valid JSON format.
    2. Do NOT include any markdown blocks (like ```json) or conversational text.
    3. ONLY include the exact program names provided in the list. DO NOT hallucinate or add any other programs.
    4. Make sure "Games" or "Juegos" is a category if there are video games in the list.
    
    Example output:
    {
        "Games": ["League of Legends", "Fallout 4"],
        "Productivity": ["Word", "Excel"],
        "Browsers": ["Google Chrome", "Firefox"]
    }
    """
    
    # Check if the generated program list exists
    if not os.path.exists(file_programs):
        print("Programs file not found.")
        return
        
    # Leemos la lista completa ahora que está limpia y no saturará los tokens
    with open(file_programs, "r", encoding="utf-8") as f:
        file_list = f.read()

    full_prompt = prompt + "\n\nFiles to organize:\n" + file_list
    
    print("Sending file list to the secondary model for organization...")
    result_json = simple_secondary_llm_call(full_prompt)
    
    if result_json:
        import json
        output_file = os.path.join(path_results, "organized_programs.json")
        
        # Clean markdown if the AI includes it anyway
        clean_json = result_json.strip()
        if clean_json.startswith("```json"):
            clean_json = clean_json[7:]
        if clean_json.startswith("```"):
            clean_json = clean_json[3:]
        if clean_json.endswith("```"):
            clean_json = clean_json[:-3]
            
        try:
            # Validate JSON
            parsed_json = json.loads(clean_json.strip())
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(parsed_json, f, indent=4)
            print(f"Organized files saved correctly to {output_file}")
        except json.JSONDecodeError:
            print("Failed to parse JSON. The model returned:")
            print(result_json)

def simple_secondary_llm_call(prompt):
    """
    Llamada súper simple a la API utilizando el 'secondary_model'.
    """
    api_key = os.getenv("api_key")
    url = os.getenv("url_api_key", "https://openrouter.ai/api/v1")
    
    # La librería openrouter (basada en el SDK del usuario) parece esperar el base_url crudo
    if url.endswith("/chat/completions"):
        url = url.replace("/chat/completions", "")
        
    config = load_model_config()
    model = config.get("secondary_model", "nex-agi/nex-n2-pro:free")
    
    try:
        from openrouter import OpenRouter
        client = OpenRouter(
            api_key=api_key,
            server_url=url
        )
        
        response = client.chat.send(
            model=model,
            messages=[
                {"role": "system", "content": "You are a JSON generating machine. Output ONLY raw JSON. No markdown, no explanations, no extra items."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1,
            max_tokens=15000
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"[API ERROR] Error llamando al modelo secundario: {e}")
        return None
