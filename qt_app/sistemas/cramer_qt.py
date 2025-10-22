from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame,
    QScrollArea, QGridLayout, QLineEdit, QTextEdit, QMessageBox
)
from PySide6.QtCore import Qt
from ..theme import make_theme_toggle_button, install_toggle_shortcut
from fractions import Fraction
from qt_app.matrices_qt import determinante_con_pasos as determinante_con_pasos_ascii


def _fmt_fraction(x: Fraction) -> str:
    try:
        if isinstance(x, Fraction):
            if x.denominator == 1:
                return str(x.numerator)
            return f"{x.numerator}/{x.denominator}"
        return str(x)
    except Exception:
        return str(x)



class DetallesDeterminantesWindow(QMainWindow):
    """Ventana que muestra los procedimientos de determinantes uno por uno con navegación."""
    def __init__(self, parent=None, items=None):
        super().__init__(parent)
        self.setWindowTitle("Cálculos de determinantes")
        self.items = items or []  # lista de (titulo, lineas[])
        self.index = 0

        outer = QWidget()
        self.setCentralWidget(outer)
        lay = QVBoxLayout(outer)
        lay.setContentsMargins(12, 12, 12, 12)
        lay.setSpacing(8)

        self.header = QLabel("")
        self.header.setAlignment(Qt.AlignCenter)
        self.header.setStyleSheet("font-weight:700; font-size:14px;")
        lay.addWidget(self.header)

        self.text = QTextEdit()
        self.text.setReadOnly(True)
        self.text.setStyleSheet("font-family:Consolas,monospace;font-size:12px;")
        lay.addWidget(self.text, 1)

        btns = QHBoxLayout()
        self.prev_btn = QPushButton("Anterior")
        self.next_btn = QPushButton("Siguiente")
        self.close_btn = QPushButton("Cerrar")
        btns.addWidget(self.prev_btn)
        btns.addWidget(self.next_btn)
        btns.addStretch(1)
        btns.addWidget(self.close_btn)
        lay.addLayout(btns)

        self.prev_btn.clicked.connect(self._prev)
        self.next_btn.clicked.connect(self._next)
        self.close_btn.clicked.connect(self.close)

        self._update_view()

    def _update_view(self):
        if not self.items:
            self.header.setText("No hay cálculos disponibles")
            self.text.setPlainText("")
            self.prev_btn.setEnabled(False)
            self.next_btn.setEnabled(False)
            return
        title, lines = self.items[self.index]
        self.header.setText(title)
        self.text.setPlainText("\n".join(lines))
        self.prev_btn.setEnabled(self.index > 0)
        self.next_btn.setEnabled(self.index < len(self.items) - 1)

    def _next(self):
        if self.index < len(self.items) - 1:
            self.index += 1
            self._update_view()

    def _prev(self):
        if self.index > 0:
            self.index -= 1
            self._update_view()



class CramerWindow(QMainWindow):
    """Interfaz para resolver sistemas por el método de Cramer.

    La cuadrícula de entrada es igual a la de Gauss-Jordan: una matriz aumentada
    con n filas y n+1 columnas. El método exige que n == columnas-1.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Método de Cramer")
        self._entries = []
        self._rows = 3
        self._cols_no_b = 3

        central = QWidget()
        self.setCentralWidget(central)
        outer = QVBoxLayout(central)
        outer.setContentsMargins(24, 24, 24, 24)
        outer.setSpacing(18)

        card = QFrame()
        card.setObjectName("Card")
        outer.addWidget(card)
        main = QVBoxLayout(card)
        main.setContentsMargins(24, 24, 24, 24)
        main.setSpacing(16)

        top = QHBoxLayout()
        main.addLayout(top)
        self.btn_back = QPushButton("Volver")
        self.btn_back.clicked.connect(self._go_back)
        top.addWidget(self.btn_back)
        self.btn_add_row = QPushButton("+ Fila")
        self.btn_add_row.clicked.connect(lambda: self._change_rows(1))
        top.addWidget(self.btn_add_row)
        self.btn_del_row = QPushButton("- Fila")
        self.btn_del_row.clicked.connect(lambda: self._change_rows(-1))
        top.addWidget(self.btn_del_row)
        self.btn_add_col = QPushButton("+ Columna")
        self.btn_add_col.clicked.connect(lambda: self._change_cols(1))
        top.addWidget(self.btn_add_col)
        self.btn_del_col = QPushButton("- Columna")
        self.btn_del_col.clicked.connect(lambda: self._change_cols(-1))
        top.addWidget(self.btn_del_col)
        self.btn_limpiar = QPushButton("Limpiar pantalla")
        self.btn_limpiar.clicked.connect(self._limpiar)
        top.addWidget(self.btn_limpiar)
        top.addStretch(1)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        main.addWidget(self.scroll)

        self.grid_container = QWidget()
        self.grid_layout = QGridLayout(self.grid_container)
        self.grid_layout.setHorizontalSpacing(10)
        self.grid_layout.setVerticalSpacing(8)
        self.scroll.setWidget(self.grid_container)

        title = QLabel("Resultados")
        title.setObjectName("Subtitle")
        main.addWidget(title)

        # Área de resultados: cuadro destacado con det(A) y valores de las variables
        self.result_highlight = QFrame()
        self.result_highlight.setObjectName("Card")
        rh_lay = QVBoxLayout(self.result_highlight)
        rh_lay.setContentsMargins(12, 12, 12, 12)
        rh_lay.setSpacing(8)
        self.det_label = QLabel("det(A) = —")
        self.det_label.setStyleSheet("font-size:18px;font-weight:700;color:#b91c1c;")
        rh_lay.addWidget(self.det_label)
        self.vars_box = QTextEdit()
        self.vars_box.setReadOnly(True)
        self.vars_box.setStyleSheet("font-size:16px;font-weight:700;background:transparent;border:none;font-family:Segoe UI;")
        rh_lay.addWidget(self.vars_box)
        main.addWidget(self.result_highlight)

        # Botón resolver
        self.btn_resolver = QPushButton("Resolver por Cramer")
        self.btn_resolver.clicked.connect(self._resolver)
        self.btn_resolver.setEnabled(False)
        main.addWidget(self.btn_resolver)

        # Panel de procedimiento (alto nivel) y panel ocultable para cálculos de determinantes
        self.procedimiento = QTextEdit()
        self.procedimiento.setReadOnly(True)
        self.procedimiento.setStyleSheet("font-family:Segoe UI; font-size:12px;")
        main.addWidget(self.procedimiento, 1)

        self.toggle_det_btn = QPushButton("Mostrar cálculos de determinantes")
        self.toggle_det_btn.setCheckable(True)
        self.toggle_det_btn.clicked.connect(self._open_detalles_window)
        main.addWidget(self.toggle_det_btn)

        self.detalles_container = QFrame()
        self.detalles_container.setVisible(False)
        det_l = QVBoxLayout(self.detalles_container)
        det_l.setContentsMargins(6, 6, 6, 6)
        self.detalles_text = QTextEdit()
        self.detalles_text.setReadOnly(True)
        self.detalles_text.setStyleSheet("font-family:Consolas,monospace;font-size:12px;")
        det_l.addWidget(self.detalles_text)
        main.addWidget(self.detalles_container, 1)

        self._rebuild_grid(self._rows, self._cols_no_b + 1)
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

    def _limpiar(self):
        self._entries = []
        while self.grid_layout.count():
            w = self.grid_layout.takeAt(0).widget()
            if w:
                w.deleteLater()
        self.procedimiento.clear()
        self.detalles_text.clear()
        self.det_label.setText("det(A) = —")
        self.vars_box.clear()
        self.btn_resolver.setEnabled(False)

    def _rebuild_grid(self, filas: int, columnas: int):
        old = [[e.text() for e in row] for row in self._entries] if self._entries else []
        self._limpiar()
        # encabezados para variables x1..xn y columna b
        for j in range(columnas - 1):
            h = QLabel(f"x{j+1}")
            h.setStyleSheet("font-weight:700;")
            self.grid_layout.addWidget(h, 0, j)
        hb = QLabel("b")
        hb.setStyleSheet("font-weight:700;")
        self.grid_layout.addWidget(hb, 0, columnas - 1)
        self._entries = []
        for i in range(filas):
            row = []
            for j in range(columnas):
                e = QLineEdit()
                e.setPlaceholderText("0")
                e.setAlignment(Qt.AlignCenter)
                if old and i < len(old) and j < len(old[i]):
                    e.setText(old[i][j])
                self.grid_layout.addWidget(e, i + 1, j)
                row.append(e)
            self._entries.append(row)
        self.btn_resolver.setEnabled(True)

    def _change_rows(self, delta: int):
        self._rows = max(1, self._rows + delta)
        self._rebuild_grid(self._rows, self._cols_no_b + 1)

    def _change_cols(self, delta: int):
        self._cols_no_b = max(1, self._cols_no_b + delta)
        self._rebuild_grid(self._rows, self._cols_no_b + 1)

    def _leer_matriz(self):
        if not self._entries:
            raise ValueError("Primero cree la matriz.")
        A = []
        for row in self._entries:
            vals = []
            for e in row:
                s = (e.text() or "0").strip()
                vals.append(Fraction(s.replace(",", ".")))
            A.append(vals)
        return A

    def _toggle_detalles(self):
        # kept for backward compatibility but not used; prefer popup
        visible = self.detalles_container.isVisible()
        self.detalles_container.setVisible(not visible)
        self.toggle_det_btn.setText("Ocultar cálculos de determinantes" if not visible else "Mostrar cálculos de determinantes")

    def _open_detalles_window(self):
        # open a dedicated window with paginated determinante steps
        items = getattr(self, "_det_steps_items", None)
        if not items:
            QMessageBox.information(self, "Sin cálculos", "Primero resuelve el sistema para generar los cálculos de determinantes.")
            return
        w = DetallesDeterminantesWindow(parent=self, items=items)
        w.resize(820, 620)
        w.show()
        self._detalles_window = w

    def _resolver(self):
        try:
            A_aug = self._leer_matriz()
        except Exception as exc:
            QMessageBox.critical(self, "Error", f"Entrada inválida: {exc}")
            return
        n = len(A_aug)
        if n == 0:
            QMessageBox.warning(self, "Error", "Matriz vacía.")
            return
        m = len(A_aug[0])
        if m != n + 1:
            QMessageBox.warning(self, "Dimensiones incompatibles", "Para Cramer se requiere una matriz aumentada n x (n+1). Ajusta filas/columnas.")
            return

        # separar A y b
        A = [[A_aug[i][j] for j in range(m - 1)] for i in range(n)]
        b = [A_aug[i][-1] for i in range(n)]

        # calculo de det(A)
        detA, pasosA = determinante_con_pasos_ascii(A)
        # mostrar detA distintivo
        self.det_label.setText(f"det(A) = {_fmt_fraction(detA)}")

        if detA == 0:
            # mostrar mensaje y detallar pasos en la sección de determinantes
            QMessageBox.critical(self, "No se puede aplicar Cramer", "El determinante de la matriz de coeficientes es cero. No se puede resolver por el método de Cramer.")
        # calcular determinantes para cada variable
        det_vars = []
        det_steps = {"detA": pasosA}
        for col in range(n):
            # construir matriz con columna col reemplazada por b
            M = [row[:] for row in A]
            for i in range(n):
                M[i][col] = b[i]
            detk, pasosk = determinante_con_pasos_ascii(M)
            det_vars.append(detk)
            det_steps[f"det_var_{col+1}"] = pasosk

        # preparar items paginados para la ventana de detalles: lista de (titulo, lineas)
        self._det_steps_items = []
        # primer item: det(A)
        self._det_steps_items.append(("|A| — determinante general", pasosA))
        for idx in range(n):
            key = f"det_var_{idx+1}"
            lines = det_steps.get(key, [])
            self._det_steps_items.append((f"|A{idx+1}| — determinante sustituyendo columna {idx+1}", lines))

        # preparar y mostrar resultados
        self.vars_box.clear()
        if detA != 0:
            lines = []
            for i, detk in enumerate(det_vars):
                val = detk / detA
                lines.append(f"x{i+1} = {_fmt_fraction(detk)} / {_fmt_fraction(detA)} = {_fmt_fraction(val)}")
            self.vars_box.setPlainText("\n".join(lines))
        else:
            # si detA == 0 ofrecer interpretación: mostrar det vars si se desea
            self.vars_box.setPlainText("Determinante cero: no aplicable. Se muestran los determinantes sustituidos si los desea ver.")

        # procedimiento principal (alto nivel) — ahora formateado en HTML + <pre>
        # Queremos: 1) Regla de Cramer (fórmula). 2) Con valores: mostrar |A|, |A1|, |A2|... con matrices dentro de barras
        def _matrix_block_html(M):
            # devuelve HTML con <pre> que representa la matriz entre barras
            # calcular ancho por columna
            if not M:
                return "<pre> | | </pre>"
            rows = [[_fmt_fraction(x) for x in r] for r in M]
            cols = len(rows[0])
            widths = [0] * cols
            for r in rows:
                for j, cell in enumerate(r):
                    widths[j] = max(widths[j], len(cell))
            lines = []
            for r in rows:
                cells = [str(r[j]).rjust(widths[j]) for j in range(cols)]
                lines.append("  | " + "  ".join(cells) + " |")
            return "<pre style='font-family:Consolas,monospace;font-size:13px; margin:6px;'>" + "\n".join(lines) + "</pre>"

        def _matrix_block_html_aug(M, bvec):
            # Representación de matriz aumentada A | b con separador vertical antes de la última columna
            if not M:
                return "<pre> | | </pre>"
            rows = []
            # A columns
            a_rows = [[_fmt_fraction(x) for x in r] for r in M]
            b_cells = [_fmt_fraction(x) for x in bvec]
            colsA = len(a_rows[0])
            widths = [0] * colsA
            width_b = 0
            for r in a_rows:
                for j, cell in enumerate(r):
                    widths[j] = max(widths[j], len(cell))
            for cell in b_cells:
                width_b = max(width_b, len(cell))

            lines = []
            for i, r in enumerate(a_rows):
                cells = [r[j].rjust(widths[j]) for j in range(colsA)]
                bcell = b_cells[i].rjust(width_b)
                # use a visible separator ' | ' between A and b
                lines.append("  | " + "  ".join(cells) + "  | " + bcell + " |")
            return "<pre style='font-family:Consolas,monospace;font-size:13px; margin:6px;'>" + "\n".join(lines) + "</pre>"

        # Cabecera con la fórmula
        html_parts = []
        html_parts.append("<div style='text-align:center; font-family:Segoe UI, sans-serif;'>")
        html_parts.append("<h3 style='margin:6px 0;'>Regla de Cramer (fórmula):</h3>")
        html_parts.append("<div style='font-size:14px; margin-bottom:10px;'>Para i = 1, ..., n: <b>x<sub>i</sub> = |A<sub>i</sub>| / |A|</b></div>")

        # Mostrar primero la matriz aumentada centrada (A | b)
        html_parts.append("<div style='width:100%; text-align:center; margin-bottom:6px;'>")
        html_parts.append("<div style='display:inline-block; text-align:center;'>")
        html_parts.append("<div style='text-align:center; font-weight:700; margin-bottom:6px;'>Matriz aumentada (A | b)</div>")
        html_parts.append(_matrix_block_html_aug(A, b))
        html_parts.append("</div>")
        html_parts.append("</div>")

        # luego mostrar la matriz A sola (centrada)
        html_parts.append("<div style='width:100%; text-align:center; margin-bottom:6px;'>")
        html_parts.append("<div style='display:inline-block; text-align:center;'>")
        html_parts.append("<div style='text-align:center; font-weight:700; margin-bottom:6px;'>Matriz A (coeficientes)</div>")
        html_parts.append(_matrix_block_html(A))
        html_parts.append("</div>")
        html_parts.append("</div>")

        # Mostrar los determinantes con matrices (sin expandir)
        html_parts.append("<div style='clear:both; margin-top:12px; text-align:center;'>")
        html_parts.append("<div style='font-weight:700; margin-bottom:6px;'>Con valores:</div>")
        # det(A)
        html_parts.append("<div style='display:inline-block; margin:6px 18px; text-align:center;'>")
        html_parts.append("<div style='font-weight:600'>&#124;A&#124; =</div>")
        html_parts.append(_matrix_block_html(A))
        html_parts.append(f"<div style='margin-top:6px; font-weight:700;'>= {_fmt_fraction(detA)}</div>")
        html_parts.append("</div>")

        # cada det Ai
        for idx in range(n):
            # construir Ai
            M = [row[:] for row in A]
            for i in range(n):
                M[i][idx] = b[i]
            html_parts.append("<div style='display:inline-block; margin:6px 18px; text-align:center;'>")
            html_parts.append(f"<div style='font-weight:600'>&#124;A<sub>{idx+1}</sub>&#124; =</div>")
            html_parts.append(_matrix_block_html(M))
            html_parts.append(f"<div style='margin-top:6px; font-weight:700;'>= {_fmt_fraction(det_vars[idx])}</div>")
            html_parts.append("</div>")

        html_parts.append("</div>")

        # finalmente mostrar solución compacta (con formato completo: det/ det = valor)
        html_parts.append("<div style='margin-top:12px; text-align:center; font-weight:700;'>Solución:</div>")
        sol_html_lines = []
        if detA == 0:
            sol_html_lines.append("det(A) = 0 → El método de Cramer no es aplicable.")
        else:
            for i, detk in enumerate(det_vars):
                val = detk / detA
                # formatear como: x1 = |A1|/|A| = 24/-12 = -2
                left = f"x{i+1} = "
                frac = f"|A{i+1}| / |A| = {_fmt_fraction(detk)} / {_fmt_fraction(detA)} = {_fmt_fraction(val)}"
                sol_html_lines.append(left + frac)
        # usar <pre> para mantener alineación y un recuadro un poco más grande
        html_parts.append("<pre style='font-family:Consolas,monospace; font-size:15px; text-align:left; display:inline-block; padding:12px; margin-top:8px; border:1px solid #ddd; border-radius:6px; background:#fff;'>")
        html_parts.append("\n".join(sol_html_lines))
        html_parts.append("</pre>")

        html_parts.append("</div>")
        proc_html = "\n".join(html_parts)
        try:
            # aumentar ligeramente el tamaño visible del QTextEdit para el procedimiento
            self.procedimiento.setMinimumHeight(340)
            self.procedimiento.setHtml(proc_html)
        except Exception:
            # fallback a texto simple
            self.procedimiento.setPlainText("Regla de Cramer:\n" + "\n".join(sol_html_lines))

        # rellenar detalles de cálculos de determinantes (no visible por defecto)
        detalles_text = []
        detalles_text.append("Cálculos detallados de determinantes:\n")
        detalles_text.append("-- det(A) --")
        detalles_text.extend(pasosA)
        detalles_text.append("\n")
        for idx in range(n):
            detalles_text.append(f"-- det sustituyendo columna x{idx+1} --")
            detalles_text.extend(det_steps[f"det_var_{idx+1}"])
            detalles_text.append("\n")

        self.detalles_text.setPlainText("\n".join(detalles_text))
