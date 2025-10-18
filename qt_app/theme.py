from PySide6.QtWidgets import QApplication, QPushButton
from PySide6.QtGui import QPalette, QColor, QFont, QKeySequence
from PySide6.QtCore import Qt
from PySide6.QtGui import QShortcut


def apply_theme(app: QApplication, mode: str = "light") -> None:
    app.setStyle("Fusion")
    app.setProperty("theme_mode", mode)

    palette = QPalette()
    if mode == "dark":
        # Modo oscuro con acento rosa
        bg = QColor("#1f2937")
        base = QColor("#111827")
        text = QColor("#f9fafb")
        subtle = QColor("#374151")
        accent = QColor("#f472b6")

        palette.setColor(QPalette.Window, bg)
        palette.setColor(QPalette.WindowText, text)
        palette.setColor(QPalette.Base, base)
        palette.setColor(QPalette.AlternateBase, QColor("#0f172a"))
        palette.setColor(QPalette.ToolTipBase, base)
        palette.setColor(QPalette.ToolTipText, text)
        palette.setColor(QPalette.Text, text)
        palette.setColor(QPalette.Button, base)
        palette.setColor(QPalette.ButtonText, text)
        palette.setColor(QPalette.Highlight, accent)
        palette.setColor(QPalette.HighlightedText, QColor("#ffffff"))
        palette.setColor(QPalette.PlaceholderText, QColor("#9ca3af"))

        app.setPalette(palette)
        app.setFont(QFont("Segoe UI", 11))
        app.setStyleSheet(
            """
            QWidget { background: #1f2937; color: #f9fafb; }
            QMainWindow { background: #1f2937; }
            QFrame#Card { background: #111827; border: 1px solid #374151; border-radius: 12px; }
            QLabel#Title { font-size: 28px; font-weight: 700; color: #f9fafb; }
            QLabel#Subtitle { font-size: 14px; color: #e5e7eb; }
            QPushButton { background: #f472b6; color: #ffffff; border: none; border-radius: 8px; padding: 10px 16px; font-size: 14px; font-weight: 600; }
            QPushButton:hover { background: #ec4899; }
            QPushButton:pressed { background: #db2777; }
            QPushButton:disabled { background: #374151; color: #9ca3af; }
            QLineEdit, QSpinBox { border: 1px solid #374151; border-radius: 8px; padding: 6px 8px; background: #0b1220; color: #f9fafb; }
            QLineEdit:focus, QSpinBox:focus { border: 1px solid #f472b6; }
            QScrollArea { border: none; }
            QTextEdit { border: 1px solid #374151; border-radius: 8px; background: #0b1220; color: #f9fafb; }
            QGroupBox { border: 1px solid #374151; border-radius: 8px; margin-top: 12px; }
            QGroupBox::title { subcontrol-origin: margin; left: 12px; padding: 0 4px; }
            """
        )
    else:
        # Claro rosa pastel (como Tk)
        bg = QColor("#ffe4e6")
        base = QColor("#ffffff")
        text = QColor("#111111")
        accent = QColor("#f472b6")

        palette.setColor(QPalette.Window, bg)
        palette.setColor(QPalette.WindowText, text)
        palette.setColor(QPalette.Base, base)
        palette.setColor(QPalette.AlternateBase, QColor("#fff0f5"))
        palette.setColor(QPalette.ToolTipBase, base)
        palette.setColor(QPalette.ToolTipText, text)
        palette.setColor(QPalette.Text, text)
        palette.setColor(QPalette.Button, base)
        palette.setColor(QPalette.ButtonText, text)
        palette.setColor(QPalette.Highlight, accent)
        palette.setColor(QPalette.HighlightedText, QColor("#ffffff"))
        palette.setColor(QPalette.PlaceholderText, QColor("#6b7280"))
        app.setPalette(palette)
        app.setFont(QFont("Segoe UI", 11))
        app.setStyleSheet(
            """
            QWidget { background: #ffe4e6; color: #111111; }
            QMainWindow { background: #ffe4e6; }
            QFrame#Card { background: #ffffff; border: 1px solid #f8cbd9; border-radius: 12px; }
            QLabel#Title { font-size: 28px; font-weight: 700; color: #b91c1c; }
            QLabel#Subtitle { font-size: 14px; color: #b91c1c; }
            QPushButton { background: #fbb6ce; color: #ffffff; border: none; border-radius: 8px; padding: 10px 16px; font-size: 14px; font-weight: 600; }
            QPushButton:hover { background: #f472b6; }
            QPushButton:pressed { background: #ec4899; }
            QPushButton:disabled { background: #e5e7eb; color: #6b7280; }
            QLineEdit, QSpinBox { border: 1px solid #f8cbd9; border-radius: 8px; padding: 6px 8px; background: #ffffff; }
            QLineEdit:focus, QSpinBox:focus { border: 1px solid #f472b6; }
            QScrollArea { border: none; }
            QTextEdit { border: 1px solid #f8cbd9; border-radius: 8px; background: #ffffff; }
            QGroupBox { border: 1px solid #f8cbd9; border-radius: 8px; margin-top: 12px; }
            QGroupBox::title { subcontrol-origin: margin; left: 12px; padding: 0 4px; }
            """
        )


def current_mode(app: QApplication) -> str:
    return app.property("theme_mode") or "light"


def toggle_theme(app: QApplication) -> None:
    mode = current_mode(app)
    apply_theme(app, "dark" if mode == "light" else "light")


def make_theme_toggle_button(parent_widget) -> QPushButton:
    """Crea un botón que alterna claro/oscuro y actualiza su etiqueta."""
    from PySide6.QtWidgets import QApplication
    app = QApplication.instance()
    btn = QPushButton()

    def _update_text():
        btn.setText("Modo oscuro" if current_mode(app) == "light" else "Modo claro")

    def _toggle():
        toggle_theme(app)
        _update_text()

    _update_text()
    btn.clicked.connect(_toggle)
    return btn


def install_toggle_shortcut(window) -> None:
    """Instala Ctrl+D para alternar tema en la ventana dada."""
    from PySide6.QtWidgets import QApplication
    app = QApplication.instance()
    sc = QShortcut(QKeySequence("Ctrl+D"), window)
    sc.activated.connect(lambda: toggle_theme(app))
