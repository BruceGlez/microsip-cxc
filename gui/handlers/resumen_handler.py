import pandas as pd
from PyQt5.QtWidgets import QMessageBox
from conexion.conexion_firebird import conectar_firebird
from consultas.tipo_cambio import obtener_tipo_cambio_hoy
from reportes.resumen_simplificado import generar_resumen_simplificado
from reportes.resumen_agrupado import generar_resumen_por_cliente_base
from consultas.consulta_credito import obtener_detalle_cliente
from gui.utils.detalle_cliente_dialog import DetalleClienteDialog

def generar_resumen_simplificado_handler(ventana):
    if ventana.df_resultado.empty:
        QMessageBox.information(ventana, "Información", "Primero realiza una consulta.")
        return
    try:
        conn = conectar_firebird()
        tipo_cambio = obtener_tipo_cambio_hoy(conn)
        conn.close()

        if tipo_cambio is None:
            QMessageBox.warning(ventana, "Advertencia", "No se encontró tipo de cambio del día.")
            tipo_cambio = 0.0

        ventana.label_tc.setText(f"Tipo de cambio del día (USD): ${tipo_cambio:,.4f}")
        ventana.label_tc.setVisible(True)

        df = generar_resumen_simplificado(ventana.df_resultado)

        for col in ["TOTAL_PESOS", "TOTAL_DOLARES"]:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0.0).astype(float)

        tipo_cambio = float(tipo_cambio)
        df["TC_HOY"] = tipo_cambio
        df["TOTAL_EN_PESOS"] = df["TOTAL_PESOS"] + (df["TOTAL_DOLARES"] * tipo_cambio)

        ventana.df_resumen = df
        ventana.mostrar_dataframe(df)

    except Exception as e:
        QMessageBox.critical(ventana, "Error", str(e))


def generar_resumen_agrupado_handler(ventana):
    if ventana.df_resultado.empty:
        QMessageBox.information(ventana, "Información", "Primero realiza una consulta.")
        return
    try:
        df = generar_resumen_por_cliente_base(ventana.df_resultado)
        ventana.df_resumen = df
        ventana.mostrar_dataframe(df)
    except Exception as e:
        QMessageBox.critical(ventana, "Error", str(e))

def mostrar_detalle_cliente_desde_resumen(ventana, cliente_base):
    try:
        conn = conectar_firebird()
        cursor = conn.cursor()
        cursor.execute("SELECT CLIENTE_ID FROM CLIENTES WHERE TRIM(UPPER(NOMBRE)) LIKE ?", (cliente_base.strip().upper(),))
        row = cursor.fetchone()
        if not row:
            QMessageBox.warning(ventana, "No encontrado", f"No se encontró CLIENTE_ID para {cliente_base}")
            return
        cliente_id = row[0]

        df_saldos, df_remisiones = obtener_detalle_cliente(conn, cliente_id)
        conn.close()

        dlg = DetalleClienteDialog(cliente_base, df_saldos, df_remisiones)
        dlg.exec_()

    except Exception as e:
        QMessageBox.critical(ventana, "Error al obtener detalle", str(e))
