import os
import json
import re

# Resolve base paths
CORE_DIR = os.path.dirname(os.path.abspath(__file__))
MIKU_AGENT_DIR = os.path.join(CORE_DIR, "..", "miku_agent")
SOUL_FILE_PATH = os.path.join(MIKU_AGENT_DIR, "miku_soul.md")
MEMORY_FILE_PATH = os.path.join(MIKU_AGENT_DIR, "miku_memory.md")
CONFIG_JSON_PATH = os.path.join(CORE_DIR, "config.json")

def ensure_agent_dir():
    if not os.path.exists(MIKU_AGENT_DIR):
        os.makedirs(MIKU_AGENT_DIR)

# ----------------- SOUL PROMPT FUNCTIONS -----------------

def load_soul_prompt():
    """Reads the raw base prompt template from miku_soul.md."""
    default_prompt = (
        "Eres Hatsune Miku. Sé natural, breve (máx 2 frases) en {miku_idiom}. "
        "Usa kaomojis, no abuses de ellos, nunca emojis. Llama a {user_name} por su nombre. "
        "Sé siempre Miku, jamás menciones ser IA. {personalizated_promt} Tienes una personalidad: {miku_personality}. "
        "Contexto/Memoria de eventos pasados: {memory_str} No digas cosas que no se te solicitan, se directa a la pregunta o mensaje"
    )
    if not os.path.exists(SOUL_FILE_PATH):
        return default_prompt
    try:
        with open(SOUL_FILE_PATH, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if content:
                return content
    except Exception as e:
        print(f"[SYSTEM] Error loading soul prompt: {e}")
    return default_prompt

def save_soul_prompt(prompt):
    """Writes the raw base prompt template to miku_soul.md."""
    ensure_agent_dir()
    try:
        with open(SOUL_FILE_PATH, "w", encoding="utf-8") as f:
            f.write(prompt.strip() + "\n")
    except Exception as e:
        print(f"[SYSTEM] Error saving soul prompt: {e}")

# ----------------- MEMORY DATA FUNCTIONS -----------------

def load_memory_data():
    """
    Parses miku_memory.md to extract key-value data (name, idiom, personalizated_promt, etc.)
    and a list of general memories.
    """
    data = {
        "name": "Usuario",
        "idiom": "Español",
        "personalizated_promt": "",
        "miku_personality": "Miku classic",
        "general_memories": []
    }
    if not os.path.exists(MEMORY_FILE_PATH):
        return data

    try:
        with open(MEMORY_FILE_PATH, "r", encoding="utf-8") as f:
            content = f.read()

        # Regex patterns to find key-values:
        # e.g., - **name**: Emanuel   or   - name: Emanuel
        kv_pattern = re.compile(r"^(?:-\s*)?\*\*([^*]+)\*\*:\s*(.*)$")
        simple_kv_pattern = re.compile(r"^(?:-\s*)?([a-zA-Z_0-9]+):\s*(.*)$")
        
        in_general_memories = False
        
        for line in content.splitlines():
            line_stripped = line.strip()
            if not line_stripped:
                continue
            
            # Check for header of general memories section
            if line_stripped.startswith("## General Memories"):
                in_general_memories = True
                continue
            if line_stripped.startswith("#"):
                continue

            # Try to match key-value formats
            match_kv = kv_pattern.match(line_stripped)
            if match_kv and not in_general_memories:
                key = match_kv.group(1).strip().lower().replace(" ", "_")
                val = match_kv.group(2).strip()
                data[key] = val
                continue

            match_simple_kv = simple_kv_pattern.match(line_stripped)
            if match_simple_kv and not in_general_memories:
                key = match_simple_kv.group(1).strip().lower()
                val = match_simple_kv.group(2).strip()
                # Only map if it's a known key or starts with -
                if key in ["name", "idiom", "personalizated_promt", "miku_personality"]:
                    data[key] = val
                    continue

            # If it's a list item, clean the bullet point prefix
            if line_stripped.startswith("-"):
                mem = line_stripped[1:].strip()
                if mem:
                    data["general_memories"].append(mem)
            else:
                data["general_memories"].append(line_stripped)
                
    except Exception as e:
        print(f"[SYSTEM] Error loading memory data: {e}")
        
    return data

def save_memory_data(data_dict):
    """
    Saves user parameters and general memories to miku_memory.md.
    """
    ensure_agent_dir()
    
    # Get current memory data to preserve any existing general memories if not provided
    existing = load_memory_data()
    general_mems = data_dict.get("general_memories", existing.get("general_memories", []))
    
    lines = [
        "# Memory",
        "",
        f"- **name**: {data_dict.get('name', 'Usuario')}",
        f"- **idiom**: {data_dict.get('idiom', 'Español')}",
        f"- **personalizated_promt**: {data_dict.get('personalizated_promt', '')}",
        f"- **miku_personality**: {data_dict.get('miku_personality', 'Miku classic')}"
    ]

    # Save any other key value fields
    for k, v in data_dict.items():
        if k not in ["name", "idiom", "personalizated_promt", "miku_personality", "general_memories"]:
            lines.append(f"- **{k}**: {v}")

    if general_mems:
        lines.append("")
        lines.append("## General Memories")
        for mem in general_mems:
            lines.append(f"- {mem}")

    content = "\n".join(lines) + "\n"
    
    try:
        with open(MEMORY_FILE_PATH, "w", encoding="utf-8") as f:
            f.write(content)
    except Exception as e:
        print(f"[SYSTEM] Error saving memory data: {e}")

# ----------------- MODEL CONFIG FUNCTIONS -----------------

def load_model_config():
    """Loads model configurations (model, temperature, top_p) from config.json."""
    default_config = {
        "model": "nex-agi/nex-n2-pro:free",
        "temperature": 0.3,
        "top_p": 0.6
    }
    if not os.path.exists(CONFIG_JSON_PATH):
        return default_config
    try:
        with open(CONFIG_JSON_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            return {
                "model": data.get("model", default_config["model"]),
                "temperature": data.get("temperature", default_config["temperature"]),
                "top_p": data.get("top_p", default_config["top_p"])
            }
    except Exception as e:
        print(f"[SYSTEM] Error loading model config: {e}")
    return default_config

def save_model_config(config_dict):
    """Saves model configurations (model, temperature, top_p) to config.json."""
    try:
        # Load any existing data to preserve extra JSON keys if they exist
        existing = {}
        if os.path.exists(CONFIG_JSON_PATH):
            try:
                with open(CONFIG_JSON_PATH, "r", encoding="utf-8") as f:
                    existing = json.load(f)
            except Exception:
                pass
        
        existing["model"] = config_dict.get("model", existing.get("model", "nex-agi/nex-n2-pro:free"))
        existing["temperature"] = config_dict.get("temperature", existing.get("temperature", 0.3))
        existing["top_p"] = config_dict.get("top_p", existing.get("top_p", 0.6))
        
        # We don't save the prompt or memory fields here anymore since they are in .md files.
        # But we remove them if they were previously present to keep config.json clean.
        for key in ["idiom", "name", "personalizated_promt", "miku_personality", "base_prompt"]:
            existing.pop(key, None)
            
        with open(CONFIG_JSON_PATH, "w", encoding="utf-8") as f:
            json.dump(existing, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"[SYSTEM] Error saving model config: {e}")
