from PyQt5.QtWidgets import QTableWidgetItem
import pandas as pd

def mostrar_dataframe_en_tabla(ventana, df):
    """
    Llena el widget de tabla con los datos del DataFrame y los muestra.
    """
    ventana.table.setVisible(True)
    ventana.btn_exportar.setVisible(True)

    ventana.table.clear()
    ventana.table.setColumnCount(len(df.columns))
    ventana.table.setRowCount(len(df.index))
    ventana.table.setHorizontalHeaderLabels(df.columns)

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

            ventana.table.setItem(i, j, QTableWidgetItem(texto))
