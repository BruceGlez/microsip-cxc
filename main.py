import os
import sys
import pandas as pd
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton,
    QTableWidget, QTableWidgetItem, QAction, QFileDialog, QMessageBox, QLabel
)

from conexion.conexion_firebird import conectar_firebird
from consultas.consulta_credito import obtener_saldos_credito
from reportes.resumen_simplificado import generar_resumen_simplificado
from reportes.resumen_agrupado import generar_resumen_por_cliente_base
from utils.exportar_excel import exportar_df_excel
from consultas.tipo_cambio import obtener_tipo_cambio_hoy
from updater import verificar_actualizacion
from singleton import verificar_instancia_unica

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Monitoreo de crédito - Microsip")
        self.setGeometry(100, 100, 1000, 600)

        self.df_resultado = pd.DataFrame()
        self.df_resumen = pd.DataFrame()

        self.init_ui()

    def init_ui(self):
        # Menú superior
        menubar = self.menuBar()
        reportes_menu = menubar.addMenu("Reportes")

        resumen_action = QAction("Resumen simplificado", self)
        resumen_action.triggered.connect(self.generar_resumen_simplificado)
        reportes_menu.addAction(resumen_action)

        agrupado_action = QAction("Resumen agrupado", self)
        agrupado_action.triggered.connect(self.generar_resumen_agrupado)
        reportes_menu.addAction(agrupado_action)

        # Área principal
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.layout = QVBoxLayout()
        central_widget.setLayout(self.layout)

        # Etiqueta para mostrar el tipo de cambio
        self.label_tc = QLabel("Tipo de cambio del día (USD):")
        self.label_tc.setVisible(False)
        self.layout.addWidget(self.label_tc)

        # Botón de consulta
        self.btn_consultar = QPushButton("Consultar saldos")
        self.btn_consultar.clicked.connect(self.consultar_saldos)
        self.layout.addWidget(self.btn_consultar)

        # Tabla y botón de exportación: ocultos inicialmente
        self.table = QTableWidget()
        self.table.setVisible(False)
        self.layout.addWidget(self.table)

        self.btn_exportar = QPushButton("Exportar reporte")
        self.btn_exportar.clicked.connect(self.exportar_reporte)
        self.btn_exportar.setVisible(False)
        self.layout.addWidget(self.btn_exportar)

    def consultar_saldos(self):
        try:
            conn = conectar_firebird()
            rows, columns = obtener_saldos_credito(conn)
            self.df_resultado = pd.DataFrame(rows, columns=columns)
            conn.close()
            QMessageBox.information(self, "Consulta exitosa", "Datos cargados. Ahora puedes generar un reporte desde el menú.")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def generar_resumen_simplificado(self):
        if self.df_resultado.empty:
            QMessageBox.information(self, "Información", "Primero realiza una consulta.")
            return
        try:
            conn = conectar_firebird()
            tipo_cambio = obtener_tipo_cambio_hoy(conn)
            conn.close()

            if tipo_cambio is None:
                QMessageBox.warning(self, "Advertencia", "No se encontró tipo de cambio del día.")
                tipo_cambio = 0.0

            # Mostrar el TC en la etiqueta superior
            self.label_tc.setText(f"Tipo de cambio del día (USD): ${tipo_cambio:,.4f}")
            self.label_tc.setVisible(True)

            self.df_resumen = generar_resumen_simplificado(self.df_resultado)

            # Convertir columnas monetarias a float
            for col in ["TOTAL_PESOS", "TOTAL_DOLARES"]:
                if col in self.df_resumen.columns:
                    self.df_resumen[col] = pd.to_numeric(self.df_resumen[col], errors='coerce').fillna(0.0).astype(
                        float)

            # Asegurar que el tipo de cambio también sea float
            tipo_cambio = float(tipo_cambio)

            # Agregar columnas derivadas
            self.df_resumen["TC_HOY"] = tipo_cambio
            self.df_resumen["TOTAL_EN_PESOS"] = (
                    self.df_resumen["TOTAL_PESOS"] + (self.df_resumen["TOTAL_DOLARES"] * tipo_cambio)
            )

            self.mostrar_dataframe(self.df_resumen)

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def generar_resumen_agrupado(self):
        if self.df_resultado.empty:
            QMessageBox.information(self, "Información", "Primero realiza una consulta.")
            return
        try:
            self.df_resumen = generar_resumen_por_cliente_base(self.df_resultado)
            self.mostrar_dataframe(self.df_resumen)
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def mostrar_dataframe(self, df):
        self.table.setVisible(True)
        self.btn_exportar.setVisible(True)

        self.table.clear()
        self.table.setColumnCount(len(df.columns))
        self.table.setRowCount(len(df.index))
        self.table.setHorizontalHeaderLabels(df.columns)

        columnas_moneda = [
            col for col in df.columns
            if any(key in col.upper() for key in ["PESOS", "DOLARES", "SALDO", "TOTAL", "IMPORTE"])
        ]

        for i in range(len(df.index)):
            for j in range(len(df.columns)):
                col_name = df.columns[j]
                valor = df.iat[i, j]

                if col_name in columnas_moneda and pd.notnull(valor):
                    try:
                        valor = float(valor)
                        texto = f"${valor:,.2f}"
                    except:
                        texto = str(valor)
                else:
                    texto = str(valor)

                self.table.setItem(i, j, QTableWidgetItem(texto))

    def exportar_reporte(self):
        if self.df_resumen.empty:
            return
        path, _ = QFileDialog.getSaveFileName(
            self, "Guardar archivo", "reporte.xlsx", "Archivos Excel (*.xlsx)"
        )
        if path:
            success, error = exportar_df_excel(self.df_resumen, path)
            if success:
                QMessageBox.information(self, "Éxito", "Reporte exportado correctamente.")
            else:
                QMessageBox.critical(self, "Error", error)


import time
from datetime import datetime

def log_actualizacion(msg):
    with open("actualizacion.log", "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}\n")

if __name__ == "__main__":
    # Permite que el nuevo .exe tenga tiempo de iniciar si viene del updater.bat
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

    # Mostrar mensaje si fue recién actualizado
    if os.path.exists("actualizado.txt"):
        log_actualizacion("Se detecto actualizado.txt")
        from updater import VERSION_LOCAL  # importar la versión local

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




