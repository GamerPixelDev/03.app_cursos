import tkinter as tk
from tkinter import ttk, messagebox
from models import matriculas as model


class BuscarAlumnoWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Buscar alumno")
        self.geometry("800x400")
        # --- Campo de búsqueda ---
        frame_buscar = tk.Frame(self)
        frame_buscar.pack(pady=10)
        tk.Label(frame_buscar, text="NIF del alumno:").grid(row=0, column=0, padx=5)
        self.entry_nif = tk.Entry(frame_buscar, width=20)
        self.entry_nif.grid(row=0, column=1, padx=5)
        tk.Button(frame_buscar, text="Buscar", command=self.buscar).grid(row=0, column=2, padx=5)
        # --- Tabla de resultados ---
        self.tree = ttk.Treeview(self, columns=("codigo", "nombre", "inicio", "fin", "estado"),
                                    show="headings", height=15)
        columnas = [
            ("codigo", "Código curso", 120),
            ("nombre", "Nombre del curso", 200),
            ("inicio", "Inicio", 100),
            ("fin", "Fin", 100),
            ("estado", "Estado", 100)
        ]
        for col, texto, ancho in columnas:
            self.tree.heading(col, text=texto)
            self.tree.column(col, width=ancho)
        self.tree.pack(fill=tk.BOTH, expand=True, pady=10)
        self.transient(parent)
        self.grab_set()
        self.focus_set()
    # --- Función de búsqueda ---
    def buscar(self):
        nif = self.entry_nif.get().strip()
        if not nif:
            messagebox.showwarning("Aviso", "Introduce el NIF del alumno.")
            return
        cursos = model.obtener_cursos_por_alumno(nif)
        for row in self.tree.get_children():
            self.tree.delete(row)
        if not cursos:
            messagebox.showinfo("Resultado", "No se encontraron cursos para este alumno.")
            return
        for curso in cursos:
            self.tree.insert("", tk.END, values=curso)
