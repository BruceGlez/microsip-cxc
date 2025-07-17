from PyQt5.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QLabel,
    QAction, QWidget, QGroupBox
)
from PyQt5.QtGui import QFont

def construir_ui(ventana):
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
    layout.setContentsMargins(15, 15, 15, 15)
    layout.setSpacing(10)
    central_widget.setLayout(layout)

    # Fuente general
    titulo_font = QFont("Segoe UI", 11, QFont.Bold)
    label_font = QFont("Segoe UI", 10)

    # Etiqueta tipo de cambio
    label_tc = QLabel("Tipo de cambio del día (USD):")
    label_tc.setFont(label_font)
    label_tc.setVisible(False)
    layout.addWidget(label_tc)

    # Botones en grupo
    btn_consultar = QPushButton("Consultar saldos")
    btn_consultar.setFont(titulo_font)

    btn_exportar = QPushButton("Exportar reporte")
    btn_exportar.setFont(label_font)
    btn_exportar.setVisible(False)

    acciones_box = QGroupBox("Acciones")
    acciones_layout = QHBoxLayout()
    acciones_layout.setSpacing(10)
    acciones_box.setLayout(acciones_layout)
    acciones_layout.addWidget(btn_consultar)
    acciones_layout.addWidget(btn_exportar)
    layout.addWidget(acciones_box)

    # Tabla
    table = QTableWidget()
    table.setVisible(False)
    table.setAlternatingRowColors(True)
    table.setStyleSheet("alternate-background-color: #f2f2f2;")
    layout.addWidget(table)

    # Asignar referencias
    ventana.layout = layout
    ventana.label_tc = label_tc
    ventana.btn_consultar = btn_consultar
    ventana.table = table
    ventana.btn_exportar = btn_exportar
    ventana.resumen_action = resumen_action
    ventana.agrupado_action = agrupado_action

    # Estilo general
    ventana.setStyleSheet("""
        QPushButton {
            background-color: #2e86de;
            color: white;
            padding: 8px;
            border-radius: 4px;
        }
        QPushButton:hover {
            background-color: #1b4f72;
        }
        QGroupBox {
            font-weight: bold;
            margin-top: 10px;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 3px 0 3px;
        }
    """)
