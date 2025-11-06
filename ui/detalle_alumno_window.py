import tkinter as tk
from tkinter import ttk, messagebox
from models import matriculas, alumnos
from ui.utils_style import aplicar_estilo_global
from ui.utils_treeview import auto_ajustar_columnas  # si ya tienes esta utilidad

class DetalleAlumnoWindow(tk.Toplevel):
    def __init__(self, parent, nif, modo="claro"):
        super().__init__(parent)
        # === Estilo y configuración ===
        self.style, self.bg_color = aplicar_estilo_global(modo)
        self.configure(bg=self.bg_color)
        self.title(f"Cursos de alumno {nif}")
        self.geometry("800x500")
        self.resizable(True, True)
        self.transient(parent)
        self.grab_set()
        # === Obtener datos del alumno ===
        alumno = alumnos.obtener_datos_alumno(nif)
        if alumno:
            nombre_completo = f"{alumno[0]} {alumno[1]}"
        else:
            nombre_completo = "(Nombre no encontrado)"
        # === Encabezado ===
        label = tk.Label(
            self,
            text=f"Alumno: {nombre_completo}  |  NIF: {nif}",
            font=("Segoe UI", 11, "bold"),
            fg="#3E64FF",
            bg=self.bg_color
        )
        label.pack(pady=10)
        # === Frame principal ===
        frame = tk.Frame(self, bg=self.bg_color)
        frame.pack(fill="both", expand=True, padx=10, pady=10)
        # === Tabla (Treeview) ===
        self.tree = ttk.Treeview(
            frame,
            columns=("codigo", "nombre", "fecha", "modalidad", "horas"),
            show="headings",
            height=15
        )
        columnas = [
            ("codigo", "Código Curso", 100, "center"),
            ("nombre", "Nombre del Curso", 250, "w"),
            ("fecha", "Fecha Matrícula", 120, "center"),
            ("modalidad", "Modalidad", 120, "center"),
            ("horas", "Horas", 80, "center")
        ]
        for col, texto, ancho, align in columnas:
            self.tree.heading(col, text=texto, anchor="center")
            self.tree.column(col, width=ancho, anchor=align)
        scroll_y = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll_y.set)
        scroll_y.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)
        # === Rellenar datos ===
        try:
            cursos = matriculas.obtener_cursos_por_alumno(nif)
            if cursos:
                for c in cursos:
                    self.tree.insert("", "end", values=c)
                auto_ajustar_columnas(self.tree)  # si tienes la función común
            else:
                messagebox.showinfo("Sin cursos", "Este alumno no tiene matrículas registradas.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los cursos: {e}")
