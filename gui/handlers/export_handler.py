from PyQt5.QtWidgets import QFileDialog, QMessageBox
from utils.exportar_excel import exportar_df_excel

def exportar_reporte_handler(ventana):
    if ventana.df_resumen.empty:
        return

    path, _ = QFileDialog.getSaveFileName(
        ventana, "Guardar archivo", "reporte.xlsx", "Archivos Excel (*.xlsx)"
    )
    if path:
        success, error = exportar_df_excel(ventana.df_resumen, path)
        if success:
            QMessageBox.information(ventana, "Éxito", "Reporte exportado correctamente.")
        else:
            QMessageBox.critical(ventana, "Error", error)
