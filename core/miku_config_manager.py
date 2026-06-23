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

# ----------------- SOUL PROMPT & BASIC DATA FUNCTIONS (miku_soul.md) -----------------

def load_soul_prompt():
    """Reads the raw base prompt template from miku_soul.md (everything before the # Memory_Soul section)."""
    default_prompt = (
        "You are Hatsune Miku. Be natural and brief (max 2 sentences). "
        "Use kaomojis sparingly, never emojis. Never mention being an AI. "
        "Be direct and only answer what is asked."
    )
    if not os.path.exists(SOUL_FILE_PATH):
        return default_prompt
    try:
        with open(SOUL_FILE_PATH, "r", encoding="utf-8") as f:
            lines = []
            for line in f:
                if line.strip().startswith("# Memory_Soul") or line.strip().startswith("# Memory"):
                    break
                lines.append(line)
            content = "".join(lines).strip()
            if content:
                return content
    except Exception as e:
        print(f"[SYSTEM] Error loading soul prompt: {e}")
    return default_prompt

def save_soul_prompt(prompt):
    """Writes the raw base prompt template to miku_soul.md, preserving the # Memory_Soul section."""
    ensure_agent_dir()
    soul_data_part = ""
    if os.path.exists(SOUL_FILE_PATH):
        try:
            with open(SOUL_FILE_PATH, "r", encoding="utf-8") as f:
                content = f.read()
                match = re.search(r'(# Memory_Soul.*|# Memory.*)', content, re.DOTALL)
                if match:
                    soul_data_part = "\n\n" + match.group(1).strip()
        except Exception as e:
            print(f"[SYSTEM] Error reading soul file to preserve data: {e}")
            
    try:
        with open(SOUL_FILE_PATH, "w", encoding="utf-8") as f:
            f.write(prompt.strip() + soul_data_part + "\n")
    except Exception as e:
        print(f"[SYSTEM] Error saving soul prompt: {e}")

def load_soul_data():
    """
    Parses miku_soul.md to extract user config data under # Memory_Soul
    (name, idiom, personalizated_promt, etc.).
    """
    data = {
        "name": "Usuario",
        "idiom": "Español",
        "personalizated_promt": "",
        "miku_personality": "Miku classic"
    }
    if not os.path.exists(SOUL_FILE_PATH):
        return data

    try:
        with open(SOUL_FILE_PATH, "r", encoding="utf-8") as f:
            content = f.read()

        kv_pattern = re.compile(r"^(?:-\s*)?\*\*([^*]+)\*\*:\s*(.*)$")
        simple_kv_pattern = re.compile(r"^(?:-\s*)?([a-zA-Z_0-9]+):\s*(.*)$")
        
        found_section = False
        for line in content.splitlines():
            line_stripped = line.strip()
            if not line_stripped:
                continue
            if line_stripped.startswith("# Memory_Soul") or line_stripped.startswith("# Memory"):
                found_section = True
                continue
            if not found_section:
                continue

            match_kv = kv_pattern.match(line_stripped)
            if match_kv:
                key = match_kv.group(1).strip().lower().replace(" ", "_")
                val = match_kv.group(2).strip()
                if key in data:
                    data[key] = val
                continue

            match_simple_kv = simple_kv_pattern.match(line_stripped)
            if match_simple_kv:
                key = match_simple_kv.group(1).strip().lower()
                val = match_simple_kv.group(2).strip()
                if key in data:
                    data[key] = val
                continue
    except Exception as e:
        print(f"[SYSTEM] Error loading soul data: {e}")
        
    return data

def save_soul_data(data_dict):
    """
    Saves user parameters to miku_soul.md, preserving the prompt template at the top.
    """
    ensure_agent_dir()
    
    prompt_part = ""
    if os.path.exists(SOUL_FILE_PATH):
        try:
            with open(SOUL_FILE_PATH, "r", encoding="utf-8") as f:
                lines = []
                for line in f:
                    if line.strip().startswith("# Memory_Soul") or line.strip().startswith("# Memory"):
                        break
                    lines.append(line)
                prompt_part = "".join(lines).strip()
        except Exception as e:
            print(f"[SYSTEM] Error reading soul file to preserve prompt: {e}")
            
    if not prompt_part:
        prompt_part = (
            "You are Hatsune Miku. Be natural and brief (max 2 sentences). "
            "Use kaomojis sparingly, never emojis. Never mention being an AI. "
            "Be direct and only answer what is asked."
        )
        
    lines = [
        prompt_part,
        "",
        "# Memory_Soul",
        "",
        f"- **name**: {data_dict.get('name', 'Usuario')}",
        f"- **idiom**: {data_dict.get('idiom', 'Español')}",
        f"- **personalizated_promt**: {data_dict.get('personalizated_promt', '')}",
        f"- **miku_personality**: {data_dict.get('miku_personality', 'Miku classic')}"
    ]
    
    # Append other keys if any
    for k, v in data_dict.items():
        if k not in ["name", "idiom", "personalizated_promt", "miku_personality", "general_memories"]:
            lines.append(f"- **{k}**: {v}")
            
    content = "\n".join(lines) + "\n"
    try:
        with open(SOUL_FILE_PATH, "w", encoding="utf-8") as f:
            f.write(content)
    except Exception as e:
        print(f"[SYSTEM] Error saving soul data: {e}")

# ----------------- GENERAL MEMORY FUNCTIONS (miku_memory.md) -----------------

def load_memory_data():
    """Reads all general memories from miku_memory.md."""
    memories = []
    if not os.path.exists(MEMORY_FILE_PATH):
        return memories
    try:
        with open(MEMORY_FILE_PATH, "r", encoding="utf-8") as f:
            in_memories = False
            for line in f:
                line_stripped = line.strip()
                if not line_stripped:
                    continue
                if line_stripped.startswith("## General Memories") or line_stripped.startswith("# Memory"):
                    in_memories = True
                    continue
                if in_memories:
                    if line_stripped.startswith("-"):
                        mem = line_stripped[1:].strip()
                        if mem:
                            memories.append(mem)
                    else:
                        memories.append(line_stripped)
    except Exception as e:
        print(f"[SYSTEM] Error loading memory data: {e}")
    return memories

def save_memory_data(memories_list):
    """Saves all general memories to miku_memory.md."""
    ensure_agent_dir()
    lines = [
        "# Memory",
        "",
        "## General Memories"
    ]
    for mem in memories_list:
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
        "secondary_model": "nex-agi/nex-n2-pro:free",
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
                "secondary_model": data.get("secondary_model", default_config["model"]),
                "temperature": data.get("temperature", default_config["temperature"]),
                "top_p": data.get("top_p", default_config["top_p"])
            }
    except Exception as e:
        print(f"[SYSTEM] Error loading model config: {e}")
    return default_config

def save_model_config(config_dict):
    """Saves model configurations (model, temperature, top_p) to config.json."""
    try:
        existing = {}
        if os.path.exists(CONFIG_JSON_PATH):
            try:
                with open(CONFIG_JSON_PATH, "r", encoding="utf-8") as f:
                    existing = json.load(f)
            except Exception:
                pass
        
        existing["model"] = config_dict.get("model", existing.get("model", "nex-agi/nex-n2-pro:free"))
        existing["secondary_model"] = config_dict.get("secondary_model", existing.get("secondary_model", "nex-agi/nex-n2-pro:free"))
        existing["temperature"] = config_dict.get("temperature", existing.get("temperature", 0.3))
        existing["top_p"] = config_dict.get("top_p", existing.get("top_p", 0.6))
        
        for key in ["idiom", "name", "personalizated_promt", "miku_personality", "base_prompt"]:
            existing.pop(key, None)
            
        with open(CONFIG_JSON_PATH, "w", encoding="utf-8") as f:
            json.dump(existing, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"[SYSTEM] Error saving model config: {e}")
