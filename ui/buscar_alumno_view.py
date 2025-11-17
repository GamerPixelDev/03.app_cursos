import tkinter as tk
from tkinter import ttk, messagebox
from models import alumnos
from ui.utils_style import aplicar_estilo_global
from ui.utils_treeview import auto_ajustar_columnas

class BuscarAlumnoView(tk.Frame):
    def __init__(self, parent, modo="claro"):
        super().__init__(parent)
        self.modo = modo
        self.style, self.bg_color = aplicar_estilo_global(modo)
        self.configure(bg=self.bg_color)
        # ==== TITULO ====
        tk.Label(
            self,
            text="🔎 Buscar alumno",
            bg=self.bg_color,
            fg="#3E64FF",
            font=("Segoe UI", 16, "bold")
        ).pack(pady=10)
        # ==== CAMPO DE BÚSQUEDA ====
        frame_buscar = tk.Frame(self, bg=self.bg_color)
        frame_buscar.pack(pady=10)
        tk.Label(
            frame_buscar,
            text="Buscar:",
            bg=self.bg_color,
            font=("Segoe UI", 11)
        ).grid(row=0, column=0, padx=5)
        self.entry_buscar = ttk.Entry(frame_buscar, width=40)
        self.entry_buscar.grid(row=0, column=1, padx=5)
        self.entry_buscar.bind("<Return>", lambda e: self.buscar())
        ttk.Button(
            frame_buscar,
            text="Buscar",
            command=self.buscar
        ).grid(row=0, column=2, padx=5)
        # ==== RESULTADOS ====
        self.tree = ttk.Treeview(
            self,
            columns=("nif", "nombre", "apellidos", "telefono", "email"),
            show="headings",
            height=12
        )
        columnas = [
            ("nif", "NIF", 100),
            ("nombre", "Nombre", 150),
            ("apellidos", "Apellidos", 200),
            ("telefono", "Teléfono", 120),
            ("email", "Email", 200)
        ]
        for col, texto, ancho in columnas:
            self.tree.heading(col, text=texto)
            self.tree.column(col, width=ancho)
        self.tree.pack(padx=10, pady=10, fill="both", expand=True)

    # ==== BUSCAR ====
    def buscar(self):
        texto = self.entry_buscar.get().strip().lower()
        if not texto:
            messagebox.showwarning("Aviso", "Introduce algo para buscar.")
            return
        # Vaciar tabla
        for row in self.tree.get_children():
            self.tree.delete(row)
        datos = alumnos.obtener_alumnos()
        # Filtrado básico
        resultados = [
            a for a in datos
            if texto in a[0].lower()  # NIF
            or texto in a[1].lower()  # Nombre
            or texto in a[2].lower()  # Apellidos
        ]
        if not resultados:
            messagebox.showinfo("Sin resultados", "No se encontraron alumnos.")
            return
        for r in resultados:
            self.tree.insert("", tk.END, values=(r[0], r[1], r[2], r[6], r[5]))
        auto_ajustar_columnas(self.tree)