import os

CORE_DIR = os.path.dirname(os.path.abspath(__file__))
FOLDER = os.path.abspath(os.path.join(CORE_DIR, "..", "miku_agent"))
soul_file = "miku_soul.md"
memory_file = "miku_memory.md"
session_file = "miku.md"

def save_memory_session(text=""):
    if not os.path.exists(FOLDER):
        os.makedirs(FOLDER)
    path_session_file = os.path.join(FOLDER, session_file)

    # Solo guardamos si el texto no está vacío
    if isinstance(text, str):
        cleaned_text = text.strip()
        if cleaned_text:
            with open(path_session_file, "a", encoding="utf-8") as file:
                file.write(cleaned_text + "\n")

def save_general_memorie(text=""):
    if not os.path.exists(FOLDER):
        os.makedirs(FOLDER)

    if isinstance(text, str):
        cleaned_text = text.strip()
        if cleaned_text:
            from core.miku_config_manager import load_memory_data, save_memory_data
            # Load existing memory keys and list, append to general memories, and write it back
            mem_data = load_memory_data()
            if "general_memories" not in mem_data:
                mem_data["general_memories"] = []
            mem_data["general_memories"].append(cleaned_text)
            save_memory_data(mem_data)

def save_soul(text=""):
    if not os.path.exists(FOLDER):
        os.makedirs(FOLDER)

    if isinstance(text, str):
        cleaned_text = text.strip()
        if cleaned_text:
            from core.miku_config_manager import load_soul_prompt, save_soul_prompt
            # Load existing base prompt, append the new instruction, and write it back
            prompt = load_soul_prompt()
            if prompt:
                prompt += "\n" + cleaned_text
            else:
                prompt = cleaned_text
            save_soul_prompt(prompt)