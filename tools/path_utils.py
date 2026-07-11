import os
import sys

def get_asset_path(relative_path):
    """
    Get the absolute path to a resource.
    Works for development and for PyInstaller.
    """
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        # Assuming path_utils.py is inside `tools` folder
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    
    return os.path.join(base_path, relative_path)
