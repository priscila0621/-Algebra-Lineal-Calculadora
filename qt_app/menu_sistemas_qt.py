from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QFrame,
)
from PySide6.QtCore import Qt
from .theme import make_theme_toggle_button, install_toggle_shortcut, make_font_scale_selector


class MenuSistemasWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Resolver sistemas de ecuaciones lineales")

        outer = QWidget()
        self.setCentralWidget(outer)
        outer_lay = QVBoxLayout(outer)
        outer_lay.setContentsMargins(24, 24, 24, 24)
        outer_lay.setSpacing(18)

        nav = QFrame()
        nav.setObjectName("TopNav")
        nav_lay = QHBoxLayout(nav)
        nav_lay.setContentsMargins(18, 12, 18, 12)
        nav_lay.setSpacing(12)

        btn_back = QPushButton("\u2190")
        btn_back.setObjectName("BackButton")
        btn_back.setFixedSize(42, 42)
        btn_back.setToolTip("Volver")
        btn_back.setCursor(Qt.PointingHandCursor)
        btn_back.clicked.connect(self._go_back)
        nav_lay.addWidget(btn_back)

        nav_lay.addSpacing(6)

        btn_gauss = QPushButton("Gauss-Jordan")
        btn_gauss.setMinimumHeight(36)
        btn_gauss.clicked.connect(self._open_gauss)
        nav_lay.addWidget(btn_gauss)

        btn_cramer = QPushButton("Método de Cramer")
        btn_cramer.setMinimumHeight(36)
        btn_cramer.clicked.connect(self._open_cramer)
        nav_lay.addWidget(btn_cramer)

        nav_lay.addStretch(1)
        font_selector = make_font_scale_selector(self)
        nav_lay.addWidget(font_selector, 0, Qt.AlignVCenter)
        nav_lay.addSpacing(8)
        nav_lay.addWidget(make_theme_toggle_button(self), 0, Qt.AlignVCenter)
        outer_lay.addWidget(nav)

        card = QFrame()
        card.setObjectName("Card")
        card_lay = QVBoxLayout(card)
        card_lay.setContentsMargins(32, 28, 32, 28)
        card_lay.setSpacing(16)

        title = QLabel("Resolver sistemas de ecuaciones lineales")
        title.setObjectName("Title")
        card_lay.addWidget(title)

        subtitle = QLabel(
            "Selecciona un método desde la barra superior para iniciar la resolución. "
            "Cada módulo muestra los pasos algorítmicos y permite exportar resultados limpios."
        )
        subtitle.setObjectName("Subtitle")
        subtitle.setWordWrap(True)
        card_lay.addWidget(subtitle)

        insights = QLabel(
            "• Gauss-Jordan: ideal para pivotear matrices aumentadas y diagnosticar la naturaleza del sistema.\n"
            "• Método de Cramer: ejecuta determinantes automáticamente cuando la matriz es invertible."
        )
        insights.setWordWrap(True)
        card_lay.addWidget(insights)

        card_lay.addStretch(1)
        outer_lay.addWidget(card, 1)

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
        w.showMaximized()
        self._child = w

    def _open_cramer(self):
        from .sistemas.cramer_qt import CramerWindow

        w = CramerWindow(parent=self)
        w.showMaximized()
        self._child = w


