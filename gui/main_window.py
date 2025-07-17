import pandas as pd
from PyQt5.QtWidgets import QMainWindow

from gui.ui_elements import construir_ui
from gui.handlers.consulta_handler import manejar_consulta_saldos
from gui.handlers.resumen_handler import (
    generar_resumen_simplificado_handler,
    generar_resumen_agrupado_handler
)
from gui.handlers.export_handler import exportar_reporte_handler
from gui.utils.table_formatter import mostrar_dataframe_en_tabla


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

    def mostrar_dataframe(self, df):
        """
        Método auxiliar que delega el renderizado del DataFrame a la tabla.
        """
        mostrar_dataframe_en_tabla(self, df)
