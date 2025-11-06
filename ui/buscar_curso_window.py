import tkinter as tk
from tkinter import ttk, messagebox
from ui.utils_style import aplicar_estilo_global
from models import matriculas as model
from models import cursos


class BuscarCursoWindow(tk.Toplevel):
    def __init__(self, parent, modo="claro"):
        super().__init__(parent)
        self.style, self.bg_color = aplicar_estilo_global(modo)
        self.configure(bg=self.bg_color)
        self.title("Buscar curso")
        self.geometry("850x450")
        # --- Campo de búsqueda ---
        frame_buscar = tk.Frame(self)
        frame_buscar.pack(pady=10)
        tk.Label(frame_buscar, text="Código del curso:").grid(row=0, column=0, padx=5)
        self.entry_codigo = tk.Entry(frame_buscar, width=20)
        self.entry_codigo.grid(row=0, column=1, padx=5)
        ttk.Button(frame_buscar, text="Buscar", command=self.buscar).grid(row=0, column=2, padx=5)
        # --- Información del curso ---
        self.frame_info = tk.LabelFrame(self, text="Datos del curso", padx=10, pady=5)
        self.frame_info.pack(fill="x", padx=10, pady=5)
        self.label_info = tk.Label(self.frame_info, text="", justify="left", anchor="w")
        self.label_info.pack(fill="x")
        # --- Tabla de alumnos ---
        self.tree = ttk.Treeview(self, columns=("nif", "alumno", "telefono", "email", "estado"),
                                    show="headings", height=15)
        columnas = [
            ("nif", "NIF", 100),
            ("alumno", "Alumno", 200),
            ("telefono", "Teléfono", 200),
            ("email", "Email", 100),
            ("estado", "Estado del curso", 120)
        ]
        for col, texto, ancho in columnas:
            self.tree.heading(col, text=texto)
            self.tree.column(col, width=ancho)
        #--- Barras de desplazamiento ---
        scroll_y = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        scroll_x = ttk.Scrollbar(self, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

        scroll_y.pack(side="right", fill="y")
        scroll_x.pack(side="bottom", fill="x")
        self.tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.transient(parent)
        self.grab_set()
        self.focus_set()

    # --- Buscar curso ---
    def buscar(self):
        codigo = self.entry_codigo.get().strip()
        if not codigo:
            messagebox.showwarning("Aviso", "Introduce el código del curso.")
            return
        # Limpiar datos anteriores
        for row in self.tree.get_children():
            self.tree.delete(row)
        self.label_info.config(text="")
        # --- Obtener datos del curso ---
        datos_curso = cursos.obtener_datos_curso(codigo)
        if not datos_curso:
            messagebox.showinfo("Resultado", "No se encontró ningún curso con ese código.")
            return
        nombre, fecha_inicio, fecha_fin, lugar, modalidad, horas, responsable = datos_curso
        texto_info = (
            f"Nombre: {nombre}\n"
            f"Fechas: {fecha_inicio} → {fecha_fin}\n"
            f"Lugar: {lugar}\n"
            f"Modalidad: {modalidad}\n"
            f"Horas: {horas}\n"
            f"Responsable: {responsable}"
        )
        self.label_info.config(text=texto_info)
        # --- Obtener alumnos del curso ---
        alumnos = model.obtener_alumnos_por_curso(codigo)
        if not alumnos:
            messagebox.showinfo("Alumnos", "Este curso no tiene alumnos matriculados.")
            return
        for alumno in alumnos:
            self.tree.insert("", tk.END, values=alumno)
