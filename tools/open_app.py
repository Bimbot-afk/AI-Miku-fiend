import os
import winreg
import shutil
import subprocess


def get_app_path(app_name: str) -> str:
    """
    Intenta buscar la ruta de un ejecutable usando varios métodos de Windows.
    Devuelve la ruta si la encuentra, o None si no.
    """
    app_name_lower = app_name.lower().strip()
    if not app_name_lower.endswith('.exe'):
        exe_name = app_name_lower + '.exe'
    else:
        exe_name = app_name_lower
    # 1. Buscar en el PATH (shutil.which)
    in_path = shutil.which(exe_name)
    if in_path:
        return in_path
    # 2. Buscar en el Registro (App Paths)
    try:
        # Intentar en HKEY_LOCAL_MACHINE
        reg_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\\" + exe_name
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path)
        path, _ = winreg.QueryValueEx(key, "")
        if path:
            return path
    except FileNotFoundError:
        pass
    try:
        # Intentar en HKEY_CURRENT_USER
        reg_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\\" + exe_name
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path)
        path, _ = winreg.QueryValueEx(key, "")
        if path:
            return path
    except FileNotFoundError:
        pass
    # 3. Buscar Accesos Directos (.lnk) en el Menú Inicio
    # Usamos PowerShell para resolver la ruta destino del acceso directo
    start_menu_dirs = [
        os.path.expandvars(r"%ProgramData%\Microsoft\Windows\Start Menu\Programs"),
        os.path.expandvars(r"%APPDATA%\Microsoft\Windows\Start Menu\Programs"),
        os.path.expandvars(r"%USERPROFILE%\Desktop")
    ]
    for sm_dir in start_menu_dirs:
        if not os.path.exists(sm_dir):
            continue
        # Recorrer subcarpetas en el Menú Inicio
        for root, dirs, files in os.walk(sm_dir):
            for file in files:
                if file.lower().endswith('.lnk'):
                    # Ignorar los accesos directos de desinstalación
                    if "uninstall" in file.lower() or "desinstalar" in file.lower():
                        continue
                    # Si el nombre del acceso directo se parece al que buscamos
                    if app_name_lower in file.lower():
                        lnk_path = os.path.join(root, file)
                        # Devolver directamente el archivo .lnk. os.startfile se encargará
                        # de procesar el acceso directo junto con todos sus argumentos ocultos.
                        return lnk_path
    return None
def open_application(app_name: str) -> str:
    """
    Función que Miku usa para intentar abrir una aplicación.
    Si la encuentra usando la búsqueda en cascada, la abre con os.startfile.
    """
    path = get_app_path(app_name)
    if path:
        try:
            # os.startfile abre la app de forma asíncrona, igual que hacerle doble clic en Windows
            os.startfile(path)
            return f"He abierto {app_name} exitosamente desde {path}."
        except Exception as e:
            return f"Encontré {app_name} en {path}, pero hubo un error al abrirlo: {str(e)}"
    else:
        return f"No pude encontrar la aplicación '{app_name}' instalada en tu sistema."