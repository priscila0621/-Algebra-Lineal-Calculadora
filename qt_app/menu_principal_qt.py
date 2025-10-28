from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QFrame,
    QSizePolicy,
)
from PySide6.QtCore import Qt
from .menu_matrices_qt import MenuMatricesWindow
from .menu_sistemas_qt import MenuSistemasWindow
from .independencia_qt import IndependenciaWindow
from .transformaciones_qt import TransformacionesWindow
from .theme import make_theme_toggle_button, install_toggle_shortcut


class MenuPrincipalWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calculadora Álgebra Lineal")

        root = QWidget()
        self.setCentralWidget(root)
        base = QHBoxLayout(root)
        base.setContentsMargins(24, 24, 24, 24)
        base.setSpacing(24)

        # Navegación lateral
        nav = QFrame()
        nav.setObjectName("NavPanel")
        nav.setFixedWidth(260)
        nav_lay = QVBoxLayout(nav)
        nav_lay.setContentsMargins(24, 24, 24, 24)
        nav_lay.setSpacing(18)

        nav_title = QLabel("Menú principal")
        nav_title.setObjectName("Title")
        nav_title.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        nav_lay.addWidget(nav_title)

        nav_sub = QLabel("Explora cada módulo especializado.")
        nav_sub.setObjectName("Subtitle")
        nav_sub.setWordWrap(True)
        nav_lay.addWidget(nav_sub)

        self.btn_sistemas = QPushButton("Sistemas de ecuaciones")
        self.btn_sistemas.setMinimumHeight(44)
        self.btn_sistemas.clicked.connect(self._open_sistemas)
        nav_lay.addWidget(self.btn_sistemas)

        self.btn_matrices = QPushButton("Operaciones con matrices")
        self.btn_matrices.setMinimumHeight(44)
        self.btn_matrices.clicked.connect(self._open_matrices)
        nav_lay.addWidget(self.btn_matrices)

        self.btn_independencia = QPushButton("Independencia de vectores")
        self.btn_independencia.setMinimumHeight(44)
        self.btn_independencia.clicked.connect(self._open_independencia)
        nav_lay.addWidget(self.btn_independencia)

        self.btn_transformaciones = QPushButton("Transformaciones lineales")
        self.btn_transformaciones.setMinimumHeight(44)
        self.btn_transformaciones.clicked.connect(self._open_transformaciones)
        nav_lay.addWidget(self.btn_transformaciones)

        nav_lay.addStretch(1)

        about = QLabel(
            "© 2024 · Priscila Selva · Emma Serrano · Jeyni Orozco\n"
            "Todos los derechos reservados."
        )
        about.setWordWrap(True)
        about.setAlignment(Qt.AlignLeft | Qt.AlignBottom)
        about.setObjectName("Subtitle")
        nav_lay.addWidget(about)

        base.addWidget(nav)

        # Panel principal con información
        content = QFrame()
        content.setObjectName("Card")
        content_lay = QVBoxLayout(content)
        content_lay.setContentsMargins(32, 32, 32, 32)
        content_lay.setSpacing(20)

        top_bar = QHBoxLayout()
        top_bar.addStretch(1)
        toggle = make_theme_toggle_button(self)
        toggle.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        top_bar.addWidget(toggle)
        content_lay.addLayout(top_bar)

        hero = QHBoxLayout()
        hero.setSpacing(24)

        logo = QLabel("NL")
        logo.setAlignment(Qt.AlignCenter)
        logo.setFixedSize(96, 96)
        logo.setStyleSheet(
            """
            QLabel {
                background-color: #B07A8C;
                color: #FFFFFF;
                border-radius: 48px;
                font-size: 36px;
                font-weight: 700;
                letter-spacing: 4px;
            }
            """
        )
        hero.addWidget(logo, 0, Qt.AlignTop)

        title_box = QVBoxLayout()
        heading = QLabel("Nexus Linear · Calculadora Inteligente")
        heading.setObjectName("Title")
        title_box.addWidget(heading)

        strapline = QLabel(
            "Una suite profesional para explorar, resolver y visualizar problemas de álgebra lineal. "
            "Integramos herramientas interactivas para docentes, estudiantes y profesionales."
        )
        strapline.setObjectName("Subtitle")
        strapline.setWordWrap(True)
        title_box.addWidget(strapline)

        title_box.addSpacing(8)

        highlights = QLabel(
            "· Automatiza cálculos complejos con precisión fraccional.\n"
            "· Documenta cada procedimiento con trazabilidad paso a paso.\n"
            "· Diseñada para la Universidad de Tecnología: innovación aplicada."
        )
        highlights.setWordWrap(True)
        highlights.setAlignment(Qt.AlignLeft)
        title_box.addWidget(highlights)

        hero.addLayout(title_box, 1)
        content_lay.addLayout(hero)

        content_lay.addSpacing(12)

        info_title = QLabel("Acerca de la plataforma")
        info_title.setObjectName("Subtitle")
        content_lay.addWidget(info_title)

        info_body = QLabel(
            "Nexus Linear nace para centralizar las operaciones más demandadas en álgebra lineal. "
            "Desde la resolución de sistemas y la manipulación de matrices hasta el análisis de transformaciones, "
            "cada módulo ofrece una experiencia guiada con interfaces claras, resultados instantáneos y explicación pedagógica. "
            "El diseño Ivory Chic refuerza una estética sobria y moderna, ideal para entornos académicos y profesionales."
        )
        info_body.setWordWrap(True)
        content_lay.addWidget(info_body)

        content_lay.addStretch(1)
        base.addWidget(content, 1)

        install_toggle_shortcut(self)

    def _open_sistemas(self):
        self.s = MenuSistemasWindow(parent=self)
        self.s.showMaximized()

    def _open_matrices(self):
        self.m = MenuMatricesWindow(parent=self)
        self.m.showMaximized()

    def _open_independencia(self):
        self.w = IndependenciaWindow(parent=self)
        self.w.showMaximized()

    def _open_transformaciones(self):
        self.w = TransformacionesWindow(parent=self)
        self.w.showMaximized()
