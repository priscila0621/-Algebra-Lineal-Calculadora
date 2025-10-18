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

        subtitle = QLabel("Selecciona una operaci\u00F3n.")
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

        btn_suma = QPushButton("Suma de matrices"); btn_suma.setMinimumHeight(44)
        btn_suma.clicked.connect(self._open_suma); lay.addWidget(btn_suma)
        btn_resta = QPushButton("Resta de matrices"); btn_resta.setMinimumHeight(44)
        btn_resta.clicked.connect(self._open_resta); lay.addWidget(btn_resta)
        btn_mult = QPushButton("Multiplicaci\u00F3n de matrices"); btn_mult.setMinimumHeight(44)
        btn_mult.clicked.connect(self._open_mult); lay.addWidget(btn_mult)
        btn_det = QPushButton("Determinantes"); btn_det.setMinimumHeight(44)
        btn_det.clicked.connect(self._open_det); lay.addWidget(btn_det)
        btn_trans = QPushButton("Transpuesta de matriz"); btn_trans.setMinimumHeight(44)
        btn_trans.clicked.connect(self._open_trans); lay.addWidget(btn_trans)
        btn_inv = QPushButton("Inversa de matriz"); btn_inv.setMinimumHeight(44)
        btn_inv.clicked.connect(self._open_inv); lay.addWidget(btn_inv)

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

    def _open_suma(self):
        from .matrices_qt import SumaMatricesWindow
        w = SumaMatricesWindow(parent=self)
        w.showMaximized(); self._child = w

    def _open_resta(self):
        from .matrices_qt import RestaMatricesWindow
        w = RestaMatricesWindow(parent=self)
        w.showMaximized(); self._child = w

    def _open_mult(self):
        from .matrices_qt import MultiplicacionMatricesWindow
        w = MultiplicacionMatricesWindow(parent=self)
        w.showMaximized(); self._child = w

    def _open_det(self):
        from .matrices_qt import DeterminanteMatrizWindow
        w = DeterminanteMatrizWindow(parent=self)
        w.showMaximized(); self._child = w

    def _open_trans(self):
        from .matrices_qt import TranspuestaMatrizWindow
        w = TranspuestaMatrizWindow(parent=self)
        w.showMaximized(); self._child = w



    def _open_inv(self):
        from .matrices_qt import InversaMatrizWindow
        w = InversaMatrizWindow(parent=self)
        w.showMaximized(); self._child = w



