import sys
import os

with open("debug.txt", "w") as f:
    f.write(f"frozen: {getattr(sys, 'frozen', False)}\n")
    if hasattr(sys, '_MEIPASS'):
        f.write(f"_MEIPASS: {sys._MEIPASS}\n")
    else:
        f.write("_MEIPASS is missing\n")
    f.write(f"executable: {sys.executable}\n")
    f.write(f"cwd: {os.getcwd()}\n")
