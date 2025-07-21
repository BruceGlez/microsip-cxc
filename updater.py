import os
import sys
import requests
import shutil
from PyQt5.QtWidgets import QMessageBox

VERSION_LOCAL = "1.0.0"
URL_VERSION_JSON = "https://bruceglez.github.io/microsip-actualizador/version.json"

def get_download_path():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.abspath(os.path.dirname(__file__))

def actualizar_aplicacion(download_url):
    destino_exe = os.path.join(get_download_path(), "MicrosipTool_new.exe")

    try:
        response = requests.get(download_url, stream=True)
        response.raise_for_status()

        with open(destino_exe, "wb") as f:
            shutil.copyfileobj(response.raw, f)

        QMessageBox.information(None, "Actualización",
                                "La actualización se descargó con éxito.\nSe aplicará la próxima vez que abras la aplicación.")
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

        if version_remota and url_remoto and version_remota != VERSION_LOCAL:
            actualizar_aplicacion(url_remoto)

    except Exception as e:
        print(f"Error al verificar actualización: {e}")
