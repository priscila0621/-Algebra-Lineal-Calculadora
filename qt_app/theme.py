from PySide6.QtWidgets import QApplication, QPushButton
from PySide6.QtGui import QPalette, QColor, QFont, QKeySequence
from PySide6.QtCore import Qt
from PySide6.QtGui import QShortcut


def apply_theme(app: QApplication, mode: str = "light") -> None:
    app.setStyle("Fusion")
    app.setProperty("theme_mode", mode)

    palette = QPalette()
    if mode == "dark":
        # Modo oscuro complementario (dusty rose como acento)
        bg = QColor("#1F1D22")
        base = QColor("#15131A")
        text = QColor("#F7F4F1")
        subtle = QColor("#3A3542")
        accent = QColor("#B07A8C")

        palette.setColor(QPalette.Window, bg)
        palette.setColor(QPalette.WindowText, text)
        palette.setColor(QPalette.Base, base)
        palette.setColor(QPalette.AlternateBase, QColor("#201E25"))
        palette.setColor(QPalette.ToolTipBase, QColor("#26232B"))
        palette.setColor(QPalette.ToolTipText, text)
        palette.setColor(QPalette.Text, text)
        palette.setColor(QPalette.Button, accent)
        palette.setColor(QPalette.ButtonText, QColor("#FFFFFF"))
        palette.setColor(QPalette.Highlight, accent)
        palette.setColor(QPalette.HighlightedText, QColor("#FFFFFF"))
        palette.setColor(QPalette.PlaceholderText, QColor("#8F8697"))

        app.setPalette(palette)
        app.setFont(QFont("Segoe UI", 11))
        app.setStyleSheet(
            """
            QWidget { background: #1F1D22; color: #F7F4F1; }
            QMainWindow { background: #1F1D22; }
            QFrame#Card { background: #15131A; border: 1px solid #3A3542; border-radius: 16px; }
            QLabel#Title { font-size: 28px; font-weight: 700; color: #F7F4F1; }
            QLabel#Subtitle { font-size: 14px; color: #B9AFC0; }
            QPushButton {
                background: #B07A8C;
                color: #ffffff;
                border: none;
                border-radius: 10px;
                padding: 10px 20px;
                min-height: 40px;
                font-size: 14px;
                font-weight: 600;
            }
            QPushButton:hover { background: #9A5D73; }
            QPushButton:pressed { background: #834C63; }
            QPushButton:disabled { background: #3A3542; color: #8F8697; }
            QLineEdit, QSpinBox, QTextEdit, QPlainTextEdit, QComboBox {
                border: 1px solid #3A3542;
                border-radius: 8px;
                padding: 6px 10px;
                background: #1F1D22;
                color: #F7F4F1;
            }
            QLineEdit:focus, QSpinBox:focus, QTextEdit:focus, QPlainTextEdit:focus, QComboBox:focus {
                border: 1px solid #B07A8C;
            }
            QComboBox QListView {
                background: #15131A;
                border: 1px solid #3A3542;
                selection-background-color: #B07A8C;
                selection-color: #ffffff;
            }
            QScrollArea { border: none; }
            QTextEdit { border: 1px solid #3A3542; border-radius: 8px; background: #1F1D22; color: #F7F4F1; }
            QGroupBox { border: 1px solid #3A3542; border-radius: 10px; margin-top: 12px; }
            QGroupBox::title { subcontrol-origin: margin; left: 12px; padding: 0 4px; color: #B9AFC0; }
            QTabWidget::pane { border: 1px solid #3A3542; border-radius: 10px; background: #1F1D22; }
            QFrame#NavPanel {
                background: #201E25;
                border: 1px solid #3A3542;
                border-radius: 18px;
            }
            QFrame#Card QLabel {
                background: transparent;
            }
            QFrame#NavPanel QLabel {
                background: transparent;
            }
            QFrame#TopNav {
                background: #15131A;
                border: 1px solid #3A3542;
                border-radius: 12px;
            }
            QFrame#TopNav QPushButton {
                min-width: 120px;
            }
            QTabBar::tab {
                background: #1F1D22;
                color: #F7F4F1;
                padding: 8px 16px;
                border: 1px solid #3A3542;
                border-bottom: none;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                margin-right: 4px;
            }
            QTabBar::tab:selected { background: #B07A8C; color: #ffffff; }
            QTabBar::tab:hover { background: #9A5D73; }
            """
        )
    else:
        # Claro Ivory Chic
        bg = QColor("#FAF7F5")
        base = QColor("#FFFFFF")
        text = QColor("#4F3A47")
        accent = QColor("#B07A8C")

        palette.setColor(QPalette.Window, bg)
        palette.setColor(QPalette.WindowText, text)
        palette.setColor(QPalette.Base, base)
        palette.setColor(QPalette.AlternateBase, QColor("#F1E6E4"))
        palette.setColor(QPalette.ToolTipBase, QColor("#F1E6E4"))
        palette.setColor(QPalette.ToolTipText, QColor("#4F3A47"))
        palette.setColor(QPalette.Text, text)
        palette.setColor(QPalette.Button, accent)
        palette.setColor(QPalette.ButtonText, QColor("#FFFFFF"))
        palette.setColor(QPalette.Highlight, accent)
        palette.setColor(QPalette.HighlightedText, QColor("#FFFFFF"))
        palette.setColor(QPalette.PlaceholderText, QColor("#B09CA7"))
        app.setPalette(palette)
        app.setFont(QFont("Segoe UI", 11))
        app.setStyleSheet(
            """
            QWidget { background: #FAF7F5; color: #4F3A47; }
            QMainWindow { background: #FAF7F5; }
            QFrame#Card { background: #F1E6E4; border: 1px solid #D9C8C5; border-radius: 16px; }
            QLabel#Title { font-size: 28px; font-weight: 700; color: #6E4B5E; }
            QLabel#Subtitle { font-size: 14px; color: #A78A94; }
            QPushButton {
                background: #B07A8C;
                color: #ffffff;
                border: none;
                border-radius: 10px;
                padding: 10px 20px;
                min-height: 40px;
                font-size: 14px;
                font-weight: 600;
            }
            QPushButton:hover { background: #9A5D73; }
            QPushButton:pressed { background: #834C63; }
            QPushButton:disabled { background: #E5D9D7; color: #BBA9AE; }
            QLineEdit, QSpinBox, QTextEdit, QPlainTextEdit, QComboBox {
                border: 1px solid #D9C8C5;
                border-radius: 8px;
                padding: 6px 10px;
                background: #FFFFFF;
                color: #4F3A47;
            }
            QLineEdit:focus, QSpinBox:focus, QTextEdit:focus, QPlainTextEdit:focus, QComboBox:focus {
                border: 1px solid #B07A8C;
            }
            QComboBox QListView {
                background: #FFFFFF;
                border: 1px solid #D9C8C5;
                selection-background-color: #B07A8C;
                selection-color: #ffffff;
            }
            QScrollArea { border: none; }
            QTextEdit { border: 1px solid #D9C8C5; border-radius: 8px; background: #FFFFFF; }
            QGroupBox { border: 1px solid #D9C8C5; border-radius: 10px; margin-top: 12px; }
            QGroupBox::title { subcontrol-origin: margin; left: 12px; padding: 0 4px; color: #A78A94; }
            QTabWidget::pane { border: 1px solid #D9C8C5; border-radius: 12px; background: #FFFFFF; }
            QTabBar::tab {
                min-width: 120px;
                background: #F1E6E4;
                color: #6E4B5E;
                padding: 8px 16px;
                border: 1px solid #D9C8C5;
                border-bottom: none;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                margin-right: 4px;
            }
            QTabBar::tab:selected { background: #B07A8C; color: #ffffff; }
            QTabBar::tab:hover { background: #9A5D73; color: #ffffff; }
            QFrame#NavPanel {
                background: #F1E6E4;
                border: 1px solid #D9C8C5;
                border-radius: 18px;
            }
            QFrame#Card QLabel {
                background: transparent;
            }
            QFrame#NavPanel QLabel {
                background: transparent;
            }
            QFrame#TopNav {
                background: #F1E6E4;
                border: 1px solid #D9C8C5;
                border-radius: 12px;
            }
            QFrame#TopNav QPushButton {
                min-width: 120px;
            }
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
