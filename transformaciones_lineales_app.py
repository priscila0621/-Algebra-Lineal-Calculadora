import tkinter as tk
from tkinter import ttk, messagebox
from fractions import Fraction


class TransformacionesLinealesApp:
    """
    Módulo educativo para trabajar con transformaciones lineales T(x) = A x.

    Características principales (en pestañas):
    - Calcular T(x) = A x para una matriz A dada y un vector x.
    - Construir la matriz A a partir de las imágenes de la base canónica {e_j}.
    - Comprobar numéricamente propiedades de linealidad con vectores u, v y escalares c, d.

    Se implementa en un archivo nuevo para no alterar módulos existentes.
    """

    def __init__(self, root, volver_callback):
        self.root = root
        self.volver_callback = volver_callback

        self.root.title("Transformaciones lineales: T(x) = A x")
        self.root.geometry("1100x820")
        self.root.configure(bg="#ffe4e6")

        self._setup_styles()
        self._build_ui()

    # -------------------- utilidades --------------------
    @staticmethod
    def _parse_fraction(s: str) -> Fraction:
        s = (s or "").strip().replace(",", ".")
        if s == "":
            return Fraction(0)
        return Fraction(s)

    @staticmethod
    def _fmt(x: Fraction) -> str:
        return f"{x.numerator}" if x.denominator == 1 else f"{x.numerator}/{x.denominator}"

    @staticmethod
    def _matmul(A, x):
        m = len(A)
        n = len(A[0]) if m else 0
        if len(x) != n:
            raise ValueError("Dimensiones incompatibles entre A y x")
        return [sum(A[i][j] * x[j] for j in range(n)) for i in range(m)]

    # -------------------- estilos y UI --------------------
    def _setup_styles(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except Exception:
            pass
        style.configure("TLabel", font=("Segoe UI", 12), background="#ffe4e6", foreground="#b91c1c")
        style.configure("TEntry", font=("Segoe UI", 12))
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

    def _build_ui(self):
        top = ttk.Frame(self.root, padding=12)
        top.pack(fill="x")
        ttk.Label(top, text="Transformaciones lineales", font=("Segoe UI", 20, "bold")).pack(side="left")
        ttk.Button(top, text="Volver", style="Back.TButton", command=self.volver_callback).pack(side="right")

        nb = ttk.Notebook(self.root)
        nb.pack(fill="both", expand=True, padx=12, pady=8)

        self.tab_ax = ttk.Frame(nb)
        self.tab_base = ttk.Frame(nb)
        self.tab_linealidad = ttk.Frame(nb)
        nb.add(self.tab_ax, text="T(x) = A x")
        nb.add(self.tab_base, text="Matriz desde base")
        nb.add(self.tab_linealidad, text="Comprobar linealidad")

        self._build_tab_ax()
        self._build_tab_base()
        self._build_tab_linealidad()

    # -------------------- TAB 1: T(x) = A x --------------------
    def _build_tab_ax(self):
        f = self.tab_ax
        f.configure(style="TFrame")

        cfg = ttk.Frame(f)
        cfg.pack(pady=8)
        ttk.Label(cfg, text="Filas (m):").grid(row=0, column=0, padx=6, sticky="e")
        ttk.Label(cfg, text="Columnas (n):").grid(row=0, column=2, padx=6, sticky="e")
        self.m_var = tk.IntVar(value=2)
        self.n_var = tk.IntVar(value=2)
        ttk.Spinbox(cfg, from_=1, to=10, textvariable=self.m_var, width=5, justify="center").grid(row=0, column=1)
        ttk.Spinbox(cfg, from_=1, to=10, textvariable=self.n_var, width=5, justify="center").grid(row=0, column=3)
        ttk.Button(cfg, text="Crear A y x", style="Primary.TButton", command=self._crear_Ax).grid(row=0, column=4, padx=10)

        self.frame_Ax = ttk.Frame(f)
        self.frame_Ax.pack(pady=12)

        self.res_ax = tk.Text(f, height=12, font=("Consolas", 11), bg="#fff0f5")
        self.res_ax.pack(fill="both", expand=False, padx=10, pady=6)
        self.res_ax.configure(state="disabled")

        ttk.Button(f, text="Ejemplo de las diapositivas", style="Primary.TButton",
                   command=self._cargar_ejemplo_ax).pack(pady=6)

    def _crear_Ax(self):
        for w in self.frame_Ax.winfo_children():
            w.destroy()
        m, n = self.m_var.get(), self.n_var.get()

        ttk.Label(self.frame_Ax, text="Matriz A (m x n)").grid(row=0, column=0, padx=6, pady=6)
        self.entries_A = []
        gridA = ttk.Frame(self.frame_Ax)
        gridA.grid(row=1, column=0, padx=6)
        for i in range(m):
            fila = []
            for j in range(n):
                e = ttk.Entry(gridA, width=7, justify="center")
                e.grid(row=i, column=j, padx=3, pady=3)
                fila.append(e)
            self.entries_A.append(fila)

        ttk.Label(self.frame_Ax, text="Vector x (n)").grid(row=0, column=1, padx=6, pady=6)
        self.entries_x = []
        gridx = ttk.Frame(self.frame_Ax)
        gridx.grid(row=1, column=1, padx=6)
        for j in range(n):
            e = ttk.Entry(gridx, width=7, justify="center")
            e.grid(row=j, column=0, padx=3, pady=3)
            self.entries_x.append(e)

        ttk.Button(self.frame_Ax, text="Calcular T(x) = A x", style="Primary.TButton",
                   command=self._calcular_ax).grid(row=2, column=0, columnspan=2, pady=10)

    def _leer_A_y_x(self):
        m, n = self.m_var.get(), self.n_var.get()
        A = [[self._parse_fraction(self.entries_A[i][j].get()) for j in range(n)] for i in range(m)]
        x = [self._parse_fraction(self.entries_x[j].get()) for j in range(n)]
        return A, x

    def _calcular_ax(self):
        try:
            A, x = self._leer_A_y_x()
            b = self._matmul(A, x)

            # Representación con corchetes y paso a paso
            mat_lines = self._format_product(A, x, b)
            steps = ["", "Paso a paso:"]
            m, n = len(A), len(A[0]) if A else 0
            for i in range(m):
                mults = [f"({self._fmt(A[i][j])})*({self._fmt(x[j])})" for j in range(n)]
                prods = [A[i][j]*x[j] for j in range(n)]
                sums = " + ".join(self._fmt(p) for p in prods)
                steps.append(f"Fila {i+1}: " + " + ".join(mults) + f" = {sums} = {self._fmt(b[i])}")

            self._write(self.res_ax, "\n".join(mat_lines + steps))
        except Exception as exc:
            messagebox.showerror("Error", f"No se pudo calcular Ax: {exc}")

    def _cargar_ejemplo_ax(self):
        # Ejemplo simple 2x3 con x en R^3 tomado de las ideas de las diapositivas
        self.m_var.set(2)
        self.n_var.set(3)
        self._crear_Ax()
        Aej = [[4, -3, 1], [2, 0, 5]]
        xej = [1, 1, 1]
        for i in range(2):
            for j in range(3):
                self.entries_A[i][j].insert(0, str(Aej[i][j]))
        for j in range(3):
            self.entries_x[j].insert(0, str(xej[j]))

    # ------- formato matricial con corchetes -------
    def _format_product(self, A, x, b=None):
        m = len(A)
        n = len(A[0]) if m else 0
        col_w = [0]*n
        for j in range(n):
            col_w[j] = max(len(self._fmt(A[i][j])) for i in range(m)) if m else 1
        x_w = max((len(self._fmt(x[j])) for j in range(n)), default=1)
        b_w = max((len(self._fmt(b[i])) for i in range(m)), default=1) if b is not None else 1
        lines = []
        rows = max(m, n)
        for i in range(rows):
            if i < m:
                a_row = " ".join(self._fmt(A[i][j]).rjust(col_w[j]) for j in range(n))
                left = "[ " + a_row + " ]"
            else:
                left = "  " + " "*(sum(col_w)+(n-1)) + "  "
            if i < n:
                mid = "[ " + self._fmt(x[i]).rjust(x_w) + " ]"
            else:
                mid = "  " + " "*(x_w+2)
            if b is not None and i < m:
                right = "[ " + self._fmt(b[i]).rjust(b_w) + " ]"
            else:
                right = ""
            eq = " = " if (b is not None and i == 0) else ("   " if b is not None else "")
            if i == 0 and b is not None:
                lines.append(f"{left}   {mid}{eq}{right}")
            else:
                lines.append(f"{left}   {mid}{('   '+right) if right else ''}")
        return lines

    # ------- forma explícita T([x1,..,xn]) -------
    def _format_symbolic_explicit(self, A):
        m = len(A)
        n = len(A[0]) if m else 0
        xnames = [f"x{j+1}" for j in range(n)]
        lines = []
        # Representación como combinación lineal de columnas
        lines.append("")
        lines.append("Representación como combinación lineal de las columnas:")
        lines += self._format_linear_combination(A)
        lines.append("")
        lines.append("Forma explícita (por componentes):")
        fila_expr = []
        for i in range(m):
            terms = []
            for j in range(n):
                a = self._fmt(A[i][j])
                xj = xnames[j]
                if a == "0":
                    continue
                if a == "1":
                    terms.append(xj)
                elif a == "-1":
                    terms.append(f"- {xj}")
                else:
                    if a.startswith("-"):
                        terms.append(f"- {a[1:]}{xj}")
                    else:
                        terms.append(f"{a}{xj}")
            if not terms:
                fila_expr.append("0")
            else:
                expr = terms[0]
                for t in terms[1:]:
                    expr = expr + (" + " + t if not t.strip().startswith("-") else " - " + t.strip()[2:])
                fila_expr.append(expr)
        lines.append("T([" + ", ".join(xnames) + "]^T) = [")
        for expr in fila_expr:
            lines.append("  " + expr)
        lines.append("]^T")
        return lines

    def _format_linear_combination(self, A):
        m = len(A)
        n = len(A[0]) if m else 0
        xnames = [f"x{j+1}" for j in range(n)]

        # Ancho por columna para alinear cada bloque [ a_ij ]
        col_w = [0] * n
        for j in range(n):
            col_w[j] = max(len(self._fmt(A[i][j])) for i in range(m)) if m else 1
        xw = [len(s) for s in xnames]

        # Expresiones del resultado por fila
        fila_expr = []
        for i in range(m):
            terms = []
            for j in range(n):
                a = self._fmt(A[i][j])
                if a == "0":
                    continue
                if a == "1":
                    terms.append(f"x{j+1}")
                elif a == "-1":
                    terms.append(f"-x{j+1}")
                else:
                    terms.append(f"{a}x{j+1}")
            if not terms:
                fila_expr.append("0")
            else:
                expr = terms[0]
                for t in terms[1:]:
                    expr += (" + " + t) if not t.startswith("-") else (" - " + t[1:])
                fila_expr.append(expr)

        # Construir parte izquierda por filas con bloques de ancho fijo
        left_parts = []
        for i in range(m):
            pieces = []
            for j in range(n):
                scalar = xnames[j] if i == 0 else (" " * xw[j])
                val = self._fmt(A[i][j]).rjust(col_w[j])
                pieces.append(f"{scalar} [ {val} ]")
            left_parts.append("  +  ".join(pieces))

        # Alinear columna del resultado [ … ]
        max_left = max(len(s) for s in left_parts) if left_parts else 0
        lines = []
        for i in range(m):
            left = left_parts[i].ljust(max_left)
            if i == 0:
                lines.append(f"= {left} = [ {fila_expr[i]} ]")
            else:
                lines.append(f"  {left}   [ {fila_expr[i]} ]")
        return lines

    # -------------------- TAB 2: matriz desde imágenes de base --------------------
    def _build_tab_base(self):
        f = self.tab_base
        cfg = ttk.Frame(f)
        cfg.pack(pady=8)
        ttk.Label(cfg, text="Dimensiones de T: R^n -> R^m").grid(row=0, column=0, columnspan=4, pady=(0, 6))
        ttk.Label(cfg, text="m (filas)").grid(row=1, column=0)
        ttk.Label(cfg, text="n (columnas)").grid(row=1, column=2)
        self.m2_var = tk.IntVar(value=2)
        self.n2_var = tk.IntVar(value=2)
        ttk.Spinbox(cfg, from_=1, to=10, textvariable=self.m2_var, width=5, justify="center").grid(row=1, column=1)
        ttk.Spinbox(cfg, from_=1, to=10, textvariable=self.n2_var, width=5, justify="center").grid(row=1, column=3)
        ttk.Button(cfg, text="Crear campos T(e_j)", style="Primary.TButton", command=self._crear_base).grid(row=1, column=4, padx=10)

        self.frame_base = ttk.Frame(f)
        self.frame_base.pack(pady=10)

        self.res_base = tk.Text(f, height=14, font=("Consolas", 11), bg="#fff0f5")
        self.res_base.pack(fill="both", expand=False, padx=10, pady=6)
        self.res_base.configure(state="disabled")

    def _crear_base(self):
        for w in self.frame_base.winfo_children():
            w.destroy()
        m, n = self.m2_var.get(), self.n2_var.get()

        ttk.Label(self.frame_base, text="Imágenes de la base canónica (columnas de A)").grid(row=0, column=0, padx=6, pady=6)
        self.entries_Tej = []  # lista de columnas, cada una m entradas
        cols = ttk.Frame(self.frame_base)
        cols.grid(row=1, column=0, padx=6)
        for j in range(n):
            colf = ttk.Frame(cols)
            colf.grid(row=0, column=j, padx=5)
            ttk.Label(colf, text=f"T(e{j+1})").pack()
            col_entries = []
            for i in range(m):
                e = ttk.Entry(colf, width=7, justify="center")
                e.pack(padx=2, pady=2)
                col_entries.append(e)
            self.entries_Tej.append(col_entries)

        ttk.Button(self.frame_base, text="Construir matriz A", style="Primary.TButton", command=self._construir_A_desde_base).grid(row=2, column=0, pady=10)

    def _construir_A_desde_base(self):
        try:
            m, n = self.m2_var.get(), self.n2_var.get()
            # A tiene como columnas los T(ej)
            A = [[self._parse_fraction(self.entries_Tej[j][i].get()) for j in range(n)] for i in range(m)]

            lines = []
            # Paso 1: datos de entrada
            lines.append("Paso 1) Imágenes de la base canónica (por columnas):")
            for j in range(n):
                col = [self._fmt(A[i][j]) for i in range(m)]
                lines.append(f"T(e{j+1}) = [ " + "  ".join(col) + " ]^T")

            # Paso 2: formar A con esas columnas
            lines.append("")
            lines.append("Paso 2) Formar la matriz A colocando T(ej) como columnas:")
            for i in range(m):
                row = "  ".join(self._fmt(A[i][j]) for j in range(n))
                lines.append("A = [ " + row + " ]")

            # Paso 3: interpretación y fórmula
            lines.append("")
            lines.append(f"Interpretación: Sea T: R^{n} → R^{m} definida por T(x) = A x.")
            lines.append("La j-ésima columna de A es T(e_j). Por lo tanto, para x = [x1, …, xn]^T se tiene:")
            lines.append("T(x) = x1·T(e1) + x2·T(e2) + ··· + xn·T(en).")

            # Paso 4: forma explícita por componentes
            lines += self._format_symbolic_explicit(A)

            self._write(self.res_base, "\n".join(lines))
        except Exception as exc:
            messagebox.showerror("Error", f"No se pudo construir A: {exc}")

    # -------------------- TAB 3: comprobar linealidad --------------------
    def _build_tab_linealidad(self):
        f = self.tab_linealidad
        f.configure(style="TFrame")

        info = ttk.Label(f, text=(
            "Verifica numéricamente T(u+v) = T(u) + T(v) y T(cu+dv) = cT(u) + dT(v)\n"
            "para T(x)=Ax, ingresando A, u, v y escalares c, d."))
        info.pack(pady=8)

        cfg = ttk.Frame(f)
        cfg.pack(pady=6)
        ttk.Label(cfg, text="m filas").grid(row=0, column=0)
        ttk.Label(cfg, text="n cols").grid(row=0, column=2)
        self.m3_var = tk.IntVar(value=2)
        self.n3_var = tk.IntVar(value=2)
        ttk.Spinbox(cfg, from_=1, to=10, textvariable=self.m3_var, width=5, justify="center").grid(row=0, column=1)
        ttk.Spinbox(cfg, from_=1, to=10, textvariable=self.n3_var, width=5, justify="center").grid(row=0, column=3)
        ttk.Button(cfg, text="Crear campos", style="Primary.TButton", command=self._crear_linealidad).grid(row=0, column=4, padx=10)

        self.frame_lin = ttk.Frame(f)
        self.frame_lin.pack(pady=8)

        self.res_lin = tk.Text(f, height=16, font=("Consolas", 11), bg="#fff0f5")
        self.res_lin.pack(fill="both", expand=False, padx=10, pady=6)
        self.res_lin.configure(state="disabled")

    def _crear_linealidad(self):
        for w in self.frame_lin.winfo_children():
            w.destroy()
        m, n = self.m3_var.get(), self.n3_var.get()

        # Matriz A
        ttk.Label(self.frame_lin, text="Matriz A (m x n)").grid(row=0, column=0)
        self.entries_A3 = []
        gridA = ttk.Frame(self.frame_lin); gridA.grid(row=1, column=0, padx=6)
        for i in range(m):
            fila = []
            for j in range(n):
                e = ttk.Entry(gridA, width=7, justify="center")
                e.grid(row=i, column=j, padx=3, pady=3)
                fila.append(e)
            self.entries_A3.append(fila)

        # u, v
        ttk.Label(self.frame_lin, text="Vector u").grid(row=0, column=1)
        self.entries_u = []
        gridu = ttk.Frame(self.frame_lin); gridu.grid(row=1, column=1, padx=6)
        for j in range(n):
            e = ttk.Entry(gridu, width=7, justify="center")
            e.grid(row=j, column=0, padx=3, pady=3)
            self.entries_u.append(e)
        ttk.Label(self.frame_lin, text="Vector v").grid(row=0, column=2)
        self.entries_v = []
        gridv = ttk.Frame(self.frame_lin); gridv.grid(row=1, column=2, padx=6)
        for j in range(n):
            e = ttk.Entry(gridv, width=7, justify="center")
            e.grid(row=j, column=0, padx=3, pady=3)
            self.entries_v.append(e)

        # escalares c, d
        escalares = ttk.Frame(self.frame_lin); escalares.grid(row=2, column=0, columnspan=3, pady=8)
        ttk.Label(escalares, text="c =").pack(side="left")
        self.c_var = tk.StringVar(value="1")
        ttk.Entry(escalares, width=7, textvariable=self.c_var, justify="center").pack(side="left", padx=6)
        ttk.Label(escalares, text="d =").pack(side="left")
        self.d_var = tk.StringVar(value="1")
        ttk.Entry(escalares, width=7, textvariable=self.d_var, justify="center").pack(side="left", padx=6)

        ttk.Button(self.frame_lin, text="Comprobar", style="Primary.TButton", command=self._comprobar_linealidad).grid(row=3, column=0, columnspan=3, pady=10)

    def _leer_A3_u_v(self):
        m, n = self.m3_var.get(), self.n3_var.get()
        A = [[self._parse_fraction(self.entries_A3[i][j].get()) for j in range(n)] for i in range(m)]
        u = [self._parse_fraction(e.get()) for e in self.entries_u]
        v = [self._parse_fraction(e.get()) for e in self.entries_v]
        c = self._parse_fraction(self.c_var.get())
        d = self._parse_fraction(self.d_var.get())
        return A, u, v, c, d

    def _comprobar_linealidad(self):
        try:
            A, u, v, c, d = self._leer_A3_u_v()
            # T(x) = A x
            cu_dv = [c * ui + d * vi for ui, vi in zip(u, v)]
            Tu = self._matmul(A, u)
            Tv = self._matmul(A, v)
            T_cu_dv = self._matmul(A, cu_dv)
            cTu_dTv = [c * Tu[i] + d * Tv[i] for i in range(len(Tu))]

            eq = all(T_cu_dv[i] == cTu_dTv[i] for i in range(len(Tu)))
            lines = ["Comprobación de linealidad:"]
            lines.append("T(cu + dv) vs cT(u) + dT(v)")
            lines.append("Iguales: SI" if eq else "Iguales: NO")
            lines.append("")
            lines.append("T(u) = [" + ", ".join(self._fmt(x) for x in Tu) + "]")
            lines.append("T(v) = [" + ", ".join(self._fmt(x) for x in Tv) + "]")
            lines.append("T(cu+dv) = [" + ", ".join(self._fmt(x) for x in T_cu_dv) + "]")
            lines.append("cT(u)+dT(v) = [" + ", ".join(self._fmt(x) for x in cTu_dTv) + "]")
            self._write(self.res_lin, "\n".join(lines))
        except Exception as exc:
            messagebox.showerror("Error", f"No se pudo comprobar la linealidad: {exc}")

    # -------------------- helpers --------------------
    def _write(self, widget: tk.Text, text: str):
        widget.configure(state="normal")
        widget.delete("1.0", tk.END)
        widget.insert("1.0", text)
        widget.configure(state="disabled")


# Modo directo (para pruebas manuales)
if __name__ == "__main__":
    import tkinter as tk
    root = tk.Tk()
    def _volver():
        root.destroy()
    TransformacionesLinealesApp(root, _volver)
    root.mainloop()
