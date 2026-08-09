import os
import shutil
import subprocess
import sys

def build_and_zip():
    print("Iniciando construccion con PyInstaller...")
    # Run PyInstaller
    subprocess.run([sys.executable, "-m", "PyInstaller", "MikuFriend.spec", "--clean", "-y"], check=True)
    
    dist_dir = os.path.join("dist", "MikuFriend")
    zip_path = os.path.join("dist", "MikuFriend_Release")
    
    print(f"\nEmpaquetando toda la carpeta '{dist_dir}' (incluyendo dependencias)...")
    # Make sure we don't zip the .zip itself, shutil.make_archive creates it with .zip
    shutil.make_archive(zip_path, 'zip', "dist", "MikuFriend")
    
    print(f"\n¡Listo! El archivo para subir a GitHub Releases es: {zip_path}.zip")
    print("Asegurate de compartir ESTE archivo .zip completo, ya que contiene todas las dependencias necesarias.")

if __name__ == "__main__":
    build_and_zip()
