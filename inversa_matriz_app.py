import tkinter as tk
from tkinter import ttk, messagebox
from fractions import Fraction


def _fmt(x: Fraction) -> str:
    try:
        return str(x)
    except Exception:
        return f"{x}"


class InversaMatrizApp:
    def __init__(self, root, volver_callback):
        self.root = root
        self.volver_callback = volver_callback

        # ventana
        self.root.title("Inversa de Matriz")
        self.root.geometry("1000x720")
        self.root.configure(bg="#ffe4e6")
        self.root.resizable(True, True)

        # estilos
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

        self.bg = "#ffe4e6"
        self.entry_bg = "#fff0f5"

        # contenedor principal
        container = tk.Frame(self.root, bg=self.bg)
        container.pack(fill="both", expand=True, padx=16, pady=12)

        # encabezado
        tk.Label(container, text="Inversa de Matriz", font=("Segoe UI", 26, "bold"),
                 bg=self.bg, fg="#b91c1c").pack(pady=(10, 6))

        # configuración
        cfg = tk.Frame(container, bg=self.bg)
        cfg.pack(pady=6)
        tk.Label(cfg, text="Tamaño (n x n):", bg=self.bg).grid(row=0, column=0, padx=6, pady=6, sticky="e")
        self.var_n = tk.StringVar(value="3")
        tk.Spinbox(cfg, from_=1, to=12, increment=1, width=6,
                   textvariable=self.var_n, justify="center", bg=self.entry_bg).grid(row=0, column=1, padx=6, pady=6)

        ttk.Button(cfg, text="Crear matriz", style="Primary.TButton", command=self._crear_cuadricula)\
            .grid(row=0, column=2, padx=12, pady=6)

        # ingreso matriz
        self.ingreso_frame = tk.Frame(container, bg=self.bg)
        self.ingreso_frame.pack(pady=(8, 6))
        self.entries_grid = None
        self.n = 0

        # acciones
        actions = tk.Frame(container, bg=self.bg)
        actions.pack(pady=(4, 8), fill="x")

        # selección de método
        self.metodo = tk.StringVar(value="adj")  # adj (n<=3) o gj
        ttk.Label(actions, text="Método:", background=self.bg).pack(side="left", padx=(0,4))
        ttk.Radiobutton(actions, text="Adjunta (n≤3)", variable=self.metodo, value="adj").pack(side="left", padx=4)
        ttk.Radiobutton(actions, text="Gauss-Jordan", variable=self.metodo, value="gj").pack(side="left", padx=4)

        self.var_animar = tk.BooleanVar(value=False)
        ttk.Checkbutton(actions, text="Animar paso a paso", variable=self.var_animar).pack(side="left", padx=12)

        self.btn_calcular = ttk.Button(actions, text="Calcular inversa", style="Primary.TButton",
                                       command=self._calcular_inversa)
        self.btn_calcular.pack(side="left", padx=8)
        self.btn_calcular.state(["disabled"])  # hasta crear la grilla

        ttk.Button(actions, text="Volver al inicio", style="Back.TButton", command=self._volver_al_inicio)\
            .pack(side="right", padx=8)

        # resultados
        self.result_frame = tk.Frame(container, bg=self.bg)
        self.result_frame.pack(fill="both", expand=True, pady=(6, 6))

    # helpers UI simples
    def _clear_result(self):
        for w in self.result_frame.winfo_children():
            w.destroy()

    def _render_matrix(self, parent, M):
        grid = tk.Frame(parent, bg=self.bg)
        grid.pack(pady=4)
        for i, fila in enumerate(M):
            for j, val in enumerate(fila):
                tk.Label(
                    grid, text=_fmt(val), bg=self.bg, fg="#111",
                    font=("Segoe UI", 11), relief="groove", width=10, anchor="center"
                ).grid(row=i, column=j, padx=4, pady=4, sticky="nsew")
        return grid

    # utilidades
    def _parse_fraction(self, s: str) -> Fraction:
        s = (s or "").strip()
        if s == "":
            return Fraction(0)
        s = s.replace(",", ".")
        return Fraction(s)

    def _crear_cuadricula(self):
        for w in self.ingreso_frame.winfo_children():
            w.destroy()
        self._clear_result()

        try:
            n = int(self.var_n.get())
            if n <= 0:
                raise ValueError
            if n > 12:
                messagebox.showwarning("Aviso", "Tamao grande puede ser difcil de visualizar (mx 12).")
        except Exception:
            messagebox.showerror("Error", "Ingrese n valido (entero positivo).")
            return

        self.n = n
        grid = tk.Frame(self.ingreso_frame, bg=self.bg)
        grid.pack()
        self.entries_grid = []
        for i in range(n):
            row_entries = []
            for j in range(n):
                e = tk.Entry(grid, width=8, justify="center", font=("Segoe UI", 11), bg=self.entry_bg)
                e.grid(row=i, column=j, padx=6, pady=6)
                row_entries.append(e)
            self.entries_grid.append(row_entries)

        try:
            self.btn_calcular.state(["!disabled"])
        except Exception:
            pass

    def _leer_matriz(self):
        if not self.entries_grid:
            raise ValueError("Primero cree la matriz.")
        n = self.n
        A = []
        for i in range(n):
            fila = []
            for j in range(n):
                txt = self.entries_grid[i][j].get()
                fila.append(self._parse_fraction(txt))
            A.append(fila)
        return A

    # UI helpers para mostrar [A|I]
    def _build_augmented_view(self, n):
        wrapper = tk.Frame(self.result_frame, bg=self.bg)
        wrapper.pack(pady=6)

        left_col = tk.Frame(wrapper, bg=self.bg)
        left_col.pack(side="left", padx=(0, 10))
        right_col = tk.Frame(wrapper, bg=self.bg)
        right_col.pack(side="left", padx=(10, 0))

        tk.Label(left_col, text="A (trabajo)", font=("Segoe UI", 14, "bold"), bg=self.bg, fg="#b91c1c").pack()
        tk.Label(right_col, text="I / Inversa", font=("Segoe UI", 14, "bold"), bg=self.bg, fg="#b91c1c").pack()

        self.grid_A = tk.Frame(left_col, bg=self.bg)
        self.grid_A.pack(pady=6)
        self.grid_I = tk.Frame(right_col, bg=self.bg)
        self.grid_I.pack(pady=6)

        self.lbl_A = []
        self.lbl_I = []
        for i in range(n):
            ra = []
            ri = []
            for j in range(n):
                la = tk.Label(self.grid_A, text="", bg=self.bg, fg="#111", font=("Segoe UI", 11),
                              relief="groove", width=10, anchor="center")
                la.grid(row=i, column=j, padx=4, pady=4, sticky="nsew")
                li = tk.Label(self.grid_I, text="", bg=self.bg, fg="#111", font=("Segoe UI", 11),
                              relief="groove", width=10, anchor="center")
                li.grid(row=i, column=j, padx=4, pady=4, sticky="nsew")
                ra.append(la)
                ri.append(li)
            self.lbl_A.append(ra)
            self.lbl_I.append(ri)

        # área de pasos
        pasos_title = tk.Label(self.result_frame, text="Pasos detallados", font=("Segoe UI", 14, "bold"),
                               bg=self.bg, fg="#b91c1c")
        pasos_title.pack(pady=(10, 4))
        pasos_frame = tk.Frame(self.result_frame, bg=self.bg)
        pasos_frame.pack(fill="both", expand=True)
        scrollbar = ttk.Scrollbar(pasos_frame)
        scrollbar.pack(side="right", fill="y")
        self.pasos_text = tk.Text(pasos_frame, height=10, yscrollcommand=scrollbar.set, bg="white")
        self.pasos_text.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.pasos_text.yview)

    def _render_augmented(self, A, I):
        n = self.n
        for i in range(n):
            for j in range(n):
                self.lbl_A[i][j].config(text=_fmt(A[i][j]))
                self.lbl_I[i][j].config(text=_fmt(I[i][j]))

    def _calcular_inversa(self):
        for w in self.result_frame.winfo_children():
            w.destroy()
        try:
            A = self._leer_matriz()
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return
        n = self.n

        metodo = self.metodo.get()
        if metodo == "adj" and n <= 3:
            self._calcular_inversa_adjunta(A)
        else:
            # identidad
            I = [[Fraction(1 if i == j else 0) for j in range(n)] for i in range(n)]

            self._build_augmented_view(n)
            self._render_augmented(A, I)

            if self.var_animar.get():
                self._start_animation(A, I)
            else:
                ok, pasos = self._gauss_jordan_steps(A, I, collect_only=True)
                if not ok:
                    messagebox.showerror("Sin inversa", "La matriz no es invertible (determinante 0).")
                    return
                # ejecutar todos los pasos sin animar
                A2 = [row[:] for row in A]
                I2 = [row[:] for row in I]
                self._apply_steps(A2, I2, pasos, log_to_text=True)
                self._render_augmented(A2, I2)

    # --------- Método de la adjunta (n<=3) con pasos detallados ----------
    def _calcular_inversa_adjunta(self, A):
        n = self.n

        # layout superior con dos columnas (como en la imagen)
        top = tk.Frame(self.result_frame, bg=self.bg)
        top.pack(fill="x", pady=(4, 8))
        left = tk.Frame(top, bg=self.bg)
        left.pack(side="left", expand=True, padx=(0, 10))
        right = tk.Frame(top, bg=self.bg)
        right.pack(side="left", expand=True, padx=(10, 0))

        # columna izquierda: A y A^t
        tk.Label(left, text="A =", font=("Segoe UI", 16, "bold"), bg=self.bg, fg="#b91c1c").pack()
        self._render_matrix(left, A)

        At = [list(row) for row in zip(*A)]
        tk.Label(left, text="A^t =", font=("Segoe UI", 16, "bold"), bg=self.bg, fg="#b91c1c").pack(pady=(12, 0))
        self._render_matrix(left, At)

        # columna derecha: |A| paso a paso y Adj(A^t)
        tk.Label(right, text="|A|", font=("Segoe UI", 16, "bold"), bg=self.bg, fg="#b91c1c").pack()
        pasos_frame = tk.Frame(right, bg=self.bg)
        pasos_frame.pack(fill="both", expand=True)
        scrollbar = ttk.Scrollbar(pasos_frame)
        scrollbar.pack(side="right", fill="y")
        pasos_text = tk.Text(pasos_frame, height=10, yscrollcommand=scrollbar.set, bg="white")
        pasos_text.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=pasos_text.yview)

        pasos_text.insert("end", "1) Cálculo del determinante\n")
        if n == 1:
            det = A[0][0]
            pasos_text.insert("end", f"|A| = {det}\n")
        elif n == 2:
            a,b = A[0]
            c,d = A[1]
            det = a*d - b*c
            pasos_text.insert("end", f"|A| = a11·a22 - a12·a21\n")
            pasos_text.insert("end", f"= ({a})·({d}) - ({b})·({c})\n")
            pasos_text.insert("end", f"= {det}\n")
        elif n == 3:
            a11,a12,a13 = A[0]
            a21,a22,a23 = A[1]
            a31,a32,a33 = A[2]
            s1 = a11*a22*a33
            s2 = a12*a23*a31
            s3 = a13*a21*a32
            t1 = a13*a22*a31
            t2 = a11*a23*a32
            t3 = a12*a21*a33
            pasos_text.insert("end", f"Sarrus (diag. principales): {a11}·{a22}·{a33} + {a12}·{a23}·{a31} + {a13}·{a21}·{a32}\n")
            pasos_text.insert("end", f"= {s1} + {s2} + {s3}\n")
            pasos_text.insert("end", f"Sarrus (diag. secundarias): {a13}·{a22}·{a31} + {a11}·{a23}·{a32} + {a12}·{a21}·{a33}\n")
            pasos_text.insert("end", f"= {t1} + {t2} + {t3}\n")
            det = s1 + s2 + s3 - (t1 + t2 + t3)
            pasos_text.insert("end", f"|A| = (suma principales) - (suma secundarias) = {det}\n")
        else:
            messagebox.showerror("Método adjunta", "Solo disponible para n ≤ 3.")
            return

        if det == 0:
            messagebox.showerror("Sin inversa", "La matriz no es invertible (determinante 0).")
            return

        tk.Label(right, text="Adj(A^t) =", font=("Segoe UI", 16, "bold"), bg=self.bg, fg="#b91c1c").pack(pady=(10, 0))
        pasos_text.insert("end", "\n2) Matriz de cofactores (sobre A^t)\n")

        def sign(i,j):
            return Fraction(1) if (i+j)%2==0 else Fraction(-1)

        if n == 1:
            C = [[Fraction(1)]]
            pasos_text.insert("end", "C[1,1] = (+)·det([]) = 1\n")
        elif n == 2:
            # cofactores de A^t equivalen a cofactores de A, solo que intercambia posiciones
            a,b = At[0]
            c,d = At[1]
            # menores de 1x1 (el valor restante)
            m11, m12, m21, m22 = d, c, b, a
            c11 = sign(0,0)*m11
            c12 = sign(0,1)*m12
            c21 = sign(1,0)*m21
            c22 = sign(1,1)*m22
            pasos_text.insert("end", f"C[1,1] = (+)·{m11} = {c11}\n")
            pasos_text.insert("end", f"C[1,2] = (-)·{m12} = {c12}\n")
            pasos_text.insert("end", f"C[2,1] = (-)·{m21} = {c21}\n")
            pasos_text.insert("end", f"C[2,2] = (+)·{m22} = {c22}\n")
            C = [[c11, c12], [c21, c22]]
        else:  # n == 3
            C = [[Fraction(0) for _ in range(3)] for _ in range(3)]
            for i in range(3):
                for j in range(3):
                    rows = [r for r in range(3) if r != i]
                    cols = [c for c in range(3) if c != j]
                    m = [
                        [At[rows[0]][cols[0]], At[rows[0]][cols[1]]],
                        [At[rows[1]][cols[0]], At[rows[1]][cols[1]]],
                    ]
                    mdet = m[0][0]*m[1][1] - m[0][1]*m[1][0]
                    s = sign(i,j)
                    C[i][j] = s*mdet
                    pasos_text.insert(
                        "end",
                        f"M[{i+1},{j+1}] = det([[{m[0][0]}, {m[0][1]}],[{m[1][0]}, {m[1][1]}]]) = {mdet}; "
                        f"C[{i+1},{j+1}] = ({'+' if s>0 else '-'})·{mdet} = {C[i][j]}\n",
                    )

        # Adj(A^t) = C^T donde C son cofactores de A^t
        Adj_At = [list(row) for row in zip(*C)]
        adj_frame = tk.Frame(right, bg=self.bg)
        adj_frame.pack()
        self._render_matrix(adj_frame, Adj_At)

        # sección final: A^{-1} = (1/|A|)·Adj(A^t)
        bottom = tk.Frame(self.result_frame, bg=self.bg)
        bottom.pack(fill="x", pady=(10, 4))
        tk.Label(bottom, text="A^{-1} = (1/|A|)·Adj(A^t)", font=("Segoe UI", 14, "bold"), bg=self.bg, fg="#b91c1c").pack()

        inv = [[Adj_At[i][j] / det for j in range(n)] for i in range(n)]
        self._render_matrix(self.result_frame, inv)
        pasos_text.insert("end", f"\nAdj(A^t) = C^T\n")
        pasos_text.insert("end", f"A^{-1} = (1/{det})·Adj(A^t)\n")

    # Construye la lista de pasos (descriptores) para Gauss-Jordan
    def _gauss_jordan_steps(self, A, I, collect_only=False):
        n = self.n
        pasos = []

        def find_pivot_row(k):
            best = None
            best_abs = Fraction(0)
            for r in range(k, n):
                val = A[r][k]
                if val != 0 and abs(val) >= best_abs:
                    best = r
                    best_abs = abs(val)
            return best

        # Usamos descriptores de pasos genéricos; los valores exactos (pivote/factor)
        # se calculan al aplicar el paso, para que funcionen con animación.
        for k in range(n):
            pasos.append(("pivot", k))
            pasos.append(("scale", k))
            for i in range(n):
                if i != k:
                    pasos.append(("elim", i, k))

        if collect_only:
            # Validación mínima: intentamos simular para detectar singularidad
            Atest = [row[:] for row in A]
            Itest = [row[:] for row in I]
            ok = self._apply_steps(Atest, Itest, pasos, log_to_text=False, simulate=True)
            return ok, pasos
        return True, pasos

    def _apply_steps(self, A, I, pasos, log_to_text=True, simulate=False):
        n = self.n
        for step in pasos:
            if step[0] == "pivot":
                _, k = step
                # seleccionar mejor pivote y/o intercambiar
                p = None
                best_abs = Fraction(0)
                for r in range(k, n):
                    v = A[r][k]
                    if v != 0 and abs(v) >= best_abs:
                        best_abs = abs(v)
                        p = r
                if p is None or A[p][k] == 0:
                    # singular
                    return False
                if p != k:
                    A[k], A[p] = A[p], A[k]
                    I[k], I[p] = I[p], I[k]
                    if log_to_text:
                        self.pasos_text.insert("end", f"Intercambiar R{k+1}  R{p+1}\n")
                else:
                    if log_to_text:
                        self.pasos_text.insert("end", f"Pivote en R{k+1} ya adecuado\n")
            elif step[0] == "scale":
                _, k = step
                a = A[k][k]
                if a == 0:
                    return False
                if a != 1:
                    for j in range(n):
                        A[k][j] /= a
                        I[k][j] /= a
                    if log_to_text:
                        self.pasos_text.insert("end", f"R{k+1} := R{k+1} / {a}\n")
                else:
                    if log_to_text:
                        self.pasos_text.insert("end", f"Pivote R{k+1} ya es 1\n")
            elif step[0] == "elim":
                _, i, k = step
                if i == k:
                    continue
                f = A[i][k]
                if f != 0:
                    for j in range(n):
                        A[i][j] -= f * A[k][j]
                        I[i][j] -= f * I[k][j]
                    if log_to_text:
                        self.pasos_text.insert("end", f"R{i+1} := R{i+1} - ({_fmt(f)})*R{k+1}\n")
                else:
                    if log_to_text:
                        self.pasos_text.insert("end", f"Columna {k+1}: R{i+1} ya tiene 0\n")

            if not simulate:
                self._render_augmented(A, I)
        return True

    # Animación paso a paso
    def _start_animation(self, A, I):
        ok, pasos = self._gauss_jordan_steps(A, I, collect_only=True)
        if not ok:
            messagebox.showerror("Sin inversa", "La matriz no es invertible (determinante 0).")
            return
        # Copias mutables para animación
        self.A_anim = [row[:] for row in A]
        self.I_anim = [row[:] for row in I]
        self.steps = pasos
        self.step_index = 0
        # limpiar pasos
        self.pasos_text.delete("1.0", "end")
        self._render_augmented(self.A_anim, self.I_anim)
        self._animate_next()

    def _animate_next(self):
        if self.step_index >= len(self.steps):
            return
        # aplicar un paso
        step = [self.steps[self.step_index]]
        ok = self._apply_steps(self.A_anim, self.I_anim, step, log_to_text=True, simulate=False)
        if not ok:
            messagebox.showerror("Sin inversa", "La matriz no es invertible (determinante 0).")
            return
        self.step_index += 1
        self.pasos_text.see("end")
        self.root.after(350, self._animate_next)

    def _volver_al_inicio(self):
        try:
            self.root.destroy()
        finally:
            try:
                if callable(self.volver_callback):
                    self.volver_callback()
            except Exception:
                pass
