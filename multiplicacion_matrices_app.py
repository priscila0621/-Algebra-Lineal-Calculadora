import tkinter as tk
from tkinter import ttk, messagebox
from fractions import Fraction
from copy import deepcopy

class MultiplicacionMatricesApp:
  
    def __init__(self, root, volver_callback):
        self.root = root
        self.volver_callback = volver_callback

        # ventana
        self.root.title("Multiplicación de Matrices")
        self.root.geometry("1000x700")
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

        # colores
        self.bg = "#ffe4e6"
        self.entry_bg = "#fff0f5"

        # contenedores
        self.container = tk.Frame(self.root, bg=self.bg)
        self.container.pack(fill="both", expand=True, padx=16, pady=12)

        self.frames = {}
        for name in ("bienvenida", "config", "ingreso", "resultados"):
            f = tk.Frame(self.container, bg=self.bg)
            self.frames[name] = f

        # datos
        self.num_matrices = 0
        self.dimensiones = []
        self.matrices = []
        self.current_index = 0
        self.entries_grid = None

        # crear pantallas
        self._crear_bienvenida()
        self._crear_configuracion()
        self._crear_ingreso()
        self._crear_resultados()

        # mostrar bienvenida
        self._mostrar_frame("bienvenida")

    # ---------- util ----------
    def _mostrar_frame(self, name):
        for fr in self.frames.values():
            fr.pack_forget()
        self.frames[name].pack(fill="both", expand=True)

    def _parse_fraction(self, s):
        s = s.strip()
        if s == "":
            raise ValueError("Valor vacío")
        s = s.replace(",", ".")
        return Fraction(s)

    # ========================= Bienvenida =========================
    def _crear_bienvenida(self):
        f = self.frames["bienvenida"]
        for w in f.winfo_children():
            w.destroy()

        tk.Label(f, text="Multiplicación de Matrices", font=("Segoe UI", 26, "bold"),
                 bg=self.bg, fg="#b91c1c").pack(pady=(40, 6))

        tk.Label(f, text="Multiplicación de 2 o más matrices (A × B × …) con validación de dimensiones",
                 font=("Segoe UI", 12), bg=self.bg, fg="#7f1d1d").pack(pady=(0, 24))

        ttk.Button(f, text="Comenzar", style="Primary.TButton", command=lambda: self._mostrar_frame("config"))\
            .pack(pady=10, ipadx=12, ipady=6)

        ttk.Button(f, text="Volver al inicio", style="Back.TButton",
                   command=self._volver_al_inicio).pack(side="bottom", pady=20)

    # ========================= Configuración =========================
    def _crear_configuracion(self):
        f = self.frames["config"]
        for w in f.winfo_children():
            w.destroy()

        header = tk.Frame(f, bg=self.bg)
        header.pack(pady=(20, 10), fill="x")
        tk.Label(header, text="Configuración de dimensiones", font=("Segoe UI", 18, "bold"),
                 bg=self.bg, fg="#b91c1c").pack()

        mid = tk.Frame(f, bg=self.bg)
        mid.pack(pady=12)

        tk.Label(mid, text="¿Cuántas matrices deseas multiplicar?", bg=self.bg,
                 font=("Segoe UI", 12)).grid(row=0, column=0, sticky="w", padx=6, pady=6)
        self.input_num = tk.StringVar(value="2")
        tk.Entry(mid, textvariable=self.input_num, width=6, bg=self.entry_bg).grid(row=0, column=1, padx=6, pady=6)

        ttk.Button(mid, text="Generar campos", style="Primary.TButton", command=self._generar_campos_dim)\
            .grid(row=0, column=2, padx=12, pady=6)

        self.frame_dims = tk.Frame(f, bg=self.bg)
        self.frame_dims.pack(pady=12)

        bottom = tk.Frame(f, bg=self.bg)
        bottom.pack(side="bottom", fill="x", pady=14)
        ttk.Button(bottom, text="Volver al inicio", style="Back.TButton", command=self._volver_al_inicio)\
            .pack(side="left", padx=12)
        ttk.Button(bottom, text="Siguiente", style="Primary.TButton", command=self._validar_dimensiones)\
            .pack(side="right", padx=12)

    def _generar_campos_dim(self):
        for w in self.frame_dims.winfo_children():
            w.destroy()

        try:
            n = int(self.input_num.get())
            if n < 2:
                raise ValueError("Debe ser al menos 2")
        except Exception:
            messagebox.showerror("Error", "Ingrese un número entero ≥ 2.")
            return

        self.num_matrices = n
        self.dim_entries = []

        tk.Label(self.frame_dims, text="Ingrese dimensiones:", bg=self.bg, font=("Segoe UI", 12))\
            .pack(anchor="w", pady=(0,6))

        for i in range(n):
            rowf = tk.Frame(self.frame_dims, bg=self.bg)
            rowf.pack(anchor="w", pady=6)
            tk.Label(rowf, text=f"Matriz {i+1}:", bg=self.bg, width=10).pack(side="left", padx=6)
            ef = tk.Entry(rowf, width=6, bg=self.entry_bg)
            ec = tk.Entry(rowf, width=6, bg=self.entry_bg)
            ef.pack(side="left", padx=(0,6))
            tk.Label(rowf, text="x", bg=self.bg).pack(side="left")
            ec.pack(side="left", padx=(6,6))
            self.dim_entries.append((ef, ec))

    def _validar_dimensiones(self):
        try:
            dims = []
            for ef, ec in self.dim_entries:
                f = int(ef.get())
                c = int(ec.get())
                if f <= 0 or c <= 0:
                    raise ValueError
                dims.append((f, c))
            for i in range(len(dims) - 1):
                if dims[i][1] != dims[i+1][0]:
                    messagebox.showerror("Error",
                                         f"Columnas de Matriz {i+1} deben coincidir con filas de Matriz {i+2}.")
                    return
            self.dimensiones = dims
            self.matrices = [None] * self.num_matrices
            self.current_index = 0
            self._mostrar_frame("ingreso")
            self._render_ingreso_actual()
        except Exception:
            messagebox.showerror("Error", "Verifica que las dimensiones sean correctas.")

    # ========================= Ingreso =========================
    def _crear_ingreso(self):
        f = self.frames["ingreso"]
        for w in f.winfo_children():
            w.destroy()

        self.ing_header = tk.Frame(f, bg=self.bg)
        self.ing_header.pack(fill="x", pady=(18,6))
        self.label_ing_title = tk.Label(self.ing_header, text="", font=("Segoe UI", 16, "bold"),
                                        bg=self.bg, fg="#b91c1c")
        self.label_ing_title.pack()

        self.ing_table = tk.Frame(f, bg=self.bg)
        self.ing_table.pack(pady=8)

        self.ing_error = tk.Label(f, text="", fg="red", bg=self.bg)
        self.ing_error.pack()

        btns = tk.Frame(f, bg=self.bg)
        btns.pack(pady=12)
        self.btn_prev = ttk.Button(btns, text="Anterior", style="Back.TButton", command=self._ingresar_anterior)
        self.btn_prev.grid(row=0, column=0, padx=8)
        self.btn_confirm = ttk.Button(btns, text="Confirmar Matriz", style="Primary.TButton", command=self._confirmar_matriz)
        self.btn_confirm.grid(row=0, column=1, padx=8)

        ttk.Button(f, text="Volver al inicio", style="Back.TButton", command=self._volver_al_inicio)\
            .pack(side="bottom", pady=14)

    def _render_ingreso_actual(self):
        for w in self.ing_table.winfo_children():
            w.destroy()
        self.ing_error.config(text="")

        idx = self.current_index
        f, c = self.dimensiones[idx]
        self.label_ing_title.config(text=f"Ingresa los valores de la Matriz {idx+1} ({f}×{c})")

        self.entries_grid = []
        grid = tk.Frame(self.ing_table, bg=self.bg)
        grid.pack()

        for i in range(f):
            row_entries = []
            for j in range(c):
                e = tk.Entry(grid, width=8, justify="center", font=("Segoe UI", 11), bg=self.entry_bg)
                e.grid(row=i, column=j, padx=6, pady=6)
                row_entries.append(e)
            self.entries_grid.append(row_entries)

    def _ingresar_anterior(self):
        if self.current_index > 0:
            self.current_index -= 1
            self._render_ingreso_actual()

    def _confirmar_matriz(self):
        try:
            f, c = self.dimensiones[self.current_index]
            mat = []
            for i in range(f):
                row = []
                for j in range(c):
                    txt = self.entries_grid[i][j].get().strip()
                    if txt == "":
                        txt = "0"
                    val = self._parse_fraction(txt)
                    row.append(val)
                mat.append(row)
            self.matrices[self.current_index] = mat
            if self.current_index + 1 < self.num_matrices:
                self.current_index += 1
                self._render_ingreso_actual()
            else:
                self._calcular_multiplicacion()
        except Exception as e:
            self.ing_error.config(text=f"Error en los datos: {e}")

    # ========================= Resultados =========================
    def _crear_resultados(self):
        f = self.frames["resultados"]
        for w in f.winfo_children():
            w.destroy()
        self.result_container = tk.Frame(f, bg=self.bg)
        self.result_container.pack(fill="both", expand=True, padx=8, pady=8)
        ttk.Button(f, text="Volver al inicio", style="Back.TButton", command=self._volver_al_inicio)\
            .pack(side="bottom", pady=12)

    def _calcular_multiplicacion(self):
        try:
            parcial = deepcopy(self.matrices[0])
            pasos_general = []
            for ix in range(1, len(self.matrices)):
                B = self.matrices[ix]
                A = parcial
                R, pasos = self._multiplicar_con_detalle(A, B)
                pasos_general.extend(pasos)
                parcial = R
            resultado_final = parcial
            self._mostrar_resultados(resultado_final, pasos_general)
            self._mostrar_frame("resultados")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un problema: {e}")

    def _multiplicar_con_detalle(self, A, B):
        fa, ca = len(A), len(A[0])
        fb, cb = len(B), len(B[0])
        R = [[Fraction(0) for _ in range(cb)] for _ in range(fa)]
        pasos = []
        for i in range(fa):
            for j in range(cb):
                terms = []
                s = Fraction(0)
                for k in range(ca):
                    a = A[i][k]
                    b = B[k][j]
                    terms.append(f"{a}×{b}")
                    s += a * b
                R[i][j] = s
                pasos.append(f"c{i+1}{j+1} = " + " + ".join(terms) + f" = {s}")
        return R, pasos

    def _mostrar_resultados(self, resultado_final, pasos_general):
        for w in self.result_container.winfo_children():
            w.destroy()

        # Encabezado
        tk.Label(self.result_container, text="Resultado de la Multiplicación", 
                 font=("Segoe UI", 18, "bold"), bg=self.bg, fg="#b91c1c").pack(pady=(10,10))

        # Mostrar matrices ingresadas
        matsf = tk.Frame(self.result_container, bg=self.bg)
        matsf.pack(pady=6)
        for idx, mat in enumerate(self.matrices, start=1):
            subf = tk.Frame(matsf, bg=self.bg)
            subf.pack(side="left", padx=12)
            tk.Label(subf, text=f"Matriz {idx}", font=("Segoe UI", 12, "bold"), bg=self.bg, fg="#7f1d1d").pack()
            grid = tk.Frame(subf, bg=self.bg)
            grid.pack()
            for i, row in enumerate(mat):
                for j, val in enumerate(row):
                    tk.Label(grid, text=str(val), width=8, bg=self.entry_bg, relief="solid")\
                        .grid(row=i, column=j, padx=4, pady=4)

        # Matriz final
        tk.Label(self.result_container, text="Matriz Resultante:", 
                 font=("Segoe UI", 14, "bold"), bg=self.bg, fg="#b91c1c").pack(pady=(12,6))
        matf = tk.Frame(self.result_container, bg=self.bg)
        matf.pack()
        for i, row in enumerate(resultado_final):
            for j, val in enumerate(row):
                tk.Label(matf, text=str(val), width=10, bg=self.entry_bg, relief="solid")\
                    .grid(row=i, column=j, padx=6, pady=6)

        # Botón toggle para procedimiento
        self.proc_visible = False
        self.proc_frame = tk.Frame(self.result_container, bg=self.bg)
        self.proc_frame.pack(fill="both", expand=True, pady=(8,0))

        def toggle_proc():
            if self.proc_visible:
                for w in self.proc_frame.winfo_children():
                    w.destroy()
                self.proc_visible = False
                btn_toggle.config(text="Mostrar procedimiento")
            else:
                tk.Label(self.proc_frame, text="Procedimiento paso a paso:", 
                         font=("Segoe UI", 13, "bold"), bg=self.bg, fg="#7f1d1d").pack(anchor="w", pady=(6,4))
                for line in pasos_general:
                    tk.Label(self.proc_frame, text=line, font=("Consolas", 12), 
                             bg=self.bg, fg="black", anchor="w", justify="left").pack(anchor="w")
                self.proc_visible = True
                btn_toggle.config(text="Ocultar procedimiento")

        btn_toggle = ttk.Button(self.result_container, text="Mostrar procedimiento", style="Primary.TButton", command=toggle_proc)
        btn_toggle.pack(pady=10)

    # ========================= Volver =========================
    def _volver_al_inicio(self):
        try:
            self.root.destroy()
        except Exception:
            pass
        try:
            if self.volver_callback:
                self.volver_callback()
        except Exception:
            pass