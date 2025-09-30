import tkinter as tk
from tkinter import ttk, messagebox
from fractions import Fraction
from copy import deepcopy


class GaussJordanApp:
    def __init__(self, root, volver_callback):
        # Callback para regresar al inicio
        self.volver_callback = volver_callback


        # Configuración de la ventana principal
        self.root = root
        self.root.title("Método de Eliminación de Gauss-Jordan")
        self.root.geometry("1250x900")
        self.root.configure(bg="#ffe4e6")  # Fondo rosita pastel


        # Configuración de estilos y widgets iniciales
        self._setup_styles()
        self._setup_widgets()

        # Variables internas
        self.pasos_guardados = []
        self.matriz_original = None
        self.matriz_final = None
        self.soluciones = None
        self.detalle_button = None
        self.mostrando_detalles = False


        # El botón "Volver" se creará dentro de frame_matriz (debajo de los botones)
        self.boton_volver = None


    # ---------------------------------------------------------
    # Configuración de estilos visuales
    # ---------------------------------------------------------
    def _setup_styles(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except Exception:
            pass
        style.configure("TLabel", font=("Segoe UI", 12), background="#ffe4e6", foreground="#b91c1c")
        style.configure("TEntry", font=("Segoe UI", 12))
        style.configure("Primary.TButton", font=("Segoe UI", 12, "bold"), padding=8,
                        background="#fbb6ce", foreground="#fff")
        style.map("Primary.TButton",
                  background=[("!disabled", "#fbb6ce"), ("active", "#f472b6")],
                  foreground=[("!disabled", "white"), ("active", "white")])


        # Estilo original para botones de volver (se mantiene para MenuMatrices)
        style.configure("Back.TButton", font=("Segoe UI", 12, "bold"), padding=8,
                        background="#fecaca", foreground="#b91c1c")
        style.map("Back.TButton",
                  background=[("!disabled", "#fecaca"), ("active", "#fca5a5")],
                  foreground=[("!disabled", "#b91c1c"), ("active", "#7f1d1d")])



    # ---------------------------------------------------------
    # Creación de los elementos gráficos principales
    # ---------------------------------------------------------
    def _setup_widgets(self):            
        frame_top = ttk.Frame(self.root, padding=20, style="TFrame")
        frame_top.pack(fill="x", pady=10)




        # Entrada para número de ecuaciones (Spinbox)
        ttk.Label(frame_top, text="Número de ecuaciones:").grid(row=0, column=0, padx=8, pady=5, sticky="e")
        self.ecuaciones_var = tk.IntVar(value=2)
        tk.Spinbox(frame_top, from_=1, to=20, textvariable=self.ecuaciones_var, width=6, font=("Segoe UI", 12),
                   justify="center").grid(row=0, column=1, padx=8, pady=5)



        # Entrada para número de incógnitas (Spinbox)
        ttk.Label(frame_top, text="Número de incógnitas:").grid(row=0, column=2, padx=8, pady=5, sticky="e")
        self.incognitas_var = tk.IntVar(value=2)
        tk.Spinbox(frame_top, from_=1, to=20, textvariable=self.incognitas_var, width=6, font=("Segoe UI", 12),
                   justify="center").grid(row=0, column=3, padx=8, pady=5)




        # Botón para crear la matriz
        ttk.Button(frame_top, text="Crear matriz", style="Primary.TButton", command=self.crear_matriz).grid(row=0,
                                                                                                           column=4,
                                                                                                           padx=20)

        # Contenedor de la matriz
        self.frame_matriz = ttk.Frame(self.root, padding=20)
        self.frame_matriz.pack()


        # Área de resultados
        frame_result = ttk.LabelFrame(self.root, text="Resultados", padding=15, labelanchor="n")
        frame_result.pack(fill="both", expand=True, padx=15, pady=15)


        self.text_result = tk.Text(frame_result, height=35, wrap="none",
                                   font=("Consolas", 11), bg="#fff0f5", fg="#222",
                                   relief="solid", borderwidth=1)
        self.text_result.pack(side="left", fill="both", expand=True)


        scroll_y = ttk.Scrollbar(frame_result, orient="vertical", command=self.text_result.yview)
        scroll_y.pack(side="right", fill="y")
        self.text_result.configure(yscrollcommand=scroll_y.set, state="disabled")



        self.text_result.tag_configure("bold", font=("Consolas", 12, "bold"))
        self.text_result.tag_configure("comment", font=("Consolas", 10, "italic"), foreground="#555")


    # ---------------------------------------------------------
    # Crear la matriz en pantalla
    # ---------------------------------------------------------
    def crear_matriz(self):
        for w in self.frame_matriz.winfo_children():
            w.destroy()




        filas = self.ecuaciones_var.get()
        columnas = self.incognitas_var.get()
        if filas <= 0 or columnas <= 0:
            messagebox.showerror("Error", "Ingrese dimensiones mayores que 0.")
            return



        self.filas = filas
        self.columnas = columnas + 1  # última columna = términos independientes
        self.entries = []


        # Encabezados x1, x2, x3...
        for j in range(columnas):
            ttk.Label(self.frame_matriz, text=f"x{j + 1}", font=("Segoe UI", 12, "bold"), background="#ffe4e6",
                      foreground="#b91c1c").grid(row=0, column=j, padx=6, pady=6)
        ttk.Label(self.frame_matriz, text="b", font=("Segoe UI", 12, "bold"), background="#ffe4e6",
                  foreground="#b91c1c").grid(row=0, column=columnas, padx=6, pady=6)



        # Entradas de la matriz
        for i in range(filas):
            fila_entries = []
            for j in range(self.columnas):
                e = ttk.Entry(self.frame_matriz, width=8, justify="center")
                e.grid(row=i + 1, column=j, padx=6, pady=6)
                fila_entries.append(e)
            self.entries.append(fila_entries)



        # Botón "Resolver"
        ttk.Button(self.frame_matriz, text="Resolver", style="Primary.TButton", command=self.resolver).grid(
            row=self.filas + 1, columnspan=self.columnas, pady=20)


        # Si existen detalles previos, limpiarlos
        if self.detalle_button:
            self.detalle_button.destroy()
            self.detalle_button = None
            self.mostrando_detalles = False



        # Colocar (o crear) el botón "Volver al inicio" justo debajo del botón "Resolver"
        # Usamos el estilo Primary.TButton para que sea igualito a los botones del menú principal
        if not self.boton_volver:
            self.boton_volver = ttk.Button(self.frame_matriz, text="Volver al inicio",
                                           style="Primary.TButton", command=self.volver_callback)
            self.boton_volver.grid(row=self.filas + 2, columnspan=self.columnas, pady=10)
        else:
            # Reposicionar si ya existía
            try:
                self.boton_volver.grid_forget()
            except Exception:
                pass
            self.boton_volver.grid(row=self.filas + 2, columnspan=self.columnas, pady=10)


    # ---------------------------------------------------------
    # Convertir datos y aplicar Gauss-Jordan
    # ---------------------------------------------------------
    def resolver(self):
        try:
            matriz_original = []
            for i in range(self.filas):
                fila = []
                for j in range(self.columnas):
                    val_str = self.entries[i][j].get().strip()
                    if val_str == "":
                        val_str = "0"
                    fila.append(Fraction(val_str))
                matriz_original.append(fila)



            self.matriz_original = deepcopy(matriz_original)
            A = deepcopy(matriz_original)
            pasos = self.gauss_jordan(A, self.filas, self.columnas)
            self.pasos_guardados = pasos
            self.matriz_final = A



            self.soluciones, _ = self._extraer_soluciones(A)
            self.mostrar_resumen()



            if self.detalle_button:
                self.detalle_button.destroy()
            self.mostrando_detalles = False



            # 🔹 Botón de pasos detallados
            self.detalle_button = ttk.Button(self.frame_matriz, text="Ver pasos detallados",
                                            style="Primary.TButton", command=self.toggle_detalles)
            self.detalle_button.grid(row=self.filas + 2, columnspan=self.columnas, pady=10)


            # 🔹 Botón volver al inicio justo debajo de "Ver pasos detallados"
            if not self.boton_volver:
                self.boton_volver = ttk.Button(self.frame_matriz, text="Volver al inicio",
                                               style="Primary.TButton", command=self.volver_callback)
                self.boton_volver.grid(row=self.filas + 3, columnspan=self.columnas, pady=10)
            else:
                try:
                    self.boton_volver.grid_forget()
                except Exception:
                    pass
                self.boton_volver.grid(row=self.filas + 3, columnspan=self.columnas, pady=10)



        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")


    # ---------------------------------------------------------
    # Extraer soluciones de la matriz reducida
    # ---------------------------------------------------------
    def _extraer_soluciones(self, A):
        n, m = self.filas, self.columnas
        num_vars = m - 1
        soluciones = [None] * num_vars



        for i in range(n):
            if all(A[i][j] == 0 for j in range(num_vars)) and A[i][-1] != 0:
                return None, "incompatible"




        pivotes = [-1] * n
        columnas_pivote = []
        for i in range(n):
            for j in range(num_vars):
                if A[i][j] == 1 and all(A[k][j] == 0 for k in range(n) if k != i):
                    pivotes[i] = j
                    columnas_pivote.append(j)
                    break



        libres = [j for j in range(num_vars) if j not in columnas_pivote]



        if libres:
            expresiones = {}
            for i in range(n):
                if pivotes[i] != -1:
                    expr = str(A[i][-1])
                    for j in libres:
                        coef = -A[i][j]
                        if coef != 0:
                            expr += f" + ({coef})*x{j+1}"
                    expresiones[pivotes[i]] = expr




            for j in range(num_vars):
                if j in expresiones:
                    soluciones[j] = expresiones[j]
                elif j in libres:
                    soluciones[j] = f"x{j+1} es variable libre"
                else:
                    soluciones[j] = "0"
            return soluciones, "indeterminado"




        for i in range(min(n, num_vars)):
            if pivotes[i] != -1:
                soluciones[pivotes[i]] = A[i][-1]
        return soluciones, "determinado"


    # ---------------------------------------------------------
    # Mostrar resumen final
    # ---------------------------------------------------------
    def mostrar_resumen(self):
        self.text_result.configure(state="normal")
        self.text_result.delete("1.0", tk.END)



        self.text_result.insert(tk.END, "===== SOLUCIÓN FINAL =====\n", ("bold",))
        if self.matriz_final is None:
            self.text_result.insert(tk.END, "(no hay soluciones calculadas)\n")
            self.text_result.configure(state="disabled")
            return



        soluciones, tipo = self._extraer_soluciones(self.matriz_final)



        if tipo == "incompatible":
            self.text_result.insert(tk.END, "El sistema es inconsistente: aparece una fila del tipo 0 = b con b≠0\n")
        elif tipo == "determinado":
            self.text_result.insert(tk.END, "El sistema tiene solución única:\n")
            for i, val in enumerate(soluciones):
                self.text_result.insert(tk.END, f"x{i+1} = {val}\n")
        elif tipo == "indeterminado":
            self.text_result.insert(tk.END, "El sistema tiene infinitas soluciones:\n")
            for i, val in enumerate(soluciones):
                self.text_result.insert(tk.END, f"x{i+1} = {val}\n")


        self.text_result.configure(state="disabled")



    # ---------------------------------------------------------
    # Alternar entre resumen y pasos
    # ---------------------------------------------------------
    def toggle_detalles(self):
        if self.mostrando_detalles:
            self.mostrar_resumen()
            if self.detalle_button:
                self.detalle_button.config(text="Ver pasos detallados")
            self.mostrando_detalles = False
        else:
            self.mostrar_detalles()
            if self.detalle_button:
                self.detalle_button.config(text="Ocultar pasos detallados")
            self.mostrando_detalles = True



    # ---------------------------------------------------------
    # Mostrar pasos del método
    # ---------------------------------------------------------
    def mostrar_detalles(self):
        self.text_result.configure(state="normal")
        self.text_result.delete("1.0", tk.END)



        for step in self.pasos_guardados:
            self._insert_header(step["titulo"], step.get("comentario", ""))
            oper_lines = step["oper_lines"]
            matriz_lines = step["matriz_lines"]



            max_left = max((len(s) for s in oper_lines), default=0)
            sep = "   |   "
            max_len = max(len(oper_lines), len(matriz_lines))
            for i in range(max_len):
                left = oper_lines[i] if i < len(oper_lines) else ""
                right = matriz_lines[i] if i < len(matriz_lines) else ""
                line_text = left.ljust(max_left) + (sep if right else "") + right + "\n"
                self.text_result.insert(tk.END, line_text)
            self.text_result.insert(tk.END, "\n" + "-" * 110 + "\n\n")



        self.text_result.insert(tk.END, "===== SOLUCIÓN FINAL =====\n", ("bold",))
        soluciones, tipo = self._extraer_soluciones(self.matriz_final)
        for i, val in enumerate(soluciones):
            self.text_result.insert(tk.END, f"x{i+1} = {val}\n")
        self.text_result.configure(state="disabled")



    # ---------------------------------------------------------
    # Inserta un encabezado en el área de resultados
    # ---------------------------------------------------------
    def _insert_header(self, titulo, comentario=""):
        self.text_result.insert(tk.END, "Operación: ")
        start = self.text_result.index(tk.END)
        self.text_result.insert(tk.END, titulo)
        end = self.text_result.index(tk.END)
        self.text_result.tag_add("bold", start, end)
        if comentario:
            self.text_result.insert(tk.END, "  —  ")
            c_start = self.text_result.index(tk.END)
            self.text_result.insert(tk.END, comentario)
            c_end = self.text_result.index(tk.END)
            self.text_result.tag_add("comment", c_start, c_end)
        self.text_result.insert(tk.END, "\n\n")


    # ---------------------------------------------------------
    # Algoritmo Gauss-Jordan
    # ---------------------------------------------------------
    def gauss_jordan(self, A, n, m):
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
                    "titulo": f"F{fila_pivote+1} ↔ F{pivote+1}",
                    "comentario": f"Intercambio de filas para poner un pivote no nulo en la columna {col+1}",
                    "oper_lines": [],
                    "matriz_lines": self.format_matriz_lines(A)
                })




            divisor = A[fila_pivote][col]
            if divisor == 0:
                fila_pivote += 1
                continue
            if divisor != 1:
                A[fila_pivote] = [val / divisor for val in A[fila_pivote]]
                pasos.append({
                    "titulo": f"F{fila_pivote+1} → F{fila_pivote+1}/{divisor}",
                    "comentario": f"Normalización: se convierte en pivote a 1 en la columna {col+1}",
                    "oper_lines": [],
                    "matriz_lines": self.format_matriz_lines(A)
                })




            for f in range(n):
                if f != fila_pivote and A[f][col] != 0:
                    factor = A[f][col]
                    original_fila = A[f][:]
                    A[f] = [original_fila[j] - factor * A[fila_pivote][j] for j in range(m)]
                    oper_lines = self.format_operacion_vertical_lines(
                        A[fila_pivote], original_fila, factor, A[f], fila_pivote + 1, f + 1
                    )
                    pasos.append({
                        "titulo": f"F{f+1} → F{f+1} - ({factor})F{fila_pivote+1}",
                        "comentario": f"Se anula el elemento en la columna {col+1} usando la fila pivote",
                        "oper_lines": oper_lines,
                        "matriz_lines": self.format_matriz_lines(A)
                    })
            fila_pivote += 1
            if fila_pivote >= n:
                break
        return pasos




    # ---------------------------------------------------------
    # Funciones auxiliares
    # ---------------------------------------------------------
    def format_operacion_vertical_lines(self, fila_pivote, fila_actual, factor, fila_result, idx_piv, idx_obj):
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


    def format_matriz_lines(self, A):
        ancho = max((len(str(x)) for fila in A for x in fila), default=1)
        lines = []
        for fila in A:
            line = " ".join(str(x).rjust(ancho) for x in fila)
            lines.append(line)
        return lines
