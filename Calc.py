import tkinter as tk
from tkinter import ttk, messagebox
from fractions import Fraction
from copy import deepcopy


# ============================================================
# Clase principal de la aplicación GaussJordanApp
# ============================================================
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



# ============================================================
# MENÚ PRINCIPAL
# ============================================================
class MenuPrincipal:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora Álgebra Lineal")
        self.root.geometry("600x400")
        self.root.configure(bg="#ffe4e6")

        ttk.Label(root, text="Calculadora Álgebra Lineal",
                  font=("Segoe UI", 20, "bold"), background="#ffe4e6",
                  foreground="#b91c1c").pack(pady=40)



        ttk.Button(root, text="Resolver sistema de ecuaciones lineales",
                   style="Primary.TButton", command=self.abrir_sistema).pack(pady=10)


        ttk.Button(root, text="Operaciones con matrices",
                   style="Primary.TButton", command=self.abrir_matrices).pack(pady=10)
        



    def abrir_sistema(self):
        self.root.destroy()
        root2 = tk.Tk()
        GaussJordanApp(root2, lambda: self.volver_inicio(root2))
        root2.mainloop()


    def abrir_matrices(self):
        self.root.destroy()
        root2 = tk.Tk()
        MenuMatrices(root2, lambda: self.volver_inicio(root2))
        root2.mainloop()


    def volver_inicio(self, ventana_actual):
        ventana_actual.destroy()
        root = tk.Tk()
        MenuPrincipal(root)
        root.mainloop()



# ============================================================
# MENÚ DE MATRICES (CON BOTÓN VOLVER MODIFICADO)
# ============================================================
class MenuMatrices:
    def __init__(self, root, volver_callback):
        self.root = root
        self.root.title("Operaciones con Matrices")
        self.root.geometry("600x400")
        self.root.configure(bg="#ffe4e6")
        self.volver_callback = volver_callback




        ttk.Label(root, text="Operaciones con Matrices",
                  font=("Segoe UI", 18, "bold"), background="#ffe4e6",
                  foreground="#b91c1c").pack(pady=40)



        ttk.Button(root, text="Suma de matrices", style="Primary.TButton",
                   command=self.suma_matrices).pack(pady=10)


        ttk.Button(root, text="Resta de matrices", style="Primary.TButton",
           command=self.resta_matrices).pack(pady=10)


        ttk.Button(root, text="Multiplicación de matrices", style="Primary.TButton",
                   command=self.multiplicacion_matrices).pack(pady=10)
        
        

        # 🔹 Frame fijo en la parte inferior para el botón volver
        self.frame_volver_fijo = ttk.Frame(root)
        self.frame_volver_fijo.pack(side="bottom", fill="x")
        self.boton_volver = ttk.Button(self.frame_volver_fijo, text="Volver al inicio", style="Back.TButton",
                                       command=self.volver_callback)
        self.boton_volver.pack(pady=10)




    def suma_matrices(self):
        # Abre la interfaz de Suma de Matrices en una nueva ventana (Toplevel).
        # Se usa self.root.withdraw() para ocultar este menú mientras el usuario trabaja
        # en la suma; el botón "Volver al inicio" dentro de la nueva ventana llamará
        # al callback original para regresar al inicio (sin tocar el resto del código).
        try:
            self.root.withdraw()
            top = tk.Toplevel(self.root)
            # Pasamos el callback original para que desde la Suma de Matrices se pueda volver al inicio
            SumaMatricesApp(top, volver_callback=self.volver_callback)
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al abrir Suma de matrices: {e}")
        try:
            self.boton_volver.lift()
        except Exception:
            pass

    def resta_matrices(self):
        try:
            self.root.withdraw()
            top = tk.Toplevel(self.root)
            RestaMatricesApp(top, volver_callback=self.volver_callback)
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al abrir Resta de matrices: {e}")
        try:
            self.boton_volver.lift()
        except Exception:
            pass


    def multiplicacion_matrices(self):
        try:
            self.root.withdraw()
            top = tk.Toplevel(self.root)
            MultiplicacionMatricesApp(top, volver_callback=self.volver_callback)
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al abrir Multiplicación de matrices: {e}")
        try:
            self.boton_volver.lift()
        except Exception:
            pass





# ============================================================
# CLASE: SumaMatricesApp (CON MEJORAS DE RESUMEN Y DETALLE)
# ============================================================
import tkinter as tk
from tkinter import ttk, messagebox
from fractions import Fraction


class SumaMatricesApp:
    def __init__(self, root, volver_callback):
        self.root = root
        self.volver_callback = volver_callback

        self.root.title("Suma de Matrices")
        self.root.geometry("900x700")
        self.root.configure(bg="#ffe4e6")

        style = ttk.Style()
        try:
            style.theme_use("clam")
        except Exception:
            pass
        style.configure("TLabel", font=("Segoe UI", 12), background="#ffe4e6", foreground="#b91c1c")
        style.configure("Primary.TButton", font=("Segoe UI", 12, "bold"), padding=8,
                        background="#fbb6ce", foreground="#fff")
        style.map("Primary.TButton",
                  background=[("!disabled", "#fbb6ce"), ("active", "#f472b6")],
                  foreground=[("!disabled", "white"), ("active", "white")])
        style.configure("Back.TButton", font=("Segoe UI", 12, "bold"), padding=6,
                        background="#fecaca", foreground="#b91c1c")
        style.map("Back.TButton",
                  background=[("!disabled", "#fecaca"), ("active", "#fca5a5")],
                  foreground=[("!disabled", "#b91c1c"), ("active", "#7f1d1d")])

        self.num_matrices = 0
        self.rows = 0
        self.cols = 0
        self.matrices = []
        self.current_matrix = 0
        self.entries = []

        self.main_frame = ttk.Frame(self.root, padding=12)
        self.main_frame.pack(fill="both", expand=True)

        self.error_label = None

        self.show_welcome()

    # ---------------- Helpers ----------------
    def clear_main(self):
        for w in self.main_frame.winfo_children():
            w.destroy()

    def add_back_button(self, parent_frame=None):
        container = parent_frame if parent_frame is not None else self.main_frame
        back = ttk.Button(container, text="Volver al inicio", style="Back.TButton",
                          command=self._volver_al_inicio)
        back.pack(side="bottom", pady=8)

    def _volver_al_inicio(self):
        try:
            self.volver_callback()
        except Exception:
            pass
        finally:
            try:
                self.root.destroy()
            except Exception:
                pass

    def _parse_fraction(self, s):
        s = s.strip()
        if s == "":
            raise ValueError("Vacío")
        s = s.replace(",", ".")
        return Fraction(s)

    # ---------------- Pantalla bienvenida ----------------
    def show_welcome(self):
        self.clear_main()
        ttk.Label(self.main_frame, text="Suma de Matrices", font=("Segoe UI", 18, "bold"),
                  background="#ffe4e6", foreground="#b91c1c").pack(pady=12)
        ttk.Label(self.main_frame, text="Suma hasta N matrices con las mismas dimensiones",
                  font=("Segoe UI", 12), background="#ffe4e6", foreground="#7f1d1d").pack(pady=6)

        start_btn = ttk.Button(self.main_frame, text="Comenzar", style="Primary.TButton",
                               command=self.ask_num_and_dimensions)
        start_btn.pack(pady=20)
        self.add_back_button(self.main_frame)

    # ---------------- Configuración ----------------
    def ask_num_and_dimensions(self):
        self.clear_main()
        ttk.Label(self.main_frame, text="Configuración - Cantidad y dimensiones", font=("Segoe UI", 14, "bold"),
                  background="#ffe4e6", foreground="#b91c1c").pack(pady=10)

        frame = ttk.Frame(self.main_frame, padding=8)
        frame.pack(pady=8)

        ttk.Label(frame, text="¿Cuántas matrices deseas sumar?", background="#ffe4e6").grid(row=0, column=0, padx=6, pady=6, sticky="w")
        self.num_var = tk.StringVar()
        tk.Entry(frame, textvariable=self.num_var, width=6, font=("Segoe UI", 12), bg="#fff0f5").grid(row=0, column=1, padx=6, pady=6)

        ttk.Label(frame, text="Filas:", background="#ffe4e6").grid(row=1, column=0, padx=6, pady=6, sticky="w")
        self.row_var = tk.StringVar()
        tk.Entry(frame, textvariable=self.row_var, width=6, font=("Segoe UI", 12), bg="#fff0f5").grid(row=1, column=1, padx=6, pady=6)

        ttk.Label(frame, text="Columnas:", background="#ffe4e6").grid(row=1, column=2, padx=6, pady=6, sticky="w")
        self.col_var = tk.StringVar()
        tk.Entry(frame, textvariable=self.col_var, width=6, font=("Segoe UI", 12), bg="#fff0f5").grid(row=1, column=3, padx=6, pady=6)

        ttk.Button(self.main_frame, text="Siguiente", style="Primary.TButton",
                   command=self.save_num_and_dimensions).pack(pady=12)

        self.error_label = ttk.Label(self.main_frame, text="", foreground="red", background="#ffe4e6")
        self.error_label.pack()
        self.add_back_button(self.main_frame)

    def save_num_and_dimensions(self):
        try:
            n = int(self.num_var.get())
            r = int(self.row_var.get())
            c = int(self.col_var.get())
            if n < 2 or r <= 0 or c <= 0:
                raise ValueError
        except Exception:
            messagebox.showerror("Error", "Ingresa números válidos (mínimo 2 matrices, dimensiones > 0)")
            return
        self.num_matrices, self.rows, self.cols = n, r, c
        self.matrices, self.current_matrix = [], 0
        self.ask_matrix_values()

    # ---------------- Ingreso de valores ----------------
    def ask_matrix_values(self):
        self.clear_main()
        ttk.Label(self.main_frame, text=f"Matriz {self.current_matrix+1} de {self.num_matrices}",
                  font=("Segoe UI", 14, "bold"), background="#ffe4e6", foreground="#b91c1c").pack(pady=8)

        grid_frame = ttk.Frame(self.main_frame)
        grid_frame.pack(pady=6)

        self.entries = []
        for i in range(self.rows):
            row_entries = []
            for j in range(self.cols):
                e = tk.Entry(grid_frame, width=8, justify="center", font=("Segoe UI", 12), bg="#fff0f5")
                e.grid(row=i, column=j, padx=4, pady=4)
                row_entries.append(e)
            self.entries.append(row_entries)

        btn_frame = ttk.Frame(self.main_frame)
        btn_frame.pack(pady=10)

        if self.current_matrix > 0:
            ttk.Button(btn_frame, text="Anterior", command=self.go_previous).grid(row=0, column=0, padx=6)

        ttk.Button(btn_frame, text="Confirmar Matriz", style="Primary.TButton",
                   command=self.save_matrix).grid(row=0, column=1, padx=6)

        self.error_label = ttk.Label(self.main_frame, text="", foreground="red", background="#ffe4e6")
        self.error_label.pack(pady=6)
        self.add_back_button(self.main_frame)

    def go_previous(self):
        self.current_matrix -= 1
        self.ask_matrix_values()

    def save_matrix(self):
        try:
            mat = []
            for i in range(self.rows):
                fila = []
                for j in range(self.cols):
                    val = self._parse_fraction(self.entries[i][j].get())
                    fila.append(val)
                mat.append(fila)
            if self.current_matrix < len(self.matrices):
                self.matrices[self.current_matrix] = mat
            else:
                self.matrices.append(mat)
        except Exception as e:
            self.error_label.config(text=f"Error en los datos: {e}")
            return

        if self.current_matrix + 1 < self.num_matrices:
            self.current_matrix += 1
            self.ask_matrix_values()
        else:
            self.show_result()

    # ---------------- Resultado ----------------
    def show_result(self):
        self.clear_main()
        ttk.Label(self.main_frame, text="Resumen de matrices ingresadas",
                  font=("Segoe UI", 16, "bold"),
                  background="#ffe4e6", foreground="#b91c1c").pack(pady=10)

        # Contenedor centrado para matrices
        center_frame = ttk.Frame(self.main_frame)
        center_frame.pack(pady=10)

        for idx, mat in enumerate(self.matrices, start=1):
            ttk.Label(center_frame, text=f"Matriz {idx}", font=("Segoe UI", 12, "bold"),
                      background="#ffe4e6", foreground="#7f1d1d").pack(pady=4)
            self._display_matrix(center_frame, mat)

        # Botones debajo
        btns = ttk.Frame(self.main_frame)
        btns.pack(pady=15)
        ttk.Button(btns, text="Calcular suma", style="Primary.TButton",
                   command=self.calculate_sum).grid(row=0, column=0, padx=8)
        ttk.Button(btns, text="Reiniciar", style="Back.TButton",
                   command=self.ask_num_and_dimensions).grid(row=0, column=1, padx=8)

        self.add_back_button(self.main_frame)

    def calculate_sum(self):
        result = [[sum(m[i][j] for m in self.matrices) for j in range(self.cols)] for i in range(self.rows)]

        ttk.Label(self.main_frame, text="Matriz resultante",
                  font=("Segoe UI", 14, "bold"),
                  background="#ffe4e6", foreground="#b91c1c").pack(pady=10)

        self._display_matrix(self.main_frame, result)

        ttk.Label(self.main_frame, text="Detalle de la suma por posición",
                  font=("Segoe UI", 13, "bold"),
                  background="#ffe4e6", foreground="#7f1d1d").pack(pady=8)

        self._display_sum_details(self.main_frame, result)

    def _display_matrix(self, parent, matrix):
        frame = ttk.Frame(parent)
        frame.pack(pady=6)
        for i, row in enumerate(matrix):
            for j, val in enumerate(row):
                tk.Label(frame, text=str(val), width=8, font=("Segoe UI", 12),
                         bg="#fff0f5", relief="solid").grid(row=i, column=j, padx=3, pady=3)

    def _display_sum_details(self, parent, result):
        # Marco contenedor con scrollbar
        container = ttk.Frame(parent)
        container.pack(pady=6, fill="both", expand=True)

        # Scrollbar vertical
        scrollbar = ttk.Scrollbar(container)
        scrollbar.pack(side="right", fill="y")

        # Cuadro de texto con scroll
        text_widget = tk.Text(container, wrap="word", height=15, width=100,
                              font=("Segoe UI", 11), bg="#fff0f5")
        text_widget.pack(side="left", fill="both", expand=True)

        # Conectar scroll con el Text
        text_widget.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=text_widget.yview)

        # Insertar detalle de la suma
        for i in range(self.rows):
            for j in range(self.cols):
                parts = " + ".join(str(m[i][j]) for m in self.matrices)
                expr = f"[{i+1},{j+1}]: {parts} = {result[i][j]}\n"
                text_widget.insert("end", expr)

        # Hacer que el texto sea solo lectura
        text_widget.config(state="disabled")



# ============================================================
# CLASE: RestaMatricesApp (CON MEJORAS DE RESUMEN Y DETALLE)
# ============================================================

class RestaMatricesApp:
    def __init__(self, root, volver_callback):
        self.root = root
        self.volver_callback = volver_callback

        self.root.title("Resta de Matrices")
        self.root.geometry("900x700")
        self.root.configure(bg="#ffe4e6")

        style = ttk.Style()
        try:
            style.theme_use("clam")
        except Exception:
            pass
        style.configure("TLabel", font=("Segoe UI", 12), background="#ffe4e6", foreground="#b91c1c")
        style.configure("Primary.TButton", font=("Segoe UI", 12, "bold"), padding=8,
                        background="#fbb6ce", foreground="#fff")
        style.map("Primary.TButton",
                  background=[("!disabled", "#fbb6ce"), ("active", "#f472b6")],
                  foreground=[("!disabled", "white"), ("active", "white")])
        style.configure("Back.TButton", font=("Segoe UI", 12, "bold"), padding=6,
                        background="#fecaca", foreground="#b91c1c")
        style.map("Back.TButton",
                  background=[("!disabled", "#fecaca"), ("active", "#fca5a5")],
                  foreground=[("!disabled", "#b91c1c"), ("active", "#7f1d1d")])

        self.num_matrices = 0
        self.rows = 0
        self.cols = 0
        self.matrices = []
        self.current_matrix = 0
        self.entries = []

        self.main_frame = ttk.Frame(self.root, padding=12)
        self.main_frame.pack(fill="both", expand=True)

        self.error_label = None

        self.show_welcome()

    # ---------------- Helpers ----------------
    def clear_main(self):
        for w in self.main_frame.winfo_children():
            w.destroy()

    def add_back_button(self, parent_frame=None):
        container = parent_frame if parent_frame is not None else self.main_frame
        back = ttk.Button(container, text="Volver al inicio", style="Back.TButton",
                          command=self._volver_al_inicio)
        back.pack(side="bottom", pady=8)

    def _volver_al_inicio(self):
        try:
            self.volver_callback()
        except Exception:
            pass
        finally:
            try:
                self.root.destroy()
            except Exception:
                pass

    def _parse_fraction(self, s):
        s = s.strip()
        if s == "":
            raise ValueError("Vacío")
        s = s.replace(",", ".")
        return Fraction(s)

    # ---------------- Pantalla bienvenida ----------------
    def show_welcome(self):
        self.clear_main()
        ttk.Label(self.main_frame, text="Resta de Matrices", font=("Segoe UI", 18, "bold"),
                  background="#ffe4e6", foreground="#b91c1c").pack(pady=12)
        ttk.Label(self.main_frame, text="Resta hasta N matrices con las mismas dimensiones",
                  font=("Segoe UI", 12), background="#ffe4e6", foreground="#7f1d1d").pack(pady=6)

        start_btn = ttk.Button(self.main_frame, text="Comenzar", style="Primary.TButton",
                               command=self.ask_num_and_dimensions)
        start_btn.pack(pady=20)
        self.add_back_button(self.main_frame)

    # ---------------- Configuración ----------------
    def ask_num_and_dimensions(self):
        self.clear_main()
        ttk.Label(self.main_frame, text="Configuración - Cantidad y dimensiones", font=("Segoe UI", 14, "bold"),
                  background="#ffe4e6", foreground="#b91c1c").pack(pady=10)

        frame = ttk.Frame(self.main_frame, padding=8)
        frame.pack(pady=8)

        ttk.Label(frame, text="¿Cuántas matrices deseas restar?", background="#ffe4e6").grid(row=0, column=0, padx=6, pady=6, sticky="w")
        self.num_var = tk.StringVar()
        tk.Entry(frame, textvariable=self.num_var, width=6, font=("Segoe UI", 12), bg="#fff0f5").grid(row=0, column=1, padx=6, pady=6)

        ttk.Label(frame, text="Filas:", background="#ffe4e6").grid(row=1, column=0, padx=6, pady=6, sticky="w")
        self.row_var = tk.StringVar()
        tk.Entry(frame, textvariable=self.row_var, width=6, font=("Segoe UI", 12), bg="#fff0f5").grid(row=1, column=1, padx=6, pady=6)

        ttk.Label(frame, text="Columnas:", background="#ffe4e6").grid(row=1, column=2, padx=6, pady=6, sticky="w")
        self.col_var = tk.StringVar()
        tk.Entry(frame, textvariable=self.col_var, width=6, font=("Segoe UI", 12), bg="#fff0f5").grid(row=1, column=3, padx=6, pady=6)

        ttk.Button(self.main_frame, text="Siguiente", style="Primary.TButton",
                   command=self.save_num_and_dimensions).pack(pady=12)

        self.error_label = ttk.Label(self.main_frame, text="", foreground="red", background="#ffe4e6")
        self.error_label.pack()
        self.add_back_button(self.main_frame)

    def save_num_and_dimensions(self):
        try:
            n = int(self.num_var.get())
            r = int(self.row_var.get())
            c = int(self.col_var.get())
            if n < 2 or r <= 0 or c <= 0:
                raise ValueError
        except Exception:
            messagebox.showerror("Error", "Ingresa números válidos (mínimo 2 matrices, dimensiones > 0)")
            return
        self.num_matrices, self.rows, self.cols = n, r, c
        self.matrices, self.current_matrix = [], 0
        self.ask_matrix_values()

    # ---------------- Ingreso de valores ----------------
    def ask_matrix_values(self):
        self.clear_main()
        ttk.Label(self.main_frame, text=f"Matriz {self.current_matrix+1} de {self.num_matrices}",
                  font=("Segoe UI", 14, "bold"), background="#ffe4e6", foreground="#b91c1c").pack(pady=8)

        grid_frame = ttk.Frame(self.main_frame)
        grid_frame.pack(pady=6)

        self.entries = []
        for i in range(self.rows):
            row_entries = []
            for j in range(self.cols):
                e = tk.Entry(grid_frame, width=8, justify="center", font=("Segoe UI", 12), bg="#fff0f5")
                e.grid(row=i, column=j, padx=4, pady=4)
                row_entries.append(e)
            self.entries.append(row_entries)

        btn_frame = ttk.Frame(self.main_frame)
        btn_frame.pack(pady=10)

        if self.current_matrix > 0:
            ttk.Button(btn_frame, text="Anterior", command=self.go_previous).grid(row=0, column=0, padx=6)

        ttk.Button(btn_frame, text="Confirmar Matriz", style="Primary.TButton",
                   command=self.save_matrix).grid(row=0, column=1, padx=6)

        self.error_label = ttk.Label(self.main_frame, text="", foreground="red", background="#ffe4e6")
        self.error_label.pack(pady=6)
        self.add_back_button(self.main_frame)

    def go_previous(self):
        self.current_matrix -= 1
        self.ask_matrix_values()

    def save_matrix(self):
        try:
            mat = []
            for i in range(self.rows):
                fila = []
                for j in range(self.cols):
                    val = self._parse_fraction(self.entries[i][j].get())
                    fila.append(val)
                mat.append(fila)
            if self.current_matrix < len(self.matrices):
                self.matrices[self.current_matrix] = mat
            else:
                self.matrices.append(mat)
        except Exception as e:
            self.error_label.config(text=f"Error en los datos: {e}")
            return

        if self.current_matrix + 1 < self.num_matrices:
            self.current_matrix += 1
            self.ask_matrix_values()
        else:
            self.show_result()

    # ---------------- Resultado ----------------
    def show_result(self):
        self.clear_main()
        ttk.Label(self.main_frame, text="Resumen de matrices ingresadas",
                  font=("Segoe UI", 16, "bold"),
                  background="#ffe4e6", foreground="#b91c1c").pack(pady=10)

        center_frame = ttk.Frame(self.main_frame)
        center_frame.pack(pady=10)

        for idx, mat in enumerate(self.matrices, start=1):
            ttk.Label(center_frame, text=f"Matriz {idx}", font=("Segoe UI", 12, "bold"),
                      background="#ffe4e6", foreground="#7f1d1d").pack(pady=4)
            self._display_matrix(center_frame, mat)

        btns = ttk.Frame(self.main_frame)
        btns.pack(pady=15)
        ttk.Button(btns, text="Calcular resta", style="Primary.TButton",
                   command=self.calculate_subtraction).grid(row=0, column=0, padx=8)
        ttk.Button(btns, text="Reiniciar", style="Back.TButton",
                   command=self.ask_num_and_dimensions).grid(row=0, column=1, padx=8)

        self.add_back_button(self.main_frame)

    def calculate_subtraction(self):
        result = [[self.matrices[0][i][j] - sum(self.matrices[k][i][j] for k in range(1, self.num_matrices))
                   for j in range(self.cols)] for i in range(self.rows)]

        ttk.Label(self.main_frame, text="Matriz resultante",
                  font=("Segoe UI", 14, "bold"),
                  background="#ffe4e6", foreground="#b91c1c").pack(pady=10)

        self._display_matrix(self.main_frame, result)

        ttk.Label(self.main_frame, text="Detalle de la resta por posición",
                  font=("Segoe UI", 13, "bold"),
                  background="#ffe4e6", foreground="#7f1d1d").pack(pady=8)

        self._display_subtraction_details(self.main_frame, result)

    def _display_matrix(self, parent, matrix):
        frame = ttk.Frame(parent)
        frame.pack(pady=6)
        for i, row in enumerate(matrix):
            for j, val in enumerate(row):
                tk.Label(frame, text=str(val), width=8, font=("Segoe UI", 12),
                         bg="#fff0f5", relief="solid").grid(row=i, column=j, padx=3, pady=3)

    def _display_subtraction_details(self, parent, result):
        # Contenedor con scrollbar
        container = tk.Frame(parent)
        container.pack(fill="both", expand=True, pady=5)
        canvas = tk.Canvas(container, bg="#ffe4e6", height=200)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        frame = tk.Frame(canvas, bg="#ffe4e6")
        canvas.create_window((0,0), window=frame, anchor='nw')

        for i in range(self.rows):
            for j in range(self.cols):
                parts = " - ".join(str(self.matrices[k][i][j]) for k in range(self.num_matrices))
                expr = f"[{i+1},{j+1}]: {parts} = {result[i][j]}"
                ttk.Label(frame, text=expr,
                          background="#ffe4e6", foreground="#333",
                          font=("Segoe UI", 11)).pack(anchor="w", pady=2)



# ============================================================
# CLASE: MultiplicacionMatricesApp

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


# ============================================================
# INICIO DEL PROGRAMA
# ============================================================
if __name__ == "__main__":
    root = tk.Tk()
    MenuPrincipal(root)
    root.mainloop()