from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QSizePolicy
from PyQt5.QtCore import Qt
import pandas as pd

class DetalleClienteDialog(QDialog):
    def __init__(self, cliente_nombre, df_saldos, df_remisiones):
        super().__init__()
        self.setWindowTitle(f"Detalle del Cliente: {cliente_nombre}")
        self.setMinimumSize(1200, 800)

        layout = QVBoxLayout()

        # ✅ Asegurar que la columna MONEDA_ID exista (aunque los DataFrames estén vacíos)
        if "MONEDA_ID" not in df_saldos.columns:
            df_saldos["MONEDA_ID"] = None

        if "MONEDA_ID" not in df_remisiones.columns:
            df_remisiones["MONEDA_ID"] = None

        # SALDOS_CC - PESOS
        layout.addWidget(QLabel("SALDOS_CC - PESOS"))
        df_saldos_pesos = df_saldos[df_saldos["MONEDA_ID"] == 1]
        layout.addWidget(self.crear_tabla(df_saldos_pesos))

        # SALDOS_CC - DÓLARES
        layout.addWidget(QLabel("SALDOS_CC - DÓLARES"))
        df_saldos_dolares = df_saldos[df_saldos["MONEDA_ID"] == 620]
        layout.addWidget(self.crear_tabla(df_saldos_dolares))

        # REMISIONES - PESOS
        layout.addWidget(QLabel("REMISIONES PENDIENTES - PESOS"))
        df_rem_pesos = df_remisiones[df_remisiones["MONEDA_ID"] == 1]
        layout.addWidget(self.crear_tabla(df_rem_pesos))

        # REMISIONES - DÓLARES
        layout.addWidget(QLabel("REMISIONES PENDIENTES - DÓLARES"))
        df_rem_dolares = df_remisiones[df_remisiones["MONEDA_ID"] == 620]
        layout.addWidget(self.crear_tabla(df_rem_dolares))

        self.setLayout(layout)

    def crear_tabla(self, df: pd.DataFrame):
        table = QTableWidget()
        table.setColumnCount(len(df.columns))
        table.setHorizontalHeaderLabels(df.columns.tolist())
        table.setRowCount(len(df))

        for i, row in df.iterrows():
            for j, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                item.setFlags(item.flags() ^ Qt.ItemIsEditable)  # Solo lectura
                table.setItem(i, j, item)

        table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        table.resizeColumnsToContents()
        return table
