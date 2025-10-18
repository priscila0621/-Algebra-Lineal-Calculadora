from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from .menu_principal_qt import MenuPrincipalWindow
from .theme import apply_theme
import sys


def run():
    app = QApplication.instance() or QApplication(sys.argv)
    apply_theme(app, mode="light")
    w = MenuPrincipalWindow()
    # A pantalla completa SIEMPRE (maximizado conserva marcos de ventana)
    w.showMaximized()
    sys.exit(app.exec())
