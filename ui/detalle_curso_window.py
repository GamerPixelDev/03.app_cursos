import tkinter as tk
from tkinter import ttk, messagebox
from models import matriculas, cursos
from ui.utils_style import aplicar_estilo_global
from ui.utils_treeview import auto_ajustar_columnas, ajustar_tamano_ventana

class DetalleCursoWindow(tk.Toplevel):
    def __init__(self, parent, codigo_curso, modo="claro"):
        super().__init__(parent)
        # === Estilo y configuración ===
        self.style, self.bg_color = aplicar_estilo_global(modo)
        self.configure(bg=self.bg_color)
        self.title(f"Alumnos del curso {codigo_curso}")
        self.geometry("900x500")
        self.resizable(True, True)
        self.transient(parent)
        self.grab_set()
        # === Obtener datos del curso ===
        curso = cursos.obtener_datos_curso(codigo_curso)
        if curso:
            nombre_curso = curso[0]
            modalidad = curso[4] if len(curso) > 1 else "N/A"
            lugar = curso[2] if len(curso) > 2 else "N/A"
        else:
            nombre_curso = "(Curso no encontrado)"
            modalidad = ""
            lugar = ""
        # === Encabezado ===
        label = tk.Label(
            self,
            text=f"Curso: {nombre_curso}  |  Código: {codigo_curso}",
            font=("Segoe UI", 11, "bold"),
            fg="#3E64FF",
            bg=self.bg_color
        )
        label.pack(pady=(10, 3))

        sublabel = tk.Label(
            self,
            text=f"Modalidad: {modalidad}  |  Lugar: {lugar}",
            font=("Segoe UI", 10),
            bg=self.bg_color
        )
        sublabel.pack(pady=(0, 6))
        # === Contador de alumnos (ahora debajo del detalle del curso) ===
        try:
            alumnos_curso = matriculas.obtener_alumnos_por_curso(codigo_curso)
            total = len(alumnos_curso) if alumnos_curso else 0
            lbl_total = tk.Label(
                self,
                text=f"👥 Total de alumnos matriculados: {total}",
                font=("Segoe UI", 10, "italic"),
                bg=self.bg_color,
                fg="#333333"
            )
            lbl_total.pack(pady=(0, 10))
        except Exception:
            lbl_total = tk.Label(
                self,
                text="👥 Total de alumnos matriculados: Error al obtener datos",
                font=("Segoe UI", 10, "italic"),
                bg=self.bg_color,
                fg="#333333"
            )
            lbl_total.pack(pady=(0, 10))
            alumnos_curso = []
        # === Frame principal ===
        frame = tk.Frame(self, bg=self.bg_color)
        frame.pack(fill="both", expand=True, padx=10, pady=10)
        # === Tabla (Treeview) ===
        self.tree = ttk.Treeview(
            frame,
            columns=("nif", "nombre", "apellidos", "fecha_matricula"),
            show="headings",
            height=15
        )
        columnas = [
            ("nif", "NIF", 100, "center"),
            ("nombre", "Nombre", 150, "w"),
            ("apellidos", "Apellidos", 180, "w"),
            ("fecha_matricula", "Fecha Matrícula", 120, "center")
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
            alumnos_curso = matriculas.obtener_alumnos_por_curso(codigo_curso)
            if alumnos_curso:
                for a in alumnos_curso:
                    self.tree.insert("", "end", values=a)
                try:
                    auto_ajustar_columnas(self.tree)
                    ajustar_tamano_ventana(self.tree, self)
                except Exception as e:
                    print("Error ajustando ventana:", e)
            else:
                messagebox.showinfo("Sin alumnos", "Este curso no tiene alumnos matriculados.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los alumnos: {e}")