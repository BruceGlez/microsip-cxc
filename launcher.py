import os
import shutil
import subprocess
import time

MAIN_EXE = "MicrosipTool.exe"
NEW_EXE = "MicrosipTool_new.exe"
BACKUP_EXE = "MicrosipTool_old.exe"

def aplicar_actualizacion_si_pendiente():
    if os.path.exists(NEW_EXE):
        print("🔁 Actualización detectada. Reemplazando ejecutable...")

        # Backup the current version
        if os.path.exists(MAIN_EXE):
            shutil.move(MAIN_EXE, BACKUP_EXE)

        # Replace with the new version
        shutil.move(NEW_EXE, MAIN_EXE)

        print("✅ Reemplazo completo.")

def lanzar_aplicacion():
    print("🚀 Iniciando aplicación actualizada...")
    subprocess.Popen([MAIN_EXE], shell=True)

if __name__ == "__main__":
    aplicar_actualizacion_si_pendiente()
    time.sleep(1)  # Ensure file operations finish
    lanzar_aplicacion()
