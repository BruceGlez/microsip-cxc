import os
import shutil
import subprocess
import time
import json
import requests
import tkinter as tk
from threading import Thread

MAIN_EXE = "MicrosipTool.exe"
NEW_EXE = "MicrosipTool_new.exe"
BACKUP_EXE = "MicrosipTool_old.exe"
VERSION_FILE = "version.json"
REMOTE_VERSION_URL = "https://raw.githubusercontent.com/BruceGlez/microsip-cxc/master/version.json"
ICON_PATH = "icon.ico"

def get_local_version():
    try:
        if os.path.exists(VERSION_FILE):
            with open(VERSION_FILE, "r") as f:
                data = json.load(f)
                return data.get("version", "unknown")
    except Exception as e:
        print("❌ Error reading local version:", e)
    return "unknown"

def get_remote_version():
    try:
        response = requests.get(REMOTE_VERSION_URL, timeout=5)
        if response.ok:
            data = response.json()
            return data.get("version", "unknown")
        else:
            print(f"❌ Remote fetch failed: HTTP {response.status_code}")
    except Exception as e:
        print("❌ Error fetching remote version:", e)
    return "unknown"

def aplicar_actualizacion_si_pendiente(update_gui=None):
    if os.path.exists(NEW_EXE):
        if update_gui:
            update_gui("🔁 Actualización detectada...")

        if os.path.exists(MAIN_EXE):
            shutil.move(MAIN_EXE, BACKUP_EXE)
            if update_gui:
                update_gui("📦 Versión anterior respaldada.")

        shutil.move(NEW_EXE, MAIN_EXE)
        if update_gui:
            update_gui("✅ Nueva versión instalada.")

def lanzar_aplicacion():
    subprocess.Popen([MAIN_EXE], shell=True)

def launch_logic(gui_ref):
    local_ver = get_local_version()
    remote_ver = get_remote_version()

    gui_ref.set_status(f"📦 Versión local: {local_ver}")
    time.sleep(1)
    gui_ref.set_status(f"🌐 Versión remota: {remote_ver}")
    time.sleep(1)

    if local_ver != remote_ver or os.path.exists(NEW_EXE):
        aplicar_actualizacion_si_pendiente(update_gui=gui_ref.set_status)
        time.sleep(1)

    gui_ref.set_status("🚀 Iniciando aplicación...")
    time.sleep(1)
    lanzar_aplicacion()
    gui_ref.root.destroy()

class LauncherGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Microsip CXC Launcher")
        self.root.geometry("350x100")
        self.root.resizable(False, False)

        if os.path.exists(ICON_PATH):
            try:
                self.root.iconbitmap(ICON_PATH)
            except:
                pass

        self.label = tk.Label(self.root, text="🔍 Verificando actualizaciones...", font=("Arial", 10))
        self.label.pack(pady=20)

        Thread(target=launch_logic, args=(self,), daemon=True).start()

    def set_status(self, text):
        self.label.config(text=text)
        self.root.update()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = LauncherGUI()
    app.run()
