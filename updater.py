import requests
import os
import sys
import tempfile
import shutil
from PyQt5.QtWidgets import QMessageBox

VERSION_LOCAL = "1.0.0"  # Cambia según la versión de esta compilación
VERSION_URL = "https://tu-servidor.com/version.json"  # URL remota del JSON

def verificar_actualizacion(parent=None):
    try:
        response = requests.get(VERSION_URL, timeout=5)
        if response.status_code == 200:
            data = response.json()
            version_remota = data.get("version")
            url_actualizacion = data.get("url")
            if version_remota > VERSION_LOCAL:
                respuesta = QMessageBox.question(parent, "Actualización disponible",
                    f"Versión {version_remota} disponible. ¿Deseas actualizar ahora?",
                    QMessageBox.Yes | QMessageBox.No)
                if respuesta == QMessageBox.Yes:
                    descargar_actualizacion(url_actualizacion, parent)
    except Exception as e:
        print(f"[Actualizador] Error al verificar: {e}")

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
