from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QDialogButtonBox, QDateEdit
from PyQt5.QtCore import QDate

class DialogoSeleccionFecha(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Seleccionar rango de fechas")
        self.resize(300, 120)

        layout = QVBoxLayout(self)

        self.fecha_inicio = QDateEdit()
        self.fecha_inicio.setCalendarPopup(True)
        self.fecha_inicio.setDate(QDate.currentDate().addMonths(-1))
        layout.addWidget(QLabel("Fecha inicio:"))
        layout.addWidget(self.fecha_inicio)

        self.fecha_fin = QDateEdit()
        self.fecha_fin.setCalendarPopup(True)
        self.fecha_fin.setDate(QDate.currentDate())
        layout.addWidget(QLabel("Fecha fin:"))
        layout.addWidget(self.fecha_fin)

        botones = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        botones.accepted.connect(self.accept)
        botones.rejected.connect(self.reject)
        layout.addWidget(botones)

    def obtener_fechas(self):
        return (
            self.fecha_inicio.date().toString("yyyy-MM-dd"),
            self.fecha_fin.date().toString("yyyy-MM-dd")
        )
