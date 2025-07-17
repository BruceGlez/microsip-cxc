import requests
import os
import sys
import tempfile
import subprocess
import shutil
from packaging import version
from PyQt5.QtWidgets import QMessageBox, QProgressDialog, QApplication
from PyQt5.QtCore import Qt

VERSION_LOCAL = "1.0.0"
VERSION_URL = "https://BruceGlez.github.io/microsip-actualizador/version.json"

def verificar_actualizacion(parent=None):
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
            reply = QMessageBox.question(parent, "Actualización disponible",
                                         f"Versión {nueva_version} disponible. ¿Deseas actualizar?",
                                         QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                temp_dir = tempfile.mkdtemp()
                archivo_destino = os.path.join(temp_dir, "microsip_credito_actualizado.exe")

                # Obtener tamaño total
                head = requests.head(url_exe)
                total_size = int(head.headers.get("Content-Length", 0))

                # Barra de progreso
                progress = QProgressDialog("Descargando actualización...", "Cancelar", 0, total_size, parent)
                progress.setWindowModality(Qt.WindowModal)
                progress.setMinimumDuration(0)
                progress.setValue(0)

                try:
                    with requests.get(url_exe, stream=True) as r, open(archivo_destino, "wb") as f:
                        descargado = 0
                        for chunk in r.iter_content(chunk_size=8192):
                            if chunk:
                                f.write(chunk)
                                descargado += len(chunk)
                                progress.setValue(descargado)
                                QApplication.processEvents()
                                if progress.wasCanceled():
                                    return

                    progress.close()
                    QMessageBox.information(parent, "Actualización lista", "La nueva versión se descargó. Se abrirá ahora.")
                    subprocess.Popen(archivo_destino)
                    sys.exit()

                except Exception as e:
                    progress.close()
                    QMessageBox.critical(parent, "Error", f"No se pudo descargar la actualización:\n{e}")

        else:
            print(">>> Ya tienes la versión más reciente.")

    except Exception as e:
        print(">>> Error en la actualización:", e)
