import os
import sys
import requests
import shutil
import hashlib
from packaging import version
from PyQt5.QtWidgets import QMessageBox

VERSION_LOCAL = "1.0.0"
URL_VERSION_JSON = "https://bruceglez.github.io/microsip-actualizador/version.json"

def get_download_path():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.abspath(os.path.dirname(__file__))

def calcular_sha256(filepath):
    sha256 = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256.update(chunk)
    return sha256.hexdigest()

def actualizar_aplicacion(download_url, expected_hash):
    destino_exe = os.path.join(get_download_path(), "MicrosipTool_new.exe")

    try:
        response = requests.get(download_url, stream=True)
        response.raise_for_status()

        with open(destino_exe, "wb") as f:
            shutil.copyfileobj(response.raw, f)

        hash_descargado = calcular_sha256(destino_exe)
        if hash_descargado != expected_hash:
            QMessageBox.critical(None, "Error de Integridad",
                                 "El archivo descargado no coincide con el hash esperado.\nActualización cancelada.")
            os.remove(destino_exe)
            return

        QMessageBox.information(None, "Actualización",
                                "La actualización se descargó y verificó con éxito.\nSe aplicará la próxima vez que abras la aplicación.")
    except Exception as e:
        print(f"Error downloading update: {e}")
        QMessageBox.critical(None, "Error de Actualización", f"No se pudo descargar la actualización:\n{e}")

def verificar_actualizacion(parent=None):
    try:
        response = requests.get(URL_VERSION_JSON)
        response.raise_for_status()
        data = response.json()

        version_remota = data.get("version")
        url_remoto = data.get("url")
        hash_remoto = data.get("sha256")

        if version_remota and url_remoto and hash_remoto:
            if version.parse(version_remota) > version.parse(VERSION_LOCAL):
                actualizar_aplicacion(url_remoto, hash_remoto)

    except Exception as e:
        print(f"Error al verificar actualización: {e}")
