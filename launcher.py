import os
import sys
import json
import zipfile
import shutil
import urllib.request
import tkinter as tk
from tkinter import messagebox

VERSION_FILE = "version.json"
REMOTE_VERSION_URL = "https://raw.githubusercontent.com/BruceGlez/microsip-cxc/master/version.json"
ZIP_URL = "https://github.com/BruceGlez/microsip-cxc/archive/refs/heads/master.zip"
EXTRACTED_FOLDER = "microsip-cxc-master"

def show_message(title, text):
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo(title, text)

def get_local_version():
    if not os.path.exists(VERSION_FILE):
        return "0.0.0"
    try:
        with open(VERSION_FILE, "r") as f:
            return json.load(f).get("version", "0.0.0")
    except:
        return "0.0.0"

def get_remote_version():
    try:
        with urllib.request.urlopen(REMOTE_VERSION_URL, timeout=5) as response:
            data = json.loads(response.read().decode())
            return data.get("version", "0.0.0")
    except:
        return None

def download_and_extract_zip():
    zip_path = "update.zip"
    urllib.request.urlretrieve(ZIP_URL, zip_path)

    if os.path.exists(EXTRACTED_FOLDER):
        shutil.rmtree(EXTRACTED_FOLDER)

    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(".")

    os.remove(zip_path)

    # Copy contents to current dir
    for item in os.listdir(EXTRACTED_FOLDER):
        s = os.path.join(EXTRACTED_FOLDER, item)
        d = os.path.join(".", item)
        if os.path.isdir(s):
            if os.path.exists(d):
                shutil.rmtree(d)
            shutil.copytree(s, d)
        else:
            shutil.copy2(s, d)

    shutil.rmtree(EXTRACTED_FOLDER)

def install_dependencies():
    if os.path.exists("requirements.txt"):
        os.system(f"{sys.executable} -m pip install -r requirements.txt")

def run_main():
    if os.path.exists("main.py"):
        print("▶️ Ejecutando main.py...")
        os.system(f"{sys.executable} main.py")
    else:
        show_message("Error", "No se encontró main.py.")

def main():
    local_version = get_local_version()
    remote_version = get_remote_version()

    if not remote_version:
        show_message("Error", "No se pudo obtener la versión remota.")
        return

    if local_version != remote_version:
        show_message("Actualización", f"Nueva versión disponible ({remote_version}). Actualizando...")
        download_and_extract_zip()
        show_message("Actualización", "Actualización completada.")
    else:
        print("✅ Ya tienes la última versión.")

    install_dependencies()
    run_main()

if __name__ == "__main__":
    main()
