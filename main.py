import os
import sys
import time
from PyQt5.QtWidgets import QApplication, QMessageBox
from gui.main_window import MainWindow
from singleton import verificar_instancia_unica
from updater import verificar_actualizacion, VERSION_LOCAL

def log_actualizacion(msg):
    from datetime import datetime
    with open("actualizacion.log", "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}\n")

if __name__ == "__main__":
    time.sleep(2)

    instancia = verificar_instancia_unica()
    if not instancia:
        log_actualizacion("Instancia bloqueada. Ya hay una en ejecución.")
        QMessageBox.critical(None, "Ya está en ejecución", "La aplicación ya está corriendo.")
        sys.exit(1)

    app = QApplication(sys.argv)
    window = MainWindow()

    try:
        verificar_actualizacion(parent=window)
    except Exception as e:
        log_actualizacion(f"Error al verificar actualización: {e}")

    if os.path.exists("actualizado.txt"):
        log_actualizacion("Se detecto actualizado.txt")
        QMessageBox.information(None, "Actualización completada",
                                f"La aplicación se ha actualizado correctamente a la versión {VERSION_LOCAL}.")
        try:
            os.remove("actualizado.txt")
        except Exception as e:
            log_actualizacion(f"No se pudo borrar actualizado.txt: {e}")

    window.show()
    app.exec_()

    instancia.release()
    log_actualizacion("Aplicación cerrada correctamente.")
