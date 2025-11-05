import tkinter as tk
from tkinter import ttk
from models import matriculas

class DetalleAlumnoWindow:
    def __init__(self, master, nif):
        self.top = tk.Toplevel(master)
        self.top.title(f"Cursos de alumno {nif}")
        self.top.geometry("700x400")
        self.top.resizable(False, False)
        label = tk.Label(self.top, text=f"Cursos del alumno con NIF: {nif}", font=("Segoe UI", 11, "bold"))
        label.pack(pady=10)
        frame = tk.Frame(self.top)
        frame.pack(fill="both", expand=True, padx=10, pady=10)
        # Tabla
        self.tree = ttk.Treeview(frame, columns=("codigo", "nombre", "fecha", "modalidad", "horas"), show="headings")
        self.tree.heading("codigo", text="Código Curso")
        self.tree.heading("nombre", text="Nombre del Curso")
        self.tree.heading("fecha", text="Fecha Matrícula")
        self.tree.heading("modalidad", text="Modalidad")
        self.tree.heading("horas", text="Horas")
        self.tree.pack(fill="both", expand=True)
        # Rellenar datos
        cursos = matriculas.obtener_cursos_por_alumno(nif)
        for c in cursos:
            self.tree.insert("", "end", values=c)
