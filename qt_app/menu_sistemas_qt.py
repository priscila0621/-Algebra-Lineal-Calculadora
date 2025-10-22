from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFrame
)
from PySide6.QtCore import Qt
from .theme import make_theme_toggle_button, install_toggle_shortcut


class MenuSistemasWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Resolver sistemas de ecuaciones lineales")

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

        title = QLabel("Resolver sistemas de ecuaciones lineales")
        title.setObjectName("Title")
        lay.addWidget(title)

        subtitle = QLabel("Elige el método que deseas utilizar.")
        subtitle.setObjectName("Subtitle")
        lay.addWidget(subtitle)

        actions = QHBoxLayout()
        btn_back = QPushButton("Volver")
        btn_back.clicked.connect(self._go_back)
        actions.addWidget(btn_back)
        actions.addStretch(1)
        actions.addWidget(make_theme_toggle_button(self))
        lay.addLayout(actions)

        btn_gauss = QPushButton("Gauss-Jordan")
        btn_gauss.setMinimumHeight(44)
        btn_gauss.clicked.connect(self._open_gauss)
        lay.addWidget(btn_gauss)

        btn_cramer = QPushButton("Método de Cramer")
        btn_cramer.setMinimumHeight(44)
        btn_cramer.clicked.connect(self._open_cramer)
        lay.addWidget(btn_cramer)

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

    def _open_gauss(self):
        from .sistemas.gauss_jordan_qt import GaussJordanWindow
        w = GaussJordanWindow(parent=self)
        w.showMaximized(); self._child = w

    def _open_cramer(self):
        from .sistemas.cramer_qt import CramerWindow
        w = CramerWindow(parent=self)
        w.showMaximized(); self._child = w
