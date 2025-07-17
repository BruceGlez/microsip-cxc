from PyQt5.QtWidgets import (
    QVBoxLayout, QPushButton, QTableWidget, QLabel,
    QAction, QWidget, QMenuBar
)

def construir_ui(ventana):
    """
    Construye todos los elementos de la interfaz y los asocia a la ventana.
    """
    # Menú superior
    menubar = ventana.menuBar()
    reportes_menu = menubar.addMenu("Reportes")

    resumen_action = QAction("Resumen simplificado", ventana)
    resumen_action.setObjectName("action_resumen")
    reportes_menu.addAction(resumen_action)

    agrupado_action = QAction("Resumen agrupado", ventana)
    agrupado_action.setObjectName("action_agrupado")
    reportes_menu.addAction(agrupado_action)

    # Área central
    central_widget = QWidget()
    ventana.setCentralWidget(central_widget)
    layout = QVBoxLayout()
    central_widget.setLayout(layout)

    # Etiqueta tipo de cambio
    label_tc = QLabel("Tipo de cambio del día (USD):")
    label_tc.setVisible(False)
    layout.addWidget(label_tc)

    # Botón consulta
    btn_consultar = QPushButton("Consultar saldos")
    layout.addWidget(btn_consultar)

    # Tabla y botón exportar
    table = QTableWidget()
    table.setVisible(False)
    layout.addWidget(table)

    btn_exportar = QPushButton("Exportar reporte")
    btn_exportar.setVisible(False)
    layout.addWidget(btn_exportar)

    # Asignar referencias a la ventana
    ventana.layout = layout
    ventana.label_tc = label_tc
    ventana.btn_consultar = btn_consultar
    ventana.table = table
    ventana.btn_exportar = btn_exportar
    ventana.resumen_action = resumen_action
    ventana.agrupado_action = agrupado_action
