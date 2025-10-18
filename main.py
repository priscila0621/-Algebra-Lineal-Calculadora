"""
Punto de entrada de la app.
Si PySide6 está disponible, se usa la interfaz Qt (más moderna).
Si no, se usa la interfaz Tk existente como respaldo.
"""


def _run_qt():
    from qt_app.main_qt import run
    run()


def _run_tk():
    import tkinter as tk
    from menu_principal import MenuPrincipal
    root = tk.Tk()
    MenuPrincipal(root)
    root.mainloop()


if __name__ == "__main__":
    try:
        import PySide6  # noqa: F401
        _run_qt()
    except Exception:
        _run_tk()

