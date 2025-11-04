import tkinter as tk
from tkinter import ttk, messagebox
from models import matriculas as model
from models import alumnos
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
        # --- Información del alumno ---
        self.frame_info = tk.LabelFrame(self, text="Datos del alumno", padx=10, pady=5)
        self.frame_info.pack(fill="x", padx=10, pady=5)
        self.label_info = tk.Label(self.frame_info, text="", justify="left", anchor="w")
        self.label_info.pack(fill="x")
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
        # Limpiar tabla y datos previos
        for row in self.tree.get_children():
            self.tree.delete(row)
        self.label_info.config(text="")
        # --- Obtener datos del alumno ---
        datos_alumno = alumnos.obtener_datos_alumno(nif)
        if not datos_alumno:
            messagebox.showinfo("Resultado", "No se encontró ningún alumno con ese NIF.")
            return
        nombre, apellidos, localidad, codigo_postal, correo, telefono, sexo, edad, estudios, estado_laboral = datos_alumno
        texto_info = (
            f"Nombre: {nombre} {apellidos}\n"
            f"Localidad: {localidad} ({codigo_postal})\n"
            f"Correo: {correo} | Tel: {telefono}\n"
            f"Sexo: {sexo} | Edad: {edad}\n"
            f"Estudios: {estudios}\n"
            f"Estado laboral: {estado_laboral}"
        )
        self.label_info.config(text=texto_info)
        # --- Obtener cursos del alumno ---
        cursos = model.obtener_cursos_por_alumno(nif)
        if not cursos:
            messagebox.showinfo("Cursos", "Este alumno no tiene cursos registrados.")
            return
        for curso in cursos:
            self.tree.insert("", tk.END, values=curso)

