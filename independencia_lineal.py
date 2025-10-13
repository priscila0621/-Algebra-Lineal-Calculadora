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


# ---------- Función de independencia ----------
def son_linealmente_independientes(vectores):
    n = len(vectores[0])
    p = len(vectores)


    resultado = ""
    reglas_aplicadas = []


    # Reglas básicas
    for idx, v in enumerate(vectores):
        if es_vector_cero(v):
            reglas_aplicadas.append(f"• El conjunto contiene el vector cero (v{idx+1} = {v}), por lo que es linealmente dependiente.")
   
    if p > n:
        reglas_aplicadas.append(f"• El conjunto tiene más vectores ({p}) que dimensiones ({n}), por lo que es linealmente dependiente.")
   
    if p == 1:
        if not es_vector_cero(vectores[0]):
            reglas_aplicadas.append("• Un conjunto que solo tiene un vector v es linealmente independiente si y solo si v no es el vector cero.")
        else:
            reglas_aplicadas.append("• El único vector es el vector cero, por lo que el conjunto es linealmente dependiente.")
   
    if p == 2:
        if son_multiplos(vectores[0], vectores[1]):
            reglas_aplicadas.append("• Un conjunto de dos vectores {v₁, v₂} es linealmente dependiente si al menos uno de los vectores es un múltiplo del otro.")
        else:
            reglas_aplicadas.append("• Un conjunto de dos vectores {v₁, v₂} es linealmente independiente si y solo si ninguno de los vectores es un múltiplo del otro.")


    # Si alguna regla básica ya determinó dependencia o independencia para 1 o 2 vectores
    if p <= 2 and reglas_aplicadas:
        resultado += "📘 Reglas aplicadas:\n" + "\n".join(reglas_aplicadas) + "\n\n"
        # Solo consideramos reglas que indiquen explícitamente "dependiente"
        if any("es linealmente dependiente" in r for r in reglas_aplicadas):
            resultado += "❌ El conjunto es linealmente DEPENDIENTE.\n"
            return False, resultado
        else:
            resultado += "✅ El conjunto es linealmente INDEPENDIENTE.\n"
            return True, resultado


    # -------------------
    # Combinación lineal (caso general)
    # -------------------
    A = [list(col) for col in zip(*vectores)]
    for fila in A:
        fila.append(0)  # columna de ceros


    filas = len(A)
    columnas = len(A[0])
    pasos = ["📗 Procedimiento paso a paso (Gauss-Jordan):\n\n"]
    pivote = 0
    pos_pivotes = [-1] * filas


    def formato_matriz(M):
        """Devuelve la matriz alineada con espaciado uniforme."""
        filas_txt = []
        for fila in M:
            fila_txt = "  ".join(f"{int(x) if abs(x - int(x)) < 1e-10 else round(x, 2):>4}" for x in fila[:-1])
            fila_txt += "  |  " + f"{int(fila[-1]) if abs(fila[-1]-int(fila[-1]))<1e-10 else round(fila[-1],2):>4}"
            filas_txt.append("[ " + fila_txt + " ] ")
        return "\n".join(filas_txt)


    for col in range(columnas - 1):
        fila_pivote = None
        for f in range(pivote, filas):
            if abs(A[f][col]) > 1e-10:
                fila_pivote = f
                break
        if fila_pivote is None:
            continue
        if fila_pivote != pivote:
            A[pivote], A[fila_pivote] = A[fila_pivote], A[pivote]
            pasos.append(f"↔ Se intercambian filas F{pivote+1} ↔ F{fila_pivote+1}\n")
            pasos.append(formato_matriz(A) + "\n\n")


        factor = A[pivote][col]
        if abs(factor) > 1e-10:
            A[pivote] = [x / factor for x in A[pivote]]
            pasos.append(f"F{pivote+1} → F{pivote+1} / {int(factor) if factor == int(factor) else round(factor,2)}\n")
            pasos.append(formato_matriz(A) + "\n\n")


        for f in range(filas):
            if f != pivote and abs(A[f][col]) > 1e-10:
                factor = A[f][col]
                A[f] = [a - factor * b for a, b in zip(A[f], A[pivote])]
                pasos.append(f"F{f+1} → F{f+1} - ({int(factor) if factor==int(factor) else round(factor,2)})·F{pivote+1}\n")
                pasos.append(formato_matriz(A) + "\n\n")
        pos_pivotes[pivote] = col
        pivote += 1


    pivotes = set([p for p in pos_pivotes if p != -1])
    libres = [j for j in range(n) if j not in pivotes]
    solucion = [0] * n


    # Agregamos regla combinada de dependencia lineal
    if libres:
        reglas_aplicadas.append("• Es linealmente dependiente si existen coeficientes no todos cero tales que c₁v₁ + c₂v₂ + ⋯ + cₚvₚ = 0, es decir, al menos uno de los vectores puede escribirse como combinación lineal de los demás.")
        resultado += "📘 Reglas aplicadas:\n" + "\n".join(reglas_aplicadas) + "\n\n"
        pasos.append(f"Variables libres: {', '.join('X'+str(i+1) for i in libres)}\n\n")
        solucion[libres[0]] = 1
        for i in reversed(range(filas)):
            if pos_pivotes[i] == -1:
                continue
            suma = sum(A[i][j] * solucion[j] for j in range(pos_pivotes[i]+1, n))
            solucion[pos_pivotes[i]] = -suma
        pasos.append("Solución particular (no trivial):\n")
        pasos.append(", ".join([f"X{i+1} = {int(solucion[i]) if abs(solucion[i]-int(solucion[i]))<1e-10 else round(solucion[i],2)}" for i in range(n)]) + "\n\n")
        resultado += "".join(pasos)
        resultado += "🧩 Como existe una solución no trivial, el conjunto es **linealmente DEPENDIENTE**.\n"
        return False, resultado
    else:
        reglas_aplicadas.append("• Se dice que un conjunto de vectores {v₁,…,vₚ} en ℝⁿ es linealmente independiente si la ecuación x₁v₁ + x₂v₂ + ⋯ + xₚvₚ = 0 solo tiene la solución trivial (todos los coeficientes son cero).")
        resultado += "📘 Reglas aplicadas:\n" + "\n".join(reglas_aplicadas) + "\n\n"
        pasos.append("Solución trivial:\n")
        pasos.append(", ".join([f"X{i+1} = {int(solucion[i])}" for i in range(n)]) + "\n\n")
        resultado += "".join(pasos)
        resultado += "🧩 Como solo existe la solución trivial, el conjunto es **linealmente INDEPENDIENTE**.\n"
        return True, resultado


# -------------------- Interfaz Gráfica --------------------
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


        self.dim_var.trace_add("write", lambda *a: self._crear_entradas())
        self.cant_var.trace_add("write", lambda *a: self._crear_entradas())


        self.entradas_frame = ttk.Frame(frame, style="TFrame")
        self.entradas_frame.pack(pady=15)


        abajo = ttk.Frame(frame, style="TFrame")
        abajo.pack(pady=5)
        ttk.Button(abajo, text="Verificar independencia", style="Primary.TButton", command=self.verificar).pack(side="left", padx=10)
        self.resultado = tk.Text(abajo, width=70, height=20, state="disabled", font=("Consolas", 11),
                                 bg="#fff0f6", fg="black", wrap="word")
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
            ttk.Label(col_frame, text=f"v{j+1}", font=("Segoe UI", 11, "bold"),
                      background="#ffe4e6", foreground="#b91c1c").pack()
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
        self.resultado.insert(tk.END, justificacion)
        self.resultado.configure(state="disabled")



