import os
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLineEdit, QPushButton,
    QFileDialog, QMessageBox, QHBoxLayout
)

class ConfiguracionConexionDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Conexión a base de datos")
        self.setMinimumWidth(400)
        self.config = None  # Stores connection config

        layout = QVBoxLayout(self)
        form = QFormLayout()

        self.host_input = QLineEdit()
        form.addRow("Servidor:", self.host_input)

        self.database_input = QLineEdit()
        db_btn = QPushButton("📁")
        db_btn.setFixedWidth(30)
        db_btn.clicked.connect(self.browse_database)
        db_layout = QHBoxLayout()
        db_layout.addWidget(self.database_input)
        db_layout.addWidget(db_btn)
        form.addRow("Archivo .FDB:", db_layout)

        self.user_input = QLineEdit()
        form.addRow("Usuario:", self.user_input)

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        form.addRow("Contraseña:", self.password_input)

        layout.addLayout(form)

        self.test_button = QPushButton("🔍 Probar conexión")
        self.test_button.clicked.connect(self.test_connection)

        self.ok_button = QPushButton("Aceptar")
        self.ok_button.clicked.connect(self._on_accept)

        buttons = QHBoxLayout()
        buttons.addWidget(self.test_button)
        buttons.addWidget(self.ok_button)
        layout.addLayout(buttons)

    def browse_database(self):
        path, _ = QFileDialog.getOpenFileName(self, "Seleccionar archivo FDB", "", "Archivos FDB (*.fdb)")
        if path:
            self.database_input.setText(path)

    def get_connection_config(self):
        return {
            "host": self.host_input.text().strip(),
            "database": self.database_input.text().strip(),
            "user": self.user_input.text().strip(),
            "password": self.password_input.text(),
            "charset": "UTF8"
        }

    def test_connection(self):
        from conexion.conexion_firebird import conectar_firebird
        try:
            conn = conectar_firebird(self.get_connection_config())
            conn.close()
            QMessageBox.information(self, "Éxito", "✅ Conexión exitosa.")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def _on_accept(self):
        self.config = self.get_connection_config()
        self.accept()
