from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QScrollArea, QGridLayout, QLineEdit, QTextEdit, QMessageBox, QFrame
)
from PySide6.QtCore import Qt
from fractions import Fraction
from copy import deepcopy


def _fmt(x):
    try:
        return str(x)
    except Exception:
        return f"{x}"


class GaussJordanWindow(QMainWindow):
    def __init__(self, parent=None, start_with_independencia=False):
        super().__init__(parent)
        self.setWindowTitle("Método de Eliminación de Gauss-Jordan")
        self._entries = []
        self._rows = 3
        self._cols_no_b = 3
        self.pasos_guardados = []
        self.matriz_final = None
        self.matriz_original = None
        self.detalle_button = None
        self.mostrando_detalles = False

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
        self.btn_verif_indep = QPushButton("Verificar independencia")
        self.btn_verif_indep.clicked.connect(self._verificar_independencia)
        top.addWidget(self.btn_verif_indep)
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
        self.result = QTextEdit()
        self.result.setReadOnly(True)
        self.result.setStyleSheet("font-family: Consolas, monospace; font-size: 12px;")
        main.addWidget(self.result, 1)

        self.btn_resolver = QPushButton("Resolver")
        self.btn_resolver.clicked.connect(self._resolver)
        self.btn_resolver.setEnabled(False)
        main.addWidget(self.btn_resolver)

        bottom = QHBoxLayout()
        main.addLayout(bottom)
        bottom.addStretch(1)
        self.detalle_button = QPushButton("Ver pasos detallados")
        self.detalle_button.setEnabled(False)
        self.detalle_button.clicked.connect(self._toggle_detalles)
        bottom.addWidget(self.detalle_button)

        self._rebuild_grid(self._rows, self._cols_no_b + 1)

    def _limpiar(self):
        self._entries = []
        while self.grid_layout.count():
            w = self.grid_layout.takeAt(0).widget()
            if w:
                w.deleteLater()
        self.result.clear()
        self.btn_resolver.setEnabled(False)

    def _rebuild_grid(self, filas: int, columnas: int):
        old = [[e.text() for e in row] for row in self._entries] if self._entries else []
        self._limpiar()
        for j in range(columnas - 1):
            h = QLabel(f"x{j+1}")
            h.setStyleSheet("font-weight: 700;")
            self.grid_layout.addWidget(h, 0, j)
        hb = QLabel("b")
        hb.setStyleSheet("font-weight: 700;")
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
                vals.append(Fraction(s))
            A.append(vals)
        return A

    def _resolver(self):
        try:
            A = self._leer_matriz()
            filas = len(A)
            cols = len(A[0])
            self.matriz_original = deepcopy(A)
            pasos = gauss_jordan(A, filas, cols)
            self.pasos_guardados = pasos
            self.matriz_final = A
            self._mostrar_resumen()
            self.detalle_button.setEnabled(True)
        except Exception as exc:
            QMessageBox.critical(self, "Error", f"Entrada inválida: {exc}")

    def _insert_header(self, titulo: str, comentario: str = ""):
        self.result.insertPlainText("Operación: ")
        self.result.insertPlainText(titulo)
        if comentario:
            self.result.insertPlainText("  \u2014  ")
            self.result.insertPlainText(comentario)
        self.result.insertPlainText("\n\n")

    def _mostrar_detalles(self):
        self.result.clear()
        for step in self.pasos_guardados:
            self._insert_header(step.get("titulo", ""), step.get("comentario", ""))
            oper_lines = step.get("oper_lines", [])
            matriz_lines = step.get("matriz_lines", [])
            max_left = max((len(s) for s in oper_lines), default=0)
            sep = "   |   "
            max_len = max(len(oper_lines), len(matriz_lines))
            for i in range(max_len):
                left = oper_lines[i] if i < len(oper_lines) else ""
                right = matriz_lines[i] if i < len(matriz_lines) else ""
                line_text = left.ljust(max_left) + (sep if right else "") + right
                self.result.insertPlainText(line_text + "\n")
            self.result.insertPlainText("\n" + ("-" * 110) + "\n\n")
        self.result.insertPlainText("===== SOLUCIÓN FINAL =====\n")
        soluciones, tipo, _ = _extraer_soluciones(self.matriz_final)
        for i, val in enumerate(soluciones):
            self.result.insertPlainText(f"x{i+1} = {val}\n")

    def _mostrar_resumen(self):
        self.result.clear()
        self.result.insertPlainText("===== SOLUCIÓN FINAL =====\n")
        if self.matriz_final is None:
            self.result.insertPlainText("(no hay soluciones calculadas)\n")
            return
        soluciones, tipo, analisis = _extraer_soluciones(self.matriz_final)
        if tipo == "incompatible":
            self.result.insertPlainText("El sistema es inconsistente: aparece una fila del tipo 0 = b con b≠0\n")
            return
        if tipo == "determinado":
            self.result.insertPlainText("El sistema tiene solución única:\n\n")
        elif tipo == "indeterminado":
            self.result.insertPlainText("El sistema tiene infinitas soluciones:\n\n")
        for i, val in enumerate(soluciones):
            self.result.insertPlainText(f"x{i+1} = {val}\n")

        # Forma vectorial estilo libro cuando hay variables libres
        if tipo == "indeterminado":
            pivot_cols, free_cols, pivot_row_for_col = analisis
            if free_cols:
                self.result.insertPlainText("\nConjunto solución:\n\n")
                num_vars = len(soluciones)
                # Vector particular (libres = 0)
                particular = []
                for j in range(num_vars):
                    if j in free_cols:
                        particular.append(Fraction(0))
                    else:
                        irow = pivot_row_for_col.get(j, None)
                        particular.append(self.matriz_final[irow][-1] if irow is not None else Fraction(0))
                # Vectores base de cada libre
                vectores_libres = []
                for l in free_cols:
                    v = [Fraction(0)] * num_vars
                    v[l] = Fraction(1)
                    for j in pivot_cols:
                        irow = pivot_row_for_col[j]
                        v[j] = -self.matriz_final[irow][l]
                    vectores_libres.append(v)

                es_homogeneo = all(self.matriz_original[i][-1] == 0 for i in range(len(self.matriz_original))) if self.matriz_original else False
                if not es_homogeneo:
                    nombres = ["  "] + [f"x{l+1}" for l in free_cols]
                    vectores = [particular] + vectores_libres
                else:
                    nombres = [f"x{l+1}" for l in free_cols]
                    vectores = vectores_libres

                lines = vectores_columna_lado_a_lado(vectores, nombres, espacio_entre_vectores=4)
                imprimir_vectores_con_x_igual(self.result, lines)
                self.result.insertPlainText("\nDonde " + ", ".join([f"x{l+1}" for l in free_cols]) + " ∈ ℝ (parámetros libres).\n")

    def _toggle_detalles(self):
        if not self.pasos_guardados:
            return
        if self.mostrando_detalles:
            self._mostrar_resumen()
            self.detalle_button.setText("Ver pasos detallados")
            self.mostrando_detalles = False
        else:
            self._mostrar_detalles()
            self.detalle_button.setText("Ocultar pasos detallados")
            self.mostrando_detalles = True

    def _verificar_independencia(self):
        try:
            A = self._leer_matriz()
            vectores = list(map(list, zip(*[row[:-1] for row in A])))
            from independencia_lineal import son_linealmente_independientes
            ok, texto = son_linealmente_independientes(vectores)
            QMessageBox.information(self, "Independencia lineal", texto)
        except Exception as exc:
            QMessageBox.warning(self, "Aviso", f"No se pudo verificar: {exc}")

    def _go_back(self):
        try:
            p = self.parent()
            self.close()
            if p is not None:
                p.show()
                p.activateWindow()
        except Exception:
            self.close()


def gauss_jordan(A, n, m):
    pasos = []
    fila_pivote = 0
    for col in range(m - 1):
        pivote = None
        for f in range(fila_pivote, n):
            if A[f][col] != 0:
                pivote = f
                break
        if pivote is None:
            continue
        if pivote != fila_pivote:
            A[fila_pivote], A[pivote] = A[pivote], A[fila_pivote]
            pasos.append({
                "titulo": f"F{fila_pivote+1} \u2194 F{pivote+1}",
                "comentario": f"Intercambio de filas para poner un pivote no nulo en la columna {col+1}",
                "oper_lines": [],
                "matriz_lines": format_matriz_lines(A)
            })
        divisor = A[fila_pivote][col]
        if divisor == 0:
            fila_pivote += 1
            continue
        if divisor != 1:
            A[fila_pivote] = [val / divisor for val in A[fila_pivote]]
            pasos.append({
                "titulo": f"F{fila_pivote+1} \u2192 F{fila_pivote+1}/{_fmt(divisor)}",
                "comentario": f"Normalización: se convierte en pivote a 1 en la columna {col+1}",
                "oper_lines": [],
                "matriz_lines": format_matriz_lines(A)
            })
        for f in range(n):
            if f != fila_pivote and A[f][col] != 0:
                factor = A[f][col]
                original_fila = A[f][:]
                A[f] = [original_fila[j] - factor * A[fila_pivote][j] for j in range(m)]
                oper_lines = format_operacion_vertical_lines(
                    A[fila_pivote], original_fila, factor, A[f], fila_pivote + 1, f + 1
                )
                pasos.append({
                    "titulo": f"F{f+1} \u2192 F{f+1} - ({_fmt(factor)})F{fila_pivote+1}",
                    "comentario": f"Se anula el elemento en la columna {col+1} usando la fila pivote",
                    "oper_lines": oper_lines,
                    "matriz_lines": format_matriz_lines(A)
                })
        fila_pivote += 1
        if fila_pivote >= n:
            break
    return pasos


def format_operacion_vertical_lines(fila_pivote, fila_actual, factor, fila_result, idx_piv, idx_obj):
    ancho = max(len(str(x)) for x in fila_result) if fila_result else 1

    def fmt(lst):
        return " ".join(str(x).rjust(ancho) for x in lst)

    escala = [(-factor) * val for val in fila_pivote]

    if factor < 0:
        factor_str = f"+{abs(factor)}"
    else:
        factor_str = f"-{factor}"

    lines = [
        f"{factor_str}F{idx_piv} : {fmt(escala)}",
        f"+F{idx_obj}   : {fmt(fila_actual)}",
        " " * 10 + "-" * (ancho * len(fila_result) + len(fila_result) - 1),
        f"=F{idx_obj}   : {fmt(fila_result)}"
    ]
    return lines


def format_matriz_lines(A):
    ancho = 1
    for fila in A:
        for x in fila:
            ancho = max(ancho, len(str(x)))
    lines = []
    for fila in A:
        line = " ".join(str(x).rjust(ancho) for x in fila)
        lines.append(line)
    return lines


# Helpers para análisis de RREF y forma vectorial
def _analizar_rref(A):
    n = len(A); m = len(A[0]); num_vars = m - 1
    piv_col_por_fila = [-1] * n
    piv_fila_por_col = {}
    for i in range(n):
        for j in range(num_vars):
            if A[i][j] == 1 and all(A[k][j] == 0 for k in range(n) if k != i):
                piv_col_por_fila[i] = j
                piv_fila_por_col[j] = i
                break
    pivot_cols = [j for j in piv_col_por_fila if j != -1]
    free_cols = [j for j in range(num_vars) if j not in pivot_cols]
    return pivot_cols, free_cols, piv_fila_por_col


def _extraer_soluciones(A):
    n = len(A); m = len(A[0]); num_vars = m - 1
    # Incompatibilidad: [0 ... 0 | b≠0]
    for i in range(n):
        if all(A[i][j] == 0 for j in range(num_vars)) and A[i][-1] != 0:
            return None, "incompatible", ([], [], {})
    pivot_cols, free_cols, pivot_row_for_col = _analizar_rref(A)
    soluciones = [None] * num_vars
    if free_cols:
        for j in range(num_vars):
            if j in free_cols:
                soluciones[j] = f"x{j+1} es variable libre"
            else:
                irow = pivot_row_for_col.get(j, None)
                partes = []
                if irow is not None and A[irow][-1] != 0:
                    partes.append(str(A[irow][-1]))
                for l in free_cols:
                    if irow is not None:
                        coef = -A[irow][l]
                        if coef != 0:
                            partes.append(f"({coef})*x{l+1}")
                expr = " + ".join(partes) if partes else "0"
                soluciones[j] = expr
        return soluciones, "indeterminado", (pivot_cols, free_cols, pivot_row_for_col)
    else:
        # Determinado
        for j in range(num_vars):
            irow = pivot_row_for_col.get(j, None)
            soluciones[j] = A[irow][-1] if irow is not None else 0
        return soluciones, "determinado", (pivot_cols, free_cols, pivot_row_for_col)


def vectores_columna_lado_a_lado(vectores, nombres, espacio_entre_vectores=4):
    n = len(vectores[0]) if vectores else 0
    m = len(vectores)
    encabezados = [nombres[0]] + [f"+ {nombres[idx]}" for idx in range(1, m)]
    max_encabezado = max((len(e) for e in encabezados), default=0)
    max_num_len = 1
    for v in vectores:
        for fila in range(n):
            max_num_len = max(max_num_len, len(str(v[fila])))
    bloque_ancho = max_encabezado + 3 + max_num_len + 2
    sep = " " * espacio_entre_vectores
    lines = []
    for fila in range(n):
        line = ""
        for idx, v in enumerate(vectores):
            valstr = str(v[fila]).rjust(max_num_len)
            if fila == 0:
                li, ri = "\u23A1", "\u23A4"  # ⎡ ⎤
            elif fila == n - 1:
                li, ri = "\u23A3", "\u23A6"  # ⎣ ⎦
            else:
                li, ri = "\u23A2", "\u23A5"  # ⎢ ⎥
            if fila == 0:
                encabezado = encabezados[idx].rjust(max_encabezado)
                bloque = f"{encabezado} {li} {valstr} {ri}"
            else:
                bloque = " " * max_encabezado + f" {li} {valstr} {ri}"
            bloque = bloque.ljust(bloque_ancho)
            if idx < m - 1:
                bloque += sep
            line += bloque
        lines.append(line.rstrip())
    return lines


def imprimir_vectores_con_x_igual(editor: QTextEdit, lines):
    if not lines:
        return
    x_eq = "x ="
    first = lines[0]
    pos = first.find("\u23A1")
    pos = 0 if pos < 0 else pos
    x_pos = max(0, pos - len(x_eq) - 1)
    for i, l in enumerate(lines):
        if i == 0:
            editor.insertPlainText(" " * x_pos + x_eq + " " + l + "\n")
        else:
            editor.insertPlainText(" " * (x_pos + len(x_eq) + 1) + l + "\n")

