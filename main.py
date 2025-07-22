# -*- coding: utf-8 -*-
import os
import sys
import shutil
import time
from PyQt5.QtWidgets import QApplication, QMessageBox
from gui.main_window import MainWindow
from singleton import verificar_instancia_unica

def aplicar_actualizacion_si_pendiente():
    exe_path = os.path.abspath(sys.argv[0])
    exe_dir = os.path.dirname(exe_path)
    nuevo_exe = os.path.join(exe_dir, "MicrosipTool_new.exe")

    if os.path.exists(nuevo_exe):
        try:
            backup = exe_path + ".bak"
            os.rename(exe_path, backup)
            shutil.move(nuevo_exe, exe_path)
            os.execv(exe_path, sys.argv)
        except Exception as e:
            print(f"Error aplicando actualización: {e}")
            QMessageBox.critical(None, "Error", f"No se pudo aplicar la actualización:\n{e}")
    else:
        try:
            os.remove(exe_path + ".bak")
        except Exception:
            pass

aplicar_actualizacion_si_pendiente()

if __name__ == "__main__":
    time.sleep(2)

    instancia = verificar_instancia_unica()
    if not instancia:
        QMessageBox.critical(None, "Ya está en ejecución", "La aplicación ya está corriendo.")
        sys.exit(1)

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()
    instancia.release()
