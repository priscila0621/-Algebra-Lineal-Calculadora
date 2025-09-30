import tkinter as tk
from tkinter import ttk, messagebox
from suma_matrices_app import SumaMatricesApp
from resta_matrices_app import RestaMatricesApp
from multiplicacion_matrices_app import MultiplicacionMatricesApp


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