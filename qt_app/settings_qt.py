from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QComboBox,
    QDialogButtonBox,
    QFormLayout,
)
from PySide6.QtCore import Qt

from .theme import (
    current_font_scale,
    set_font_scale,
    current_font_family,
    set_font_family,
    current_mode,
    apply_theme,
)


_FONT_SIZE_OPTIONS = [
    ("Letra compacta", 0.9),
    ("Letra estandar", 1.0),
    ("Letra grande", 1.2),
    ("Letra extra grande", 1.35),
    ("Letra maxima", 1.5),
]

_FONT_FAMILY_OPTIONS = [
    "Segoe UI",
    "Calibri",
    "Arial",
    "Verdana",
    "Tahoma",
    "Times New Roman",
    "Consolas",
]


class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Configuracion de interfaz")
        self.setModal(True)

        layout = QVBoxLayout(self)
        header = QLabel("Personaliza la apariencia de la calculadora")
        header.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        header.setStyleSheet("font-weight:700; font-size:16px;")
        layout.addWidget(header)

        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignLeft)
        layout.addLayout(form)

        # Tema claro/oscuro
        self.theme_combo = QComboBox()
        self.theme_combo.addItem("Tema claro", "light")
        self.theme_combo.addItem("Tema oscuro", "dark")
        current_theme = current_mode(self._app())
        idx_theme = max(0, self.theme_combo.findData(current_theme))
        self.theme_combo.setCurrentIndex(idx_theme)
        form.addRow("Tema:", self.theme_combo)

        # Tamano de fuente
        self.font_scale_combo = QComboBox()
        for label, value in _FONT_SIZE_OPTIONS:
            self.font_scale_combo.addItem(label, value)
        current_scale = current_font_scale(self._app())
        idx_scale = min(
            range(self.font_scale_combo.count()),
            key=lambda i: abs(self.font_scale_combo.itemData(i) - current_scale),
        )
        self.font_scale_combo.setCurrentIndex(idx_scale)
        form.addRow("Tamano de letra:", self.font_scale_combo)

        # Familia tipografica
        self.font_family_combo = QComboBox()
        self.font_family_combo.setEditable(True)
        for family in _FONT_FAMILY_OPTIONS:
            if self.font_family_combo.findText(family, Qt.MatchFixedString) == -1:
                self.font_family_combo.addItem(family)
        current_family = current_font_family(self._app())
        if self.font_family_combo.findText(current_family, Qt.MatchFixedString) == -1:
            self.font_family_combo.addItem(current_family)
        self.font_family_combo.setCurrentText(current_family)
        form.addRow("Tipo de letra:", self.font_family_combo)

        info = QLabel(
            "Los cambios se aplican inmediatamente y se recuerdan para futuras sesiones."
        )
        info.setWordWrap(True)
        info.setAlignment(Qt.AlignLeft)
        info.setStyleSheet("color: #6b7280;")
        layout.addWidget(info)

        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel | QDialogButtonBox.Apply
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        apply_btn = buttons.button(QDialogButtonBox.Apply)
        if apply_btn:
            apply_btn.clicked.connect(self.apply_changes)
        layout.addWidget(buttons)

    def _app(self):
        from PySide6.QtWidgets import QApplication

        return QApplication.instance()

    def apply_changes(self):
        app = self._app()
        changed = False

        # Fuente (familia)
        chosen_family = self.font_family_combo.currentText().strip()
        if chosen_family and chosen_family != current_font_family(app):
            set_font_family(app, chosen_family)
            changed = True

        # Escala de fuente
        chosen_scale = float(self.font_scale_combo.currentData())
        if abs(chosen_scale - current_font_scale(app)) > 1e-6:
            set_font_scale(app, chosen_scale)
            changed = True

        # Tema
        chosen_theme = self.theme_combo.currentData()
        if chosen_theme != current_mode(app):
            apply_theme(app, chosen_theme)
            changed = True

        if changed:
            # actualizar familia mostrada despues de aplicar (por si se normalizo)
            self.font_family_combo.setCurrentText(current_font_family(app))

    def accept(self):
        self.apply_changes()
        super().accept()


def open_settings_dialog(parent=None):
    dlg = SettingsDialog(parent)
    dlg.exec()
