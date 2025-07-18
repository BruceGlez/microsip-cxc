
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

        # Asegurar tipos numéricos y calcular TOTAL_EN_PESOS
        for col in ["TOTAL_PESOS", "TOTAL_DOLARES"]:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0.0).astype(float)

        tipo_cambio = float(tipo_cambio)
        df["TC_HOY"] = tipo_cambio
        df["TOTAL_EN_PESOS"] = df["TOTAL_PESOS"] + (df["TOTAL_DOLARES"] * tipo_cambio)

        # Guardar CLIENTE_IDS internamente y luego ocultarla
        if "CLIENTE_IDS" in df.columns:
            ventana._cliente_ids_mapa = df[["CLIENTE_BASE", "CLIENTE_IDS"]].set_index("CLIENTE_BASE").to_dict()["CLIENTE_IDS"]
            df.drop(columns=["CLIENTE_IDS"], inplace=True)

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

def mostrar_detalle_cliente_por_moneda(ventana, cliente_base, cliente_id, moneda_id):
    try:
        conn = conectar_firebird()

        # Obtener datos del cliente
        df_saldos, df_remisiones = obtener_detalle_cliente(conn, cliente_id)

        # Como el cliente_id ya representa una moneda específica, no se filtran saldos
        df_saldos_total = df_saldos.copy()

        # Las remisiones sí se filtran por la moneda
        df_remisiones["MONEDA_ID"] = pd.to_numeric(df_remisiones["MONEDA_ID"], errors="coerce").fillna(0).astype(int)
        df_remisiones_total = df_remisiones[df_remisiones["MONEDA_ID"] == moneda_id]

        conn.close()

        if df_saldos_total.empty:
            df_saldos_total = pd.DataFrame(columns=["DOCUMENTO", "SALDO"])
        if df_remisiones_total.empty:
            df_remisiones_total = pd.DataFrame(columns=["MONEDA_ID", "DOCUMENTO", "IMPORTE"])

        dlg = DetalleClienteDialog(cliente_base, df_saldos_total, df_remisiones_total)
        dlg.exec_()

    except Exception as e:
        QMessageBox.critical(ventana, "Error al obtener detalle", str(e))

