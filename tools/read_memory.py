import os

CORE_DIR = os.path.dirname(os.path.abspath(__file__))
FOLDER = os.path.abspath(os.path.join(CORE_DIR, "..", "miku_agent"))
soul_file = "miku_soul.md"
memory_file = "miku_memory.md"
session_file = "miku.md"

def read_soul():
    path_soul_file = os.path.join(FOLDER, soul_file)
    if os.path.exists(path_soul_file):
        with open(path_soul_file, "r", encoding="utf-8") as file:
            return file.read().strip()
    return ""

def read_memory():
    path_memory_file = os.path.join(FOLDER, memory_file)
    if os.path.exists(path_memory_file):
        with open(path_memory_file, "r", encoding="utf-8") as file:
            return file.read().strip()
    return ""

def read_session():
    path_session_file = os.path.join(FOLDER, session_file)
    if os.path.exists(path_session_file):
        with open(path_session_file, "r", encoding="utf-8") as file:
            return file.read().strip()
    return ""
    