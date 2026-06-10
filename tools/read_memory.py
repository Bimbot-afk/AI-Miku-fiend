import os

name_txt = "miku_memories.txt"

def read_memory():
    folder = "miku_creations"
    path_txt = os.path.join(folder, name_txt)
    if not os.path.exists(path_txt):
        return "No memory found"
    with open(path_txt, "r", encoding="utf-8") as r:
        return r.read().strip()
    
    