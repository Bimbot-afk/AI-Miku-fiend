import os
from core import cmd_brain

name_txt = "miku_memories.txt"

text = ""

def save_memory():
    folder = "miku_creations"
    if not os.path.exists(folder):
        os.makedirs(folder)
    path_txt = os.path.join(folder, name_txt)

    with open(path_txt, "a", encoding="utf-8") as file:
        file.write(text + "\n")

