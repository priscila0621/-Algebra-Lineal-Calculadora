from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QScrollArea, QGridLayout, QLineEdit, QTextEdit, QMessageBox, QFrame
)
from PySide6.QtCore import Qt
from fractions import Fraction


def _parse_fraction(s: str) -> Fraction:
    s = (s or "").strip()
    if s == "":
        return Fraction(0)
    return Fraction(s.replace(",", "."))


def _matrix_widget(parent: QWidget, mat):
    grid = QGridLayout()
    grid.setHorizontalSpacing(6)
    grid.setVerticalSpacing(6)
    wrapper = QWidget(parent)
    wrapper.setLayout(grid)
    for i, row in enumerate(mat):
        for j, val in enumerate(row):
            lbl = QLabel(str(val))
            lbl.setAlignment(Qt.AlignCenter)
            lbl.setStyleSheet("background:#fff0f5;border:1px solid #ccc;padding:6px;font-family:Segoe UI;")
            grid.addWidget(lbl, i, j)
    return wrapper


class _BaseMatrixWindow(QMainWindow):
    def __init__(self, title: str, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        outer = QWidget(); self.setCentralWidget(outer)
        self.lay = QVBoxLayout(outer)
        self.lay.setContentsMargins(24, 24, 24, 24)
        self.lay.setSpacing(14)

        hdr = QLabel(title)
        hdr.setObjectName("Title")
        self.lay.addWidget(hdr)

        top = QHBoxLayout()
        self.lay.addLayout(top)
        self.f_edit = QLineEdit("2"); self.f_edit.setFixedWidth(60); self.f_edit.setAlignment(Qt.AlignCenter)
        self.c_edit = QLineEdit("2"); self.c_edit.setFixedWidth(60); self.c_edit.setAlignment(Qt.AlignCenter)
        top.addWidget(QLabel("Filas:")); top.addWidget(self.f_edit)
        top.addSpacing(12)
        top.addWidget(QLabel("Columnas:")); top.addWidget(self.c_edit)
        self.btn_crear = QPushButton("Crear matrices")
        self.btn_crear.clicked.connect(self._crear)
        top.addSpacing(16)
        top.addWidget(self.btn_crear)
        top.addStretch(1)

        self.scroll = QScrollArea(); self.scroll.setWidgetResizable(True)
        self.scrollw = QWidget(); self.scroll.setWidget(self.scrollw)
        self.grid = QGridLayout(self.scrollw)
        self.grid.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.lay.addWidget(self.scroll, 1)

        self.btn_run = QPushButton("Calcular")
        self.btn_run.setEnabled(False)
        self.btn_run.clicked.connect(self._run)
        self.lay.addWidget(self.btn_run)

        self.result_box = QTextEdit(); self.result_box.setReadOnly(True)
        self.result_box.setStyleSheet("font-family:Consolas,monospace;font-size:12px;")
        self.lay.addWidget(self.result_box, 1)

        self.entries = []

    def _crear(self):
        try:
            self._setup_entries()
        except Exception as exc:
            QMessageBox.warning(self, "Aviso", f"Datos invÃ¡lidos: {exc}")

    def _setup_entries(self):
        # override in subclasses for multiple matrices
        for i in reversed(range(self.grid.count())):
            w = self.grid.itemAt(i).widget()
            if w: w.setParent(None)
        filas = int(self.f_edit.text()); cols = int(self.c_edit.text())
        self.entries = []
        g = QGridLayout(); g.setHorizontalSpacing(6); g.setVerticalSpacing(6)
        box = QFrame(); box.setLayout(g)
        self.grid.addWidget(QLabel("Matriz"), 0, 0, alignment=Qt.AlignHCenter)
        self.grid.addWidget(box, 1, 0)
        for i in range(filas):
            row = []
            for j in range(cols):
                e = QLineEdit(); e.setAlignment(Qt.AlignCenter); e.setPlaceholderText("0")
                g.addWidget(e, i, j)
                row.append(e)
            self.entries.append(row)
        self.btn_run.setEnabled(True)

    def _leer(self):
        filas = len(self.entries)
        cols = len(self.entries[0]) if filas else 0
        A = []
        for i in range(filas):
            row = []
            for j in range(cols):
                row.append(_parse_fraction(self.entries[i][j].text()))
            A.append(row)
        return A

    def _run(self):
        raise NotImplementedError


class SumaMatricesWindow(_BaseMatrixWindow):
    def __init__(self, parent=None):
        super().__init__("Suma de Matrices", parent)
        self.num_edit = QLineEdit("2"); self.num_edit.setFixedWidth(60); self.num_edit.setAlignment(Qt.AlignCenter)
        self.lay.itemAt(1).layout().insertWidget(0, QLabel("NÂº matrices:"))
        self.lay.itemAt(1).layout().insertWidget(1, self.num_edit)

    def _setup_entries(self):
        for i in reversed(range(self.grid.count())):
            w = self.grid.itemAt(i).widget()
            if w: w.setParent(None)
        filas = int(self.f_edit.text()); cols = int(self.c_edit.text()); n = int(self.num_edit.text())
        self.entries = []
        for m in range(n):
            g = QGridLayout(); g.setHorizontalSpacing(6); g.setVerticalSpacing(6)
            box = QFrame(); box.setLayout(g)
            self.grid.addWidget(QLabel(f"Matriz {m+1}"), 0, m, alignment=Qt.AlignHCenter)
            self.grid.addWidget(box, 1, m)
            mat_entries = []
            for i in range(filas):
                row = []
                for j in range(cols):
                    e = QLineEdit(); e.setAlignment(Qt.AlignCenter); e.setPlaceholderText("0")
                    g.addWidget(e, i, j)
                    row.append(e)
                mat_entries.append(row)
            self.entries.append(mat_entries)
        self.btn_run.setEnabled(True)

    def _leer_all(self):
        mats = []
        for grid in self.entries:
            filas = len(grid); cols = len(grid[0]) if filas else 0
            M = []
            for i in range(filas):
                row = []
                for j in range(cols):
                    row.append(_parse_fraction(grid[i][j].text()))
                M.append(row)
            mats.append(M)
        return mats

    def _run(self):
        mats = self._leer_all()
        filas = len(mats[0]); cols = len(mats[0][0]) if filas else 0
        result = [[sum(m[i][j] for m in mats) for j in range(cols)] for i in range(filas)]
        def format_matrix_lines(M):
            if not M: return []
            w = max(len(str(x)) for r in M for x in r)
            lines = []
            for i, r in enumerate(M):
                if i == 0:
                    l, rbr = "\u23A1", "\u23A4"  # âŽ¡ âŽ¤
                elif i == len(M)-1:
                    l, rbr = "\u23A3", "\u23A6"  # âŽ£ âŽ¦
                else:
                    l, rbr = "\u23A2", "\u23A5"  # âŽ¢ âŽ¥
                body = " ".join(str(x).rjust(w) for x in r)
                lines.append(f"{l} {body} {rbr}")
            return lines
        self.result_box.clear()
        self.result_box.insertPlainText("Matriz resultante\n\n")
        for ln in format_matrix_lines(result):
            self.result_box.insertPlainText(ln + "\n")
        self.result_box.insertPlainText("\nDetalle de la suma por posiciÃ³n\n")
        for i in range(filas):
            for j in range(cols):
                parts = " + ".join(str(m[i][j]) for m in mats)
                self.result_box.insertPlainText(f"[{i+1},{j+1}]: {parts} = {result[i][j]}\n")


class RestaMatricesWindow(SumaMatricesWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Resta de Matrices")
        try:
            header = self.findChild(QLabel, "Title")
            if header is not None:
                header.setText("Resta de Matrices")
        except Exception:
            pass

    def _run(self):
        mats = self._leer_all()
        filas = len(mats[0]); cols = len(mats[0][0]) if filas else 0
        result = [[mats[0][i][j] - sum(mats[k][i][j] for k in range(1, len(mats))) for j in range(cols)] for i in range(filas)]
        def _fmt_mat(M):
            if not M: return []
            w = max(len(str(x)) for r in M for x in r)
            out = []
            for i, r in enumerate(M):
                if i == 0: l,rbr = "\u23A1","\u23A4"
                elif i == len(M)-1: l,rbr = "\u23A3","\u23A6"
                else: l,rbr = "\u23A2","\u23A5"
                out.append(f"{l} {' '.join(str(x).rjust(w) for x in r)} {rbr}")
            return out
        self.result_box.clear()
        self.result_box.insertPlainText("Matriz resultante\n\n")
        for ln in _fmt_mat(result):
            self.result_box.insertPlainText(ln + "\n")
        self.result_box.insertPlainText("\nDetalle de la resta por posición\n")
        for i in range(filas):
            for j in range(cols):
                parts = " - ".join(str(mats[k][i][j]) for k in range(len(mats)))
                self.result_box.insertPlainText(f"[{i+1},{j+1}]: {parts} = {result[i][j]}\n")


class MultiplicacionMatricesWindow(_BaseMatrixWindow):
    def __init__(self, parent=None):
        super().__init__("Multiplicación de Matrices", parent)
        # Para multiplicaciÃ³n pedimos A (f x c) y B (c x p)
        self.p_edit = QLineEdit("2"); self.p_edit.setFixedWidth(60); self.p_edit.setAlignment(Qt.AlignCenter)
        row = self.lay.itemAt(1).layout()
        row.addSpacing(12); row.addWidget(QLabel("Columnas B:")); row.addWidget(self.p_edit)
        # Encadenar: botón para usar el último resultado como A
        self._last_result = None
        self._chain_btn = QPushButton("Usar resultado como A")
        self._chain_btn.setEnabled(False)
        self._chain_btn.clicked.connect(self._use_result_as_A)
        self.lay.addWidget(self._chain_btn)

    def _setup_entries(self):
        for i in reversed(range(self.grid.count())):
            w = self.grid.itemAt(i).widget()
            if w: w.setParent(None)
        f = int(self.f_edit.text()); c = int(self.c_edit.text()); p = int(self.p_edit.text())
        self.entries = []
        for m, (rows, cols) in enumerate(((f, c), (c, p))):
            g = QGridLayout(); g.setHorizontalSpacing(6); g.setVerticalSpacing(6)
            box = QFrame(); box.setLayout(g)
            self.grid.addWidget(QLabel("Matriz A" if m == 0 else "Matriz B"), 0, m, alignment=Qt.AlignHCenter)
            self.grid.addWidget(box, 1, m)
            mat_entries = []
            for i in range(rows):
                row = []
                for j in range(cols):
                    e = QLineEdit(); e.setAlignment(Qt.AlignCenter); e.setPlaceholderText("0")
                    g.addWidget(e, i, j)
                    row.append(e)
                mat_entries.append(row)
            self.entries.append(mat_entries)
        self.btn_run.setEnabled(True)

    def _run(self):
        Agrid, Bgrid = self.entries
        A = [[_parse_fraction(e.text()) for e in row] for row in Agrid]
        B = [[_parse_fraction(e.text()) for e in row] for row in Bgrid]
        fa, ca = len(A), len(A[0]) if A else 0
        fb, cb = len(B), len(B[0]) if B else 0
        if ca != fb:
            QMessageBox.warning(self, "Aviso", "Las columnas de A deben coincidir con las filas de B.")
            return
        R = [[Fraction(0) for _ in range(cb)] for _ in range(fa)]
        pasos = []
        for i in range(fa):
            for j in range(cb):
                terms = []
                s = Fraction(0)
                for k in range(ca):
                    a = A[i][k]; b = B[k][j]
                    terms.append(f"{a}*{b}")
                    s += a * b
                R[i][j] = s
                pasos.append(f"c{i+1}{j+1} = " + " + ".join(terms) + f" = {s}")
        def _fmt_mat(M):
            if not M: return []
            w = max(len(str(x)) for r in M for x in r)
            out = []
            for i, r in enumerate(M):
                if i == 0: l,rbr = "\u23A1","\u23A4"
                elif i == len(M)-1: l,rbr = "\u23A3","\u23A6"
                else: l,rbr = "\u23A2","\u23A5"
                out.append(f"{l} {' '.join(str(x).rjust(w) for x in r)} {rbr}")
            return out
        self.result_box.clear()
        self.result_box.insertPlainText("Matriz resultante\n\n")
        for ln in _fmt_mat(R):
            self.result_box.insertPlainText(ln + "\n")
        self.result_box.insertPlainText("\n")
        self.result_box.insertPlainText("Procedimiento paso a paso:\n")
        for line in pasos:
            self.result_box.insertPlainText(line + "\n")
        # Habilitar encadenado del resultado para nueva multiplicación
        self._last_result = R
        try:
            self._chain_btn.setEnabled(True)
        except Exception:
            pass

    def _use_result_as_A(self):
        if not hasattr(self, "_last_result") or not self._last_result:
            return
        fa = len(self._last_result)
        cb = len(self._last_result[0]) if fa else 0
        self.f_edit.setText(str(fa))
        self.c_edit.setText(str(cb))
        # reconstruir grillas y volcar resultado en A
        self._setup_entries()
        try:
            Agrid, _Bgrid = self.entries
        except Exception:
            return
        for i in range(fa):
            for j in range(cb):
                Agrid[i][j].setText(str(self._last_result[i][j]))


class TranspuestaMatrizWindow(_BaseMatrixWindow):
    def __init__(self, parent=None):
        super().__init__("Transpuesta de Matriz", parent)

    def _run(self):
        A = self._leer()
        f = len(A); c = len(A[0]) if f else 0
        T = [[A[i][j] for i in range(f)] for j in range(c)]
        pasos = []
        for i in range(f):
            for j in range(c):
                pasos.append(f"Paso {len(pasos)+1}: A[{i+1},{j+1}] -> T[{j+1},{i+1}] = {A[i][j]}")
        self.result_box.clear()
        self.result_box.insertPlainText("Resultado (Transpuesta)\n\n")
        self.result_box.insertPlainText("\n".join(" ".join(str(v) for v in row) for row in T) + "\n\n")
        self.result_box.insertPlainText("Pasos detallados\n")
        for line in pasos:
            self.result_box.insertPlainText(line + "\n")


class DeterminanteMatrizWindow(_BaseMatrixWindow):
    def __init__(self, parent=None):
        super().__init__("Determinante de Matriz", parent)

    def _run(self):
        A = self._leer()
        det, steps = determinante_con_pasos(A)
        self.result_box.clear()
        self.result_box.insertPlainText("Pasos detallados\n\n")
        for s in steps:
            self.result_box.insertPlainText(s + "\n")
        self.result_box.insertPlainText(f"\nDeterminante: {det}\n")


# LÃ³gica de determinante con el mismo formato que Tk
def determinante_con_pasos(matrix, level: int = 0):
    n = len(matrix)
    indent = "    " * level
    steps = []
    separator = indent + ("-" * 70)
    def fmt(x: Fraction) -> str:
        if isinstance(x, Fraction):
            return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"
        return str(x)
    def matrix_lines(M, ind=""):
        return [ind + "[ " + "  ".join(fmt(c) for c in r) + " ]" for r in M]
    def is_upper(M):
        n = len(M)
        for i in range(1, n):
            for j in range(0, i):
                if M[i][j] != 0: return False
        return True
    def is_lower(M):
        n = len(M)
        for i in range(n):
            for j in range(i+1, n):
                if M[i][j] != 0: return False
        return True
    def minor(M, r, c):
        return [[M[i][j] for j in range(len(M)) if j != c] for i in range(len(M)) if i != r]

    if n == 1:
        value = matrix[0][0]
        steps.append(f"{indent}Caso base 1Ã—1: det(A) = {fmt(value)}")
        return value, steps
    if n == 2:
        a11, a12 = matrix[0]
        a21, a22 = matrix[1]
        prod1 = a11 * a22
        prod2 = a12 * a21
        det = prod1 - prod2
        steps.append(f"{indent}Caso base 2Ã—2:")
        steps.extend(matrix_lines(matrix, indent + "    "))
        steps.append(f"{indent}det(A) = ({fmt(a11)} Â· {fmt(a22)}) âˆ’ ({fmt(a12)} Â· {fmt(a21)}) = {fmt(prod1)} âˆ’ {fmt(prod2)} = {fmt(det)}")
        return det, steps

    if is_upper(matrix) or is_lower(matrix):
        tipo = "superior" if is_upper(matrix) else "inferior"
        diag = [matrix[i][i] for i in range(n)]
        det = Fraction(1)
        for v in diag: det *= v
        diag_product = " Â· ".join(fmt(v) for v in diag)
        steps.append(f"{indent}La matriz es triangular {tipo}.")
        steps.append(f"{indent}Producto de la diagonal principal: {diag_product} = {fmt(det)}")
        return det, steps

    steps.append(f"{indent}ExpansiÃ³n por cofactores a lo largo de la primera fila")
    formula = " + ".join(f"aâ‚{j+1}Câ‚{j+1}" for j in range(n))
    steps.append(f"{indent}det(A) = {formula}")

    contributions = []
    summary_values = []
    for j in range(n):
        elemento = matrix[0][j]
        sign = Fraction(1 if j % 2 == 0 else -1)
        sign_symbol = "+" if sign >= 0 else "âˆ’"
        steps.append(separator)
        steps.append(f"{indent}Elemento aâ‚{j+1} = {fmt(elemento)} (signo {sign_symbol})")
        if elemento == 0:
            steps.append(f"{indent}Como aâ‚{j+1} = 0, su contribuciÃ³n es nula y se omite.")
            contributions.append(Fraction(0)); summary_values.append(Fraction(0)); continue
        sub = minor(matrix, 0, j)
        steps.append(f"{indent}Submatriz Mâ‚{j+1} (eliminando fila 1 y columna {j+1}):")
        steps.extend(matrix_lines(sub, indent + "    "))
        sub_det, sub_steps = determinante_con_pasos(sub, level + 1)
        steps.extend(sub_steps)
        steps.append(f"{indent}det(Mâ‚{j+1}) = {fmt(sub_det)}")
        cofactor_value = sign * sub_det
        steps.append(f"{indent}Câ‚{j+1} = ({'+' if sign >= 0 else 'âˆ’'}{fmt(abs(sign))}) Â· {fmt(sub_det)} = {fmt(cofactor_value)}")
        contrib = elemento * cofactor_value
        steps.append(f"{indent}ContribuciÃ³n parcial: {fmt(elemento)} Â· {fmt(cofactor_value)} = {fmt(contrib)}")
        contributions.append(contrib); summary_values.append(contrib)
    steps.append(separator)
    total = sum(contributions, Fraction(0))
    partes = " + ".join((str(v) if isinstance(v, str) else fmt(v)) for v in summary_values)
    steps.append(f"{indent}Suma total de contribuciones: det(A) = {partes} = {fmt(total)}")
    return total, steps


class InversaMatrizWindow(_BaseMatrixWindow):
    def __init__(self, parent=None):
        super().__init__("Inversa de Matriz", parent)

    def _setup_entries(self):
        # Fuerza matriz cuadrada: usa filas para columnas
        for i in reversed(range(self.grid.count())):
            w = self.grid.itemAt(i).widget()
            if w: w.setParent(None)
        n = int(self.f_edit.text())
        self.c_edit.setText(str(n))
        self.entries = []
        g = QGridLayout(); g.setHorizontalSpacing(6); g.setVerticalSpacing(6)
        box = QFrame(); box.setLayout(g)
        self.grid.addWidget(QLabel("Matriz A (nÃ—n)"), 0, 0, alignment=Qt.AlignHCenter)
        self.grid.addWidget(box, 1, 0)
        for i in range(n):
            row = []
            for j in range(n):
                e = QLineEdit(); e.setAlignment(Qt.AlignCenter); e.setPlaceholderText("0")
                g.addWidget(e, i, j)
                row.append(e)
            self.entries.append(row)
        self.btn_run.setEnabled(True)

    def _run(self):
        A = self._leer()
        n = len(A)
        if n == 0 or any(len(r) != n for r in A):
            QMessageBox.warning(self, "Aviso", "Ingrese una matriz cuadrada nÃ—n.")
            return
        # convertir a Fraction y construir identidad
        Aw = [[_parse_fraction(str(x)) for x in row] for row in A]
        Iw = [[Fraction(1 if i == j else 0) for j in range(n)] for i in range(n)]

        def augmented_lines(Ax, Ix):
            ancho = 1
            for i in range(n):
                for v in Ax[i] + Ix[i]:
                    ancho = max(ancho, len(str(v)))
            lines = []
            for i in range(n):
                left = " ".join(str(x).rjust(ancho) for x in Ax[i])
                right = " ".join(str(x).rjust(ancho) for x in Ix[i])
                lines.append(f"{left}   |   {right}")
            return lines

        def operacion_vertical_aug(fp, fa, f, fr):
            # fp, fa, fr ya son filas completas (A|I) como listas
            ancho = max(len(str(x)) for x in fr) if fr else 1
            def fmt(lst):
                return " ".join(str(x).rjust(ancho) for x in lst)
            escala = [(-f) * val for val in fp]
            factor_str = f"+{abs(f)}" if f < 0 else f"-{f}"
            lines = [
                f"{factor_str}R : {fmt(escala)}",
                f"+R        : {fmt(fa)}",
                " " * 10 + "-" * (ancho * len(fr) + len(fr) - 1),
                f"=R        : {fmt(fr)}",
            ]
            return lines

        self.result_box.clear()
        fila_pivote = 0
        pivot_cols = []
        for col in range(n):
            piv = None
            for r in range(fila_pivote, n):
                if Aw[r][col] != 0:
                    piv = r; break
            if piv is None:
                continue
            if piv != fila_pivote:
                Aw[fila_pivote], Aw[piv] = Aw[piv], Aw[fila_pivote]
                Iw[fila_pivote], Iw[piv] = Iw[piv], Iw[fila_pivote]
                self.result_box.insertPlainText("OperaciÃ³n: ")
                self.result_box.insertPlainText(f"R{fila_pivote+1} \u2194 R{piv+1}\n\n")
                for ln in augmented_lines(Aw, Iw):
                    self.result_box.insertPlainText(ln + "\n")
                self.result_box.insertPlainText("\n" + ("-" * 110) + "\n\n")

            a = Aw[fila_pivote][col]
            if a == 0:
                fila_pivote += 1
                if fila_pivote >= n: break
                continue
            if a != 1:
                Aw[fila_pivote] = [v / a for v in Aw[fila_pivote]]
                Iw[fila_pivote] = [v / a for v in Iw[fila_pivote]]
                self.result_box.insertPlainText("OperaciÃ³n: ")
                self.result_box.insertPlainText(f"R{fila_pivote+1} \u2192 R{fila_pivote+1}/{a}\n\n")
                for ln in augmented_lines(Aw, Iw):
                    self.result_box.insertPlainText(ln + "\n")
                self.result_box.insertPlainText("\n" + ("-" * 110) + "\n\n")

            for r in range(n):
                if r == fila_pivote: continue
                f = Aw[r][col]
                if f == 0: continue
                origA = Aw[r][:]; origI = Iw[r][:]
                pivA = Aw[fila_pivote][:]; pivI = Iw[fila_pivote][:]
                Aw[r] = [origA[j] - f * pivA[j] for j in range(n)]
                Iw[r] = [origI[j] - f * pivI[j] for j in range(n)]
                fp = pivA + pivI
                fa = origA + origI
                fr = Aw[r] + Iw[r]
                left_lines = operacion_vertical_aug(fp, fa, f, fr)
                right_lines = augmented_lines(Aw, Iw)
                self.result_box.insertPlainText("OperaciÃ³n: ")
                self.result_box.insertPlainText(f"R{r+1} \u2192 R{r+1} - ({f})R{fila_pivote+1}\n\n")
                max_left = max(len(s) for s in left_lines) if left_lines else 0
                sep = "   |   "
                max_len = max(len(left_lines), len(right_lines))
                for i in range(max_len):
                    l = left_lines[i] if i < len(left_lines) else ""
                    rr = right_lines[i] if i < len(right_lines) else ""
                    self.result_box.insertPlainText(l.ljust(max_left) + (sep if rr else "") + rr + "\n")
                self.result_box.insertPlainText("\n" + ("-" * 110) + "\n\n")

            pivot_cols.append(col)
            fila_pivote += 1
            if fila_pivote >= n: break

        if len(pivot_cols) != n:
            self.result_box.insertPlainText("La matriz no es invertible (no se encontraron n pivotes).\n")
            return

        # Mostrar inversa
        self.result_box.insertPlainText("Matriz inversa:\n\n")
        self.result_box.insertPlainText("\n".join(" ".join(str(v) for v in row) for row in Iw) + "\n")






