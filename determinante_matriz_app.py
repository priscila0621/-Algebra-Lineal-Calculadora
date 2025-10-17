import tkinter as tk
from tkinter import ttk, messagebox
from fractions import Fraction
from typing import List, Tuple


_SUBSCRIPT_MAP = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")


def _fmt(value: Fraction) -> str:
    if isinstance(value, Fraction):
        if value.denominator == 1:
            text = str(value.numerator)
        else:
            text = f"{value.numerator}/{value.denominator}"
    else:
        text = str(value)
    return text.replace("-", "\u2212")


def _sub(num: int) -> str:
    return str(num).translate(_SUBSCRIPT_MAP)


def _label(prefix: str, row: int, col: int) -> str:
    return f"{prefix}{_sub(row)}{_sub(col)}"


def _sign_factor_text(value: Fraction) -> str:
    return f"(+{_fmt(value)})" if value >= 0 else f"({_fmt(value)})"


def _fmt_factor(value: Fraction) -> str:
    return _fmt(value) if value >= 0 else f"({_fmt(value)})"


def _matrix_lines(matrix: List[List[Fraction]], indent: str = "") -> List[str]:
    lines = []
    for row in matrix:
        line = indent + "[ " + "  ".join(_fmt(col) for col in row) + " ]"
        lines.append(line)
    return lines


def _is_upper_triangular(matrix: List[List[Fraction]]) -> bool:
    n = len(matrix)
    for i in range(1, n):
        for j in range(0, i):
            if matrix[i][j] != 0:
                return False
    return True


def _is_lower_triangular(matrix: List[List[Fraction]]) -> bool:
    n = len(matrix)
    for i in range(n):
        for j in range(i + 1, n):
            if matrix[i][j] != 0:
                return False
    return True


def _minor(matrix: List[List[Fraction]], row: int, col: int) -> List[List[Fraction]]:
    return [
        [matrix[i][j] for j in range(len(matrix)) if j != col]
        for i in range(len(matrix))
        if i != row
    ]


def determinante_con_pasos(matrix: List[List[Fraction]], level: int = 0) -> Tuple[Fraction, List[str]]:
    n = len(matrix)
    indent = "    " * level
    steps: List[str] = []
    separator = indent + "─" * 70

    if n == 1:
        value = matrix[0][0]
        steps.append(f"{indent}Caso base 1×1: det(A) = {_fmt(value)}")
        return value, steps

    if n == 2:
        a11, a12 = matrix[0]
        a21, a22 = matrix[1]
        prod1 = a11 * a22
        prod2 = a12 * a21
        det = prod1 - prod2
        steps.append(f"{indent}Caso base 2×2:")
        steps.extend(_matrix_lines(matrix, indent + "    "))
        steps.append(
            f"{indent}det(A) = ({_fmt(a11)} × {_fmt(a22)}) − ({_fmt(a12)} × {_fmt(a21)}) "
            f"= {_fmt(prod1)} − {_fmt(prod2)} = {_fmt(det)}"
        )
        return det, steps

    es_superior = _is_upper_triangular(matrix)
    es_inferior = _is_lower_triangular(matrix)
    if es_superior or es_inferior:
        tipo = "superior" if es_superior else "inferior"
        diag = [matrix[i][i] for i in range(n)]
        det = Fraction(1)
        for value in diag:
            det *= value
        diag_product = " × ".join(_fmt(value) for value in diag)
        steps.append(f"{indent}La matriz es triangular {tipo}.")
        steps.append(f"{indent}Producto de la diagonal principal: {diag_product} = {_fmt(det)}")
        return det, steps

    steps.append(f"{indent}Expansión por cofactores a lo largo de la primera fila")
    formula = " + ".join(f"{_label('a', 1, j + 1)}{_label('C', 1, j + 1)}" for j in range(n))
    steps.append(f"{indent}det(A) = {formula}")

    contributions: List[Fraction] = []
    summary_values: List[Fraction] = []
    for j in range(n):
        elemento = matrix[0][j]
        idx_label = _label("a", 1, j + 1)
        sign_factor = Fraction(1 if j % 2 == 0 else -1)
        sign_symbol = "+" if sign_factor >= 0 else "−"

        steps.append(separator)
        steps.append(f"{indent}Elemento {idx_label} = {_fmt(elemento)} (signo {sign_symbol})")
        if elemento == 0:
            steps.append(f"{indent}Como {idx_label} = 0, su contribución es nula y se omite.")
            contributions.append(Fraction(0))
            summary_values.append(Fraction(0))
            continue

        cofactor_label = _label("C", 1, j + 1)
        minor_label = _label("M", 1, j + 1)
        steps.append(f"{indent}Cofactor: {cofactor_label} = (−1)^(1+{j+1}) × det({minor_label})")

        submatriz = _minor(matrix, 0, j)
        steps.append(f"{indent}Submatriz {minor_label} (eliminando fila 1 y columna {j+1}):")
        steps.extend(_matrix_lines(submatriz, indent + "    "))

        sub_det, sub_steps = determinante_con_pasos(submatriz, level + 1)
        steps.extend(sub_steps)
        steps.append(f"{indent}det({minor_label}) = {_fmt(sub_det)}")

        cofactor_value = sign_factor * sub_det
        steps.append(
            f"{indent}{cofactor_label} = {_sign_factor_text(sign_factor)} × {_fmt_factor(sub_det)} = {_fmt(cofactor_value)}"
        )

        contribucion = elemento * cofactor_value
        steps.append(
            f"{indent}Contribución parcial: {_fmt_factor(elemento)} × {_fmt_factor(cofactor_value)} = {_fmt(contribucion)}"
        )
        contributions.append(contribucion)
        summary_values.append(contribucion)

    steps.append(separator)
    total = sum(contributions, Fraction(0))
    partes = " + ".join(_fmt_factor(valor) for valor in summary_values)
    steps.append(f"{indent}Suma total de contribuciones: det(A) = {partes} = {_fmt(total)}")
    return total, steps


class DeterminanteMatrizApp:
    def __init__(self, root, volver_callback):
        self.root = root
        self.volver_callback = volver_callback

        self.root.title("Determinante de Matriz")
        self.root.geometry("1020x740")
        self.root.configure(bg="#ffe4e6")

        style = ttk.Style()
        try:
            style.theme_use("clam")
        except Exception:
            pass
        style.configure("TLabel", font=("Segoe UI", 12), background="#ffe4e6", foreground="#b91c1c")
        style.configure("Primary.TButton", font=("Segoe UI", 12, "bold"), padding=8,
                        background="#fbb6ce", foreground="white")
        style.map("Primary.TButton",
                  background=[("!disabled", "#fbb6ce"), ("active", "#f472b6")],
                  foreground=[("!disabled", "white"), ("active", "white")])
        style.configure("Back.TButton", font=("Segoe UI", 11, "bold"), padding=6,
                        background="#fecaca", foreground="#b91c1c")
        style.map("Back.TButton",
                  background=[("!disabled", "#fecaca"), ("active", "#fca5a5")],
                  foreground=[("!disabled", "#b91c1c"), ("active", "#7f1d1d")])

        self.n_var = tk.StringVar(value="3")
        self.entries: List[List[tk.Entry]] = []

        container = ttk.Frame(self.root, padding=16)
        container.pack(fill="both", expand=True)
        container.columnconfigure(0, weight=1)
        container.rowconfigure(3, weight=1)

        header = ttk.Label(container, text="Determinante de una Matriz Cuadrada",
                           font=("Segoe UI", 22, "bold"))
        header.grid(row=0, column=0, pady=(0, 16))

        config_frame = ttk.LabelFrame(container, text="Configuración", padding=12)
        config_frame.grid(row=1, column=0, sticky="ew", pady=(0, 16))
        config_frame.columnconfigure(2, weight=1)

        ttk.Label(config_frame, text="Orden (n×n):").grid(row=0, column=0, padx=6, pady=6, sticky="w")
        self.spin_n = tk.Spinbox(config_frame, from_=1, to=8, width=5, justify="center",
                                 textvariable=self.n_var, font=("Segoe UI", 12), bg="#fff0f5")
        self.spin_n.grid(row=0, column=1, padx=6, pady=6, sticky="w")
        ttk.Button(config_frame, text="Generar cuadrícula", style="Primary.TButton",
                   command=self._generar_cuadricula).grid(row=0, column=2, padx=6, pady=6, sticky="w")

        self.matriz_frame = ttk.LabelFrame(container, text="Matriz A", padding=12)
        self.matriz_frame.grid(row=2, column=0, sticky="ew")

        acciones = ttk.Frame(container)
        acciones.grid(row=3, column=0, sticky="ew", pady=(16, 10))
        acciones.columnconfigure(0, weight=1)

        botones = ttk.Frame(acciones)
        botones.grid(row=0, column=0, sticky="w")
        ttk.Button(botones, text="Calcular determinante", style="Primary.TButton",
                   command=self._calcular).grid(row=0, column=0, padx=6, pady=4)
        ttk.Button(botones, text="Limpiar entradas", command=self._limpiar).grid(row=0, column=1, padx=6, pady=4)
        ttk.Button(botones, text="Volver al inicio", style="Back.TButton",
                   command=self._volver_al_inicio).grid(row=0, column=2, padx=6, pady=4)

        self.error_label = ttk.Label(acciones, text="", foreground="#b91c1c")
        self.error_label.grid(row=1, column=0, sticky="w", padx=6, pady=(4, 0))

        resultado_frame = ttk.LabelFrame(container, text="Procedimiento paso a paso", padding=12)
        resultado_frame.grid(row=4, column=0, sticky="nsew")
        resultado_frame.columnconfigure(0, weight=1)
        resultado_frame.rowconfigure(1, weight=1)

        self.resumen_label = ttk.Label(resultado_frame, text="Determinante pendiente de cálculo",
                                       font=("Segoe UI", 14, "bold"), foreground="#7f1d1d")
        self.resumen_label.grid(row=0, column=0, sticky="w", pady=(0, 10))

        self.matriz_preview = ttk.Frame(resultado_frame)
        self.matriz_preview.grid(row=1, column=0, sticky="nsew", pady=(0, 12))
        self.matriz_preview.columnconfigure(0, weight=1)

        pasos_container = ttk.Frame(resultado_frame)
        pasos_container.grid(row=2, column=0, sticky="nsew")
        pasos_container.columnconfigure(0, weight=1)
        pasos_container.rowconfigure(0, weight=1)

        scrollbar = ttk.Scrollbar(pasos_container, orient="vertical")
        scrollbar.grid(row=0, column=1, sticky="ns")

        self.pasos_text = tk.Text(pasos_container, wrap="word", height=16, width=90,
                                  bg="#fff0f5", font=("Segoe UI", 11))
        self.pasos_text.grid(row=0, column=0, sticky="nsew")
        self.pasos_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.pasos_text.yview)
        self.pasos_text.config(state="disabled")

        self._generar_cuadricula()

    def _generar_cuadricula(self):
        for widget in self.matriz_frame.winfo_children():
            widget.destroy()
        self.entries.clear()

        try:
            n = int(self.n_var.get())
            if n <= 0:
                raise ValueError
        except Exception:
            messagebox.showerror("Valor inválido", "Introduce un entero positivo para n.")
            return

        grid_frame = ttk.Frame(self.matriz_frame)
        grid_frame.pack()
        for i in range(n):
            fila_entries: List[tk.Entry] = []
            for j in range(n):
                entry = tk.Entry(grid_frame, width=8, justify="center", font=("Segoe UI", 12), bg="#fff0f5")
                entry.grid(row=i, column=j, padx=4, pady=4)
                fila_entries.append(entry)
            self.entries.append(fila_entries)

    def _leer_matriz(self) -> List[List[Fraction]]:
        matriz: List[List[Fraction]] = []
        for fila_entries in self.entries:
            fila: List[Fraction] = []
            for entry in fila_entries:
                valor = entry.get().strip()
                if valor == "":
                    raise ValueError("Hay casillas vacías en la matriz.")
                valor = valor.replace(",", ".")
                fila.append(Fraction(valor))
            matriz.append(fila)
        return matriz

    def _calcular(self):
        self.error_label.config(text="")
        self.pasos_text.config(state="normal")
        self.pasos_text.delete("1.0", "end")
        self.pasos_text.config(state="disabled")
        for widget in self.matriz_preview.winfo_children():
            widget.destroy()
        self.resumen_label.config(text="Determinante pendiente de cálculo")

        try:
            matriz = self._leer_matriz()
        except Exception as exc:
            self.error_label.config(text=f"Error: {exc}")
            return

        filas = len(matriz)
        if filas == 0:
            self.error_label.config(text="Genera la matriz primero.")
            return
        columnas = len(matriz[0])
        if filas != columnas:
            messagebox.showwarning("Matriz no cuadrada", "Solo se pueden calcular determinantes de matrices cuadradas.")
            return

        det, pasos = determinante_con_pasos(matriz)
        self.resumen_label.config(text=f"det(A) = {_fmt(det)}")

        self._mostrar_matriz_preview(matriz)
        self._mostrar_pasos(pasos)

    def _mostrar_matriz_preview(self, matriz: List[List[Fraction]]):
        grid = ttk.LabelFrame(self.matriz_preview, text="Matriz ingresada", padding=8)
        grid.grid(row=0, column=0, sticky="w")
        for i, fila in enumerate(matriz):
            for j, valor in enumerate(fila):
                label = tk.Label(
                    grid,
                    text=_fmt(valor),
                    width=8,
                    font=("Segoe UI", 12),
                    bg="#fff0f5",
                    relief="solid",
                )
                label.grid(row=i, column=j, padx=4, pady=4)

    def _mostrar_pasos(self, pasos: List[str]):
        self.pasos_text.config(state="normal")
        for linea in pasos:
            self.pasos_text.insert("end", linea + "\n")
        self.pasos_text.config(state="disabled")
        self.pasos_text.see("end")

    def _limpiar(self):
        for fila_entries in self.entries:
            for entry in fila_entries:
                entry.delete(0, "end")
        self.error_label.config(text="")
        self.resumen_label.config(text="Determinante pendiente de cálculo")
        self.pasos_text.config(state="normal")
        self.pasos_text.delete("1.0", "end")
        self.pasos_text.config(state="disabled")
        for widget in self.matriz_preview.winfo_children():
            widget.destroy()

    def _volver_al_inicio(self):
        try:
            self.root.destroy()
        finally:
            try:
                if callable(self.volver_callback):
                    self.volver_callback()
            except Exception:
                pass
