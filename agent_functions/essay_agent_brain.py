import os
from agent_functions import research_agent, drafting_agent, Editing_agent, YES_or_No_agent
from openrouter import OpenRouter
from dotenv import load_dotenv
from core.miku_config_manager import load_model_config

import requests
import time

def sync_llm_call(messages):
    env_in_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "env", ".env")
    env_in_root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env")
    env_path = env_in_folder if os.path.exists(env_in_folder) else env_in_root
    
    load_dotenv(env_path, override=True)
    
    api_key = os.getenv("api_key")
    url = os.getenv("url_api_key", "https://openrouter.ai/api/v1/chat/completions")
    if not url.endswith("/chat/completions"):
        url = url.rstrip("/") + "/chat/completions"
    
    config = load_model_config()
    model = config.get("secondary_model", "google/gemma-2-9b-it:free")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": model,
        "messages": messages,
        "temperature": 0.4,
        "top_p": 0.8,
        "max_tokens": 10000
    }
    
    for attempt in range(3):
        try:
            resp = requests.post(url, headers=headers, json=payload, timeout=60)
            resp.raise_for_status()
            data = resp.json()
            if "choices" in data and len(data["choices"]) > 0:
                content = data["choices"][0].get("message", {}).get("content")
                if content is None:
                    content = "Error: El modelo devolvió una respuesta vacía."
                return content
            else:
                print(f"[SYSTEM] Invalid API response: {data}")
        except Exception as e:
            print(f"[SYSTEM] Attempt {attempt+1} sync_llm_call error: {e}")
            time.sleep(2)
            
    return "Error: No se pudo generar la respuesta después de varios intentos."
def create_and_really_good_essay(query):
    # Limpiar archivos de sesiones anteriores
    miku_agent_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "miku_agent")
    files_to_clean = ["WIP.md", "editor_notes.md", "research.md"]
    for file in files_to_clean:
        path = os.path.join(miku_agent_dir, file)
        if os.path.exists(path):
            try:
                os.remove(path)
            except Exception as e:
                print(f"[SYSTEM] No se pudo borrar {file}: {e}")
                
    research_agent.research(query)
    correction_cycle(query)

def correction_cycle(query):
    cc = 4
    is_correction = False
    while cc > 0:
        drafting_agent.draft_the_information(query, is_correction_cycle=is_correction)
        print("[SYSTEM] Copleted, Sleeping 15s to avoid API rate limits...")
        time.sleep(15)
        
        Editing_agent.edit_the_essay()
        print("[SYSTEM] Copleted, Sleeping 15s to avoid API rate limits...")
        time.sleep(15)
        
        is_approved = YES_or_No_agent.yes_or_no(query, cc)
        if is_approved:
            break
            
        print("[SYSTEM] Copleted, Sleeping 15s before next correction cycle...")
        time.sleep(15)
        cc -= 1
        is_correction = True

def are_workers_done(is_correction):
    if is_correction:
        return True
    else:
        return False
        