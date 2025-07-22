import sys
import json
import pandas as pd
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QAction

from gui.ui_elements import construir_ui
from gui.handlers.consulta_handler import manejar_consulta_saldos
from gui.handlers.resumen_handler import (
    generar_resumen_simplificado_handler,
    generar_resumen_agrupado_handler,
    mostrar_detalle_cliente_por_moneda,
)
from gui.handlers.export_handler import exportar_reporte_handler
from gui.utils.table_formatter import mostrar_dataframe_en_tabla
from consultas.consulta_fecha_adeudos import obtener_adeudos_por_fecha
from conexion.conexion_firebird import conectar_firebird
from gui.components.dialogs.configuracion_conexion_dialog import ConfiguracionConexionDialog


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Monitoreo de crédito - Microsip")
        self.setGeometry(100, 100, 1000, 600)

        # 🚀 Solicitar configuración de conexión al inicio
        self.db_config = self.solicitar_configuracion_conexion()
        if self.db_config is None:
            QMessageBox.critical(self, "Sin conexión", "No se proporcionaron datos de conexión.")
            sys.exit(1)

        self.df_resultado = pd.DataFrame()
        self.df_resumen = pd.DataFrame()
        self._cliente_ids_mapa = {}  # 🔧 Inicializar para evitar errores

        # Construir UI
        construir_ui(self)

        # Menú de configuración para cambiar conexión
        config_menu = self.menuBar().addMenu("Configuración")
        conexion_action = QAction("Cambiar conexión", self)
        conexion_action.triggered.connect(self.abrir_dialogo_conexion)
        config_menu.addAction(conexion_action)

        # Conectar eventos
        self.btn_consultar.clicked.connect(lambda: manejar_consulta_saldos(self))
        self.resumen_action.triggered.connect(lambda: generar_resumen_simplificado_handler(self))
        # self.agrupado_action.triggered.connect(lambda: generar_resumen_agrupado_handler(self))
        self.btn_exportar.clicked.connect(lambda: exportar_reporte_handler(self))
        # self.adeudos_fecha_action.triggered.connect(self.mostrar_reporte_adeudos_fecha)
        self.table.cellDoubleClicked.connect(self.on_doble_click_resumen)

    def solicitar_configuracion_conexion(self):
        dialog = ConfiguracionConexionDialog(self)
        if dialog.exec_() == dialog.Accepted:
            return dialog.config
        return None

    def abrir_dialogo_conexion(self):
        nueva_config = self.solicitar_configuracion_conexion()
        if nueva_config:
            self.db_config = nueva_config

    def mostrar_dataframe(self, df):
        """
        Muestra un DataFrame en la tabla principal.
        """
        mostrar_dataframe_en_tabla(self, df)

    def mostrar_reporte_adeudos_fecha(self):
        from gui.utils.seleccion_fecha_dialog import DialogoSeleccionFecha

        dialogo = DialogoSeleccionFecha(self)
        if dialogo.exec_() != dialogo.Accepted:
            return

        fecha_inicio, fecha_fin = dialogo.obtener_fechas()

        try:
            conn = conectar_firebird(self.db_config)
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
        if self.df_resumen is None or self.df_resumen.empty:
            return

        df = self.df_resumen
        cliente_base = df.iloc[row]["CLIENTE_BASE"]
        cliente_ids_raw = self._cliente_ids_mapa.get(cliente_base, "{}")

        # Obtener moneda seleccionada
        if column == df.columns.get_loc("TOTAL_PESOS"):
            moneda_id = 1
        elif column == df.columns.get_loc("TOTAL_DOLARES"):
            moneda_id = 620
        else:
            return

        # Parsear CLIENTE_ID correcto según la moneda
        try:
            cliente_ids_dict = json.loads(cliente_ids_raw)
            cliente_id = cliente_ids_dict.get(str(moneda_id))
        except Exception:
            QMessageBox.warning(self, "Error", "CLIENTE_IDS mal formateado.")
            return

        if not cliente_id:
            QMessageBox.warning(self, "No encontrado",
                                f"No se encontró CLIENTE_ID para {cliente_base} y moneda {moneda_id}.")
            return

        mostrar_detalle_cliente_por_moneda(self, cliente_base, int(cliente_id), moneda_id)
