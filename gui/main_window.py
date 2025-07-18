import pandas as pd
from PyQt5.QtWidgets import QMainWindow, QMessageBox

from gui.ui_elements import construir_ui
from gui.handlers.consulta_handler import manejar_consulta_saldos
from gui.handlers.resumen_handler import (
    generar_resumen_simplificado_handler,
    generar_resumen_agrupado_handler,
)
from gui.handlers.export_handler import exportar_reporte_handler
from gui.utils.table_formatter import mostrar_dataframe_en_tabla
from consultas.consulta_fecha_adeudos import obtener_adeudos_por_fecha
from conexion.conexion_firebird import conectar_firebird


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Monitoreo de crédito - Microsip")
        self.setGeometry(100, 100, 1000, 600)

        self.df_resultado = pd.DataFrame()
        self.df_resumen = pd.DataFrame()

        # Construye la interfaz y asigna widgets a la instancia
        construir_ui(self)

        # Conectar eventos
        self.btn_consultar.clicked.connect(lambda: manejar_consulta_saldos(self))
        self.resumen_action.triggered.connect(lambda: generar_resumen_simplificado_handler(self))
        self.agrupado_action.triggered.connect(lambda: generar_resumen_agrupado_handler(self))
        self.btn_exportar.clicked.connect(lambda: exportar_reporte_handler(self))
        self.adeudos_fecha_action.triggered.connect(self.mostrar_reporte_adeudos_fecha)
        self.table.cellDoubleClicked.connect(self.on_doble_click_resumen)

    def mostrar_dataframe(self, df):
        """
        Método auxiliar que delega el renderizado del DataFrame a la tabla.
        """
        mostrar_dataframe_en_tabla(self, df)

    def mostrar_reporte_adeudos_fecha(self):
        from gui.utils.seleccion_fecha_dialog import DialogoSeleccionFecha

        dialogo = DialogoSeleccionFecha(self)
        if dialogo.exec_() != dialogo.Accepted:
            return

        fecha_inicio, fecha_fin = dialogo.obtener_fechas()

        try:
            conn = conectar_firebird()
            datos, columnas = obtener_adeudos_por_fecha(conn, fecha_inicio, fecha_fin)
            conn.close()

            if not datos:
                QMessageBox.information(self, "Sin resultados", "No se encontraron adeudos en ese rango de fechas.")
                return

            df = pd.DataFrame(datos, columns=columnas)
            self.df_resultado = df
            self.mostrar_dataframe(df)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error:\n{str(e)}")

    def on_doble_click_resumen(self, row, column):
        if not self.df_resumen.empty:
            try:
                cliente_base = str(self.df_resumen.iloc[row]["CLIENTE_BASE"])
                cliente_ids_raw = str(self.df_resumen.iloc[row]["CLIENTE_IDS"])
                cliente_ids = [int(cid) for cid in cliente_ids_raw.split(",") if cid.strip().isdigit()]
                if not cliente_ids:
                    QMessageBox.warning(self, "Sin IDs", "No se encontraron CLIENTE_IDs para este cliente.")
                    return

                # Si hay más de un ID (por moneda), mostrar todos
                from gui.handlers.resumen_handler import mostrar_detalle_cliente_multiple_ids
                mostrar_detalle_cliente_multiple_ids(self, cliente_base, cliente_ids)

            except Exception as e:
                QMessageBox.warning(self, "Error", f"No se pudo obtener el detalle del cliente.\n{str(e)}")
