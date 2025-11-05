import tkinter as tk
from tkinter import ttk
from models import matriculas, alumnos

class DetalleAlumnoWindow:
    def __init__(self, master, nif):
        self.top = tk.Toplevel(master)
        self.top.title(f"Cursos de alumno {nif}")
        self.top.geometry("750x450")
        self.top.resizable(False, False)
        # Obtener los datos del alumno
        alumno = alumnos.obtener_datos_alumno(nif)
        if alumno:
            nombre_completo = f"{alumno[0]} {alumno[1]}"
        else:
            nombre_completo = "(Nombre no encontrado)"
        label = tk.Label(
            self.top,
            text=f"Alumno: {nombre_completo}  |  NIF: {nif}",
            font=("Segoe UI", 11, "bold"),
            fg="#3E64FF"
        )
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
        self.tree.column("codigo", width=100)
        self.tree.column("nombre", width=230)
        self.tree.column("fecha", width=120, anchor="center")
        self.tree.column("modalidad", width=100, anchor="center")
        self.tree.column("horas", width=80, anchor="center")
        self.tree.pack(fill="both", expand=True)
        # Rellenar datos
        cursos = matriculas.obtener_cursos_por_alumno(nif)
        for c in cursos:
            self.tree.insert("", "end", values=c)
