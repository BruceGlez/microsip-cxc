from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QSizePolicy
from PyQt5.QtCore import Qt
import pandas as pd

class DetalleClienteDialog(QDialog):
    def __init__(self, cliente_nombre, df_saldos, df_remisiones):
        super().__init__()
        self.setWindowTitle(f"Detalle del Cliente: {cliente_nombre}")
        self.setMinimumSize(1000, 700)

        layout = QVBoxLayout()

        # DEBUG: imprimir ambos DataFrames
        print(f"🧾 Mostrando ventana para {cliente_nombre}")
        print("SALDOS_CC:")
        print(df_saldos)
        print("REMISIONES:")
        print(df_remisiones)

        if not df_saldos.empty:
            layout.addWidget(QLabel("SALDOS_CC"))
            layout.addWidget(self.crear_tabla(df_saldos))

        if not df_remisiones.empty:
            layout.addWidget(QLabel("REMISIONES PENDIENTES"))
            layout.addWidget(self.crear_tabla(df_remisiones))

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
