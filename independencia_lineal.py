# independencia_lineal.py

import tkinter as tk
from tkinter import ttk, messagebox

def es_vector_cero(v):
    return all(x == 0 for x in v)

def son_multiplos(v1, v2):
    ratio = None
    for a, b in zip(v1, v2):
        if b == 0 and a == 0:
            continue
        elif b == 0 or a == 0:
            return False
        else:
            r = a / b
            if ratio is None:
                ratio = r
            elif abs(r - ratio) > 1e-10:
                return False
    return ratio is not None

def determinante_3x3(m):
    a, b, c = m[0][0], m[1][0], m[2][0]
    d, e, f = m[0][1], m[1][1], m[2][1]
    g, h, i = m[0][2], m[1][2], m[2][2]
    return a*(e*i - f*h) - d*(b*i - c*h) + g*(b*f - c*e)

def gauss_jordan_homogeneo(matriz):
    n = len(matriz[0])
    m = len(matriz)
    A = [list(col) for col in zip(*matriz)]
    for fila in A:
        fila.append(0)
    filas = len(A)
    columnas = len(A[0])
    pivote = 0
    for col in range(columnas-1):
        fila_pivote = None
        for f in range(pivote, filas):
            if abs(A[f][col]) > 1e-10:
                fila_pivote = f
                break
        if fila_pivote is None:
            continue
        A[pivote], A[fila_pivote] = A[fila_pivote], A[pivote]
        factor = A[pivote][col]
        A[pivote] = [x / factor for x in A[pivote]]
        for f in range(filas):
            if f != pivote and abs(A[f][col]) > 1e-10:
                factor = A[f][col]
                A[f] = [a - factor * b for a, b in zip(A[f], A[pivote])]
        pivote += 1
    rang = 0
    for fila in A:
        if any(abs(x) > 1e-10 for x in fila[:-1]):
            rang += 1
    if rang < n:
        return False
    return True

def gauss_jordan_homogeneo_con_relacion(matriz):
    n = len(matriz[0])
    m = len(matriz)
    # Creamos la matriz aumentada (matriz | 0)
    A = [list(col) for col in zip(*matriz)]
    for fila in A:
        fila.append(0)
    filas = len(A)
    columnas = len(A[0])
    pivote = 0
    pos_pivotes = [-1] * filas
    for col in range(columnas-1):
        fila_pivote = None
        for f in range(pivote, filas):
            if abs(A[f][col]) > 1e-10:
                fila_pivote = f
                break
        if fila_pivote is None:
            continue
        A[pivote], A[fila_pivote] = A[fila_pivote], A[pivote]
        factor = A[pivote][col]
        A[pivote] = [x / factor for x in A[pivote]]
        pos_pivotes[pivote] = col
        for f in range(filas):
            if f != pivote and abs(A[f][col]) > 1e-10:
                factor = A[f][col]
                A[f] = [a - factor * b for a, b in zip(A[f], A[pivote])]
        pivote += 1
    # Identifica variables libres
    pivotes = set([p for p in pos_pivotes if p != -1])
    libres = [j for j in range(n) if j not in pivotes]
    if len(libres) == 0:
        return True, None, None  # Solo solución trivial
    # Encuentra una relación de dependencia lineal (pon una variable libre = 1, el resto = 0)
    solucion = [0] * n
    libre = libres[0]
    solucion[libre] = 1
    # Sustituye hacia atrás para encontrar las básicas
    for i in reversed(range(filas)):
        if pos_pivotes[i] == -1:
            continue
        suma = 0
        for j in range(pos_pivotes[i]+1, n):
            suma += A[i][j] * solucion[j]
        solucion[pos_pivotes[i]] = -suma
    return False, libres, solucion

def son_linealmente_independientes(vectores):
    n = len(vectores[0])
    p = len(vectores)
    for idx, v in enumerate(vectores):
        if es_vector_cero(v):
            return False, f"El vector {idx+1} es el vector cero, por lo tanto el conjunto es linealmente dependiente."
    if p > n:
        return False, f"Hay más vectores ({p}) que la dimensión del espacio ({n}), por lo tanto el conjunto es linealmente dependiente."
    if p == 1:
        if not es_vector_cero(vectores[0]):
            return True, "Un solo vector distinto de cero es linealmente independiente."
        else:
            return False, "El único vector es el vector cero, por lo tanto es linealmente dependiente."
    if p == 2:
        if son_multiplos(vectores[0], vectores[1]):
            return False, "Uno de los vectores es múltiplo del otro, por lo tanto el conjunto es linealmente dependiente."
        else:
            return True, "Ningún vector es múltiplo del otro, por lo tanto el conjunto es linealmente independiente."
    # Caso general: Gauss-Jordan y justificación teórica
    independiente, libres, relacion = gauss_jordan_homogeneo_con_relacion(vectores)
    if independiente:
        return True, "La única solución al sistema homogéneo es la trivial, por lo tanto son linealmente independientes."
    else:
        # Construye la relación de dependencia lineal explícita
        rel = " + ".join([f"({relacion[i]:.2f})·v{i+1}" for i in range(len(relacion)) if abs(relacion[i]) > 1e-10])
        return False, (
            "Hay variables libres en el sistema homogéneo, por lo tanto existe una solución no trivial.\n"
            "Por ejemplo, una relación de dependencia lineal es:\n"
            f"{rel} = 0"
        )

class IndependenciaLinealApp:
    def __init__(self, root, volver_callback):
        self.root = root
        self.volver_callback = volver_callback
        self.root.title("Independencia Lineal de Vectores")
        self.root.configure(bg="#ffe4e6")
        self._setup_styles()
        self._setup_widgets()

    def _setup_styles(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except Exception:
            pass
        style.configure("Primary.TButton", font=("Segoe UI", 11, "bold"), padding=8,
                        background="#fbb6ce", foreground="#fff")
        style.map("Primary.TButton",
                  background=[("!disabled", "#fbb6ce"), ("active", "#f472b6")],
                  foreground=[("!disabled", "white"), ("active", "white")])
        style.configure("Back.TButton", font=("Segoe UI", 11, "bold"), padding=6,
                        background="#fecaca", foreground="#b91c1c")
        style.map("Back.TButton",
                  background=[("!disabled", "#fecaca"), ("active", "#fca5a5")],
                  foreground=[("!disabled", "#b91c1c"), ("active", "#7f1d1d")])

    def _setup_widgets(self):
        frame = ttk.Frame(self.root, padding=10, style="TFrame")
        frame.pack(fill="both", expand=True)

        arriba = ttk.Frame(frame, style="TFrame")
        arriba.pack(pady=5)
        ttk.Label(arriba, text="Dimensión:", background="#ffe4e6", font=("Segoe UI", 11)).pack(side="left")
        self.dim_var = tk.IntVar(value=3)
        dim_spin = ttk.Spinbox(arriba, from_=1, to=10, width=3, textvariable=self.dim_var, font=("Segoe UI", 11))
        dim_spin.pack(side="left", padx=5)
        ttk.Label(arriba, text="Cantidad de vectores:", background="#ffe4e6", font=("Segoe UI", 11)).pack(side="left")
        self.cant_var = tk.IntVar(value=2)
        cant_spin = ttk.Spinbox(arriba, from_=1, to=10, width=3, textvariable=self.cant_var, font=("Segoe UI", 11))
        cant_spin.pack(side="left", padx=5)
        ttk.Button(arriba, text="Volver", style="Back.TButton", command=self.volver_callback).pack(side="left", padx=15)

        # Actualiza entradas automáticamente al cambiar los spinbox
        self.dim_var.trace_add("write", lambda *a: self._crear_entradas())
        self.cant_var.trace_add("write", lambda *a: self._crear_entradas())

        self.entradas_frame = ttk.Frame(frame, style="TFrame")
        self.entradas_frame.pack(pady=15)

        abajo = ttk.Frame(frame, style="TFrame")
        abajo.pack(pady=5)
        ttk.Button(abajo, text="Verificar independencia", style="Primary.TButton", command=self.verificar).pack(side="left", padx=10)
        self.resultado = tk.Text(abajo, width=70, height=7, state="disabled", font=("Consolas", 11), bg="#fff0f6", fg="#b91c1c", wrap="word")
        self.resultado.pack(side="left", padx=10)

        self._crear_entradas()

    def _crear_entradas(self):
        for widget in self.entradas_frame.winfo_children():
            widget.destroy()
        dim = self.dim_var.get()
        cant = self.cant_var.get()
        self.entradas = []
        for j in range(cant):
            col = []
            col_frame = ttk.Frame(self.entradas_frame, style="TFrame")
            col_frame.pack(side="left", padx=12)
            ttk.Label(col_frame, text=f"v{j+1}", font=("Segoe UI", 11, "bold"), background="#ffe4e6", foreground="#b91c1c").pack()
            for i in range(dim):
                e = ttk.Entry(col_frame, width=6, justify="center", font=("Segoe UI", 11))
                e.pack(pady=2)
                col.append(e)
            self.entradas.append(col)

    def verificar(self):
        try:
            vectores = []
            for col in self.entradas:
                v = [float(e.get()) for e in col]
                vectores.append(v)
        except Exception:
            messagebox.showerror("Error", "Por favor, ingresa todos los valores numéricos.")
            return
        independiente, justificacion = son_linealmente_independientes(vectores)
        self.resultado.configure(state="normal")
        self.resultado.delete("1.0", tk.END)
        if independiente:
            self.resultado.insert(tk.END, "✅ El conjunto es linealmente INDEPENDIENTE.\n\n")
        else:
            self.resultado.insert(tk.END, "❌ El conjunto es linealmente DEPENDIENTE.\n\n")
        self.resultado.insert(tk.END, justificacion)
        self.resultado.configure(state="disabled")