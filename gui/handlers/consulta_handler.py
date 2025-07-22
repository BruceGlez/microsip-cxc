import pandas as pd
from PyQt5.QtWidgets import QMessageBox
from conexion.conexion_firebird import conectar_firebird
from consultas.consulta_credito import obtener_saldos_credito

def manejar_consulta_saldos(ventana):
    """
    Ejecuta la consulta de saldos y actualiza el DataFrame en la ventana.
    """
    try:
        conn = conectar_firebird(ventana.db_config)
        rows, columns = obtener_saldos_credito(conn)
        ventana.df_resultado = pd.DataFrame(rows, columns=columns)
        conn.close()
        QMessageBox.information(ventana, "Consulta exitosa", "Datos cargados. Ahora puedes generar un reporte desde el menú.")
    except Exception as e:
        QMessageBox.critical(ventana, "Error", f"Ocurrió un error:\n{e}")
