import subprocess

import requests
import os
import sys
import tempfile
import shutil
from PyQt5.QtWidgets import QMessageBox
from packaging import version

VERSION_LOCAL = "1.0.0"  # Cambia según la versión de esta compilación
VERSION_URL = "https://BruceGlez.github.io/microsip-actualizador/version.json"


def verificar_actualizacion():
    print(">>> Verificando versión remota...")

    try:
        response = requests.get(VERSION_URL, timeout=5)
        print(">>> Status:", response.status_code)
        print(">>> Texto JSON:", response.text)

        data = response.json()
        nueva_version = data["version"]
        url_exe = data["url"]

        print(">>> Versión local:", VERSION_LOCAL)
        print(">>> Versión remota:", nueva_version)
        print(">>> URL del ejecutable:", url_exe)

        if version.parse(nueva_version) > version.parse(VERSION_LOCAL):
            print(">>> Se detectó nueva versión.")
            reply = QMessageBox.question(None, "Actualización disponible",
                                         f"Versión {nueva_version} disponible. ¿Deseas actualizar?",
                                         QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                archivo = "actualizacion.exe"
                with open(archivo, "wb") as f:
                    f.write(requests.get(url_exe).content)
                subprocess.Popen(archivo)
                sys.exit()
        else:
            print(">>> Ya tienes la versión más reciente.")

    except Exception as e:
        print(">>> Error en la actualización:", e)

def descargar_actualizacion(url, parent=None):
    temp_path = os.path.join(tempfile.gettempdir(), "microsip_credito_actualizado.exe")
    try:
        r = requests.get(url, stream=True)
        with open(temp_path, "wb") as f:
            shutil.copyfileobj(r.raw, f)
        QMessageBox.information(parent, "Actualización lista", "La nueva versión se descargó. Se abrirá ahora.")
        os.startfile(temp_path)
        sys.exit()
    except Exception as e:
        QMessageBox.critical(parent, "Error", f"No se pudo descargar:\n{e}")
