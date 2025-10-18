from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFrame
)
from PySide6.QtCore import Qt
from .theme import make_theme_toggle_button, install_toggle_shortcut


class MenuMatricesWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Operaciones con Matrices")

        outer = QWidget()
        self.setCentralWidget(outer)
        outer_lay = QVBoxLayout(outer)
        outer_lay.setContentsMargins(24, 24, 24, 24)
        outer_lay.setSpacing(18)

        row = QHBoxLayout()
        outer_lay.addLayout(row)
        row.addStretch(1)
        card = QFrame()
        card.setObjectName("Card")
        card.setMaximumWidth(1000)
        row.addWidget(card, 1)
        row.addStretch(1)

        lay = QVBoxLayout(card)
        lay.setContentsMargins(28, 28, 28, 28)
        lay.setSpacing(16)

        title = QLabel("Operaciones con Matrices")
        title.setObjectName("Title")
        lay.addWidget(title)

        subtitle = QLabel("Selecciona una operación. La migración a Qt continuará módulo por módulo.")
        subtitle.setObjectName("Subtitle")
        lay.addWidget(subtitle)

        actions = QHBoxLayout()
        # Botón Volver a la izquierda
        btn_back = QPushButton("Volver")
        btn_back.clicked.connect(self._go_back)
        actions.addWidget(btn_back)
        actions.addStretch(1)
        actions.addWidget(make_theme_toggle_button(self))
        lay.addLayout(actions)

        ops = [
            "Suma de matrices",
            "Resta de matrices",
            "Multiplicación de matrices",
            "Determinantes",
            "Inversa de matriz",
            "Transpuesta de matriz",
        ]
        for txt in ops:
            b = QPushButton(txt)
            b.setMinimumHeight(44)
            b.setEnabled(False)
            lay.addWidget(b)

        lay.addStretch(1)

        install_toggle_shortcut(self)

    def _go_back(self):
        try:
            p = self.parent()
            self.close()
            if p is not None:
                p.show()
                p.activateWindow()
        except Exception:
            self.close()
