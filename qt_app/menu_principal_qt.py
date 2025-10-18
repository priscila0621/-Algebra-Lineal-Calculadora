from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFrame
)
from PySide6.QtCore import Qt
from .menu_matrices_qt import MenuMatricesWindow
from .sistemas.gauss_jordan_qt import GaussJordanWindow
from .independencia_qt import IndependenciaWindow
from .theme import make_theme_toggle_button, install_toggle_shortcut


class MenuPrincipalWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calculadora \u00C1lgebra Lineal")

        outer = QWidget()
        self.setCentralWidget(outer)
        outer_lay = QVBoxLayout(outer)
        outer_lay.setContentsMargins(24, 24, 24, 24)
        outer_lay.setSpacing(18)

        # Contenedor centrado de ancho controlado + barra de acciones (tema)
        center_row = QHBoxLayout()
        outer_lay.addLayout(center_row)
        center_row.addStretch(1)

        container = QFrame()
        container.setObjectName("Card")
        container.setMaximumWidth(1000)
        center_row.addWidget(container, 1)
        center_row.addStretch(1)

        lay = QVBoxLayout(container)
        lay.setContentsMargins(28, 28, 28, 28)
        lay.setSpacing(16)

        title = QLabel("Calculadora \u00C1lgebra Lineal")
        title.setObjectName("Title")
        title.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        lay.addWidget(title)

        subtitle = QLabel("Herramientas de \u00E1lgebra lineal: sistemas, matrices y m\u00E1s.")
        subtitle.setObjectName("Subtitle")
        lay.addWidget(subtitle)

        # Toggle de tema a la derecha
        actions = QHBoxLayout()
        actions.addStretch(1)
        actions.addWidget(make_theme_toggle_button(self))
        lay.addLayout(actions)

        # Grupo de acciones
        btn1 = QPushButton("Resolver sistema de ecuaciones lineales")
        btn1.setMinimumHeight(44)
        btn1.clicked.connect(self._open_sistemas)
        lay.addWidget(btn1)

        btn2 = QPushButton("Operaciones con matrices")
        btn2.setMinimumHeight(44)
        btn2.clicked.connect(self._open_matrices)
        lay.addWidget(btn2)

        btn3 = QPushButton("Independencia lineal de vectores")
        btn3.setMinimumHeight(44)
        btn3.clicked.connect(self._open_independencia)
        lay.addWidget(btn3)

        lay.addStretch(1)

        # Atajo Ctrl+D
        install_toggle_shortcut(self)

    def _open_sistemas(self):
        self.w = GaussJordanWindow(parent=self)
        self.w.showMaximized()

    def _open_matrices(self):
        self.m = MenuMatricesWindow(parent=self)
        self.m.showMaximized()

    def _open_independencia(self):
        self.w = IndependenciaWindow(parent=self)
        self.w.showMaximized()




