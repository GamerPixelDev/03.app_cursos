import tkinter as tk
from tkinter import ttk, messagebox
from ui.utils_style import aplicar_estilo_global
from ui.utils_treeview import auto_ajustar_columnas, ajustar_tamano_ventana
from models import matriculas as model
from models import cursos


class BuscarCursoWindow(tk.Toplevel):
    def __init__(self, parent, modo="claro"):
        super().__init__(parent)
        # === Estilo y configuración ===
        self.modo = modo
        self.style, self.bg_color = aplicar_estilo_global(modo)
        self.configure(bg=self.bg_color)
        self.title("Buscar curso")
        self.geometry("900x500")
        self.resizable(True, True)
        self.transient(parent)
        self.grab_set()
        self.focus_set()
        # === Frame de búsqueda ===
        frame_buscar = tk.Frame(self, bg=self.bg_color)
        frame_buscar.pack(pady=10)
        tk.Label(
            frame_buscar,
            text="Código del curso:",
            font=("Segoe UI", 10),
            bg=self.bg_color
        ).grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.entry_codigo = ttk.Entry(frame_buscar, width=20)
        self.entry_codigo.grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(frame_buscar, text="Buscar", command=self.buscar).grid(row=0, column=2, padx=5, pady=5)
        # === Información del curso ===
        self.frame_info = ttk.LabelFrame(self, text="Datos del curso")
        self.frame_info.pack(fill="x", padx=10, pady=5)
        self.label_info = tk.Label(
            self.frame_info,
            text="Introduce un código de curso y presiona Buscar.",
            justify="left",
            anchor="w",
            bg="white",
            fg="#333",
            font=("Segoe UI", 9),
            relief="solid",
            bd=1
        )
        self.label_info.pack(fill="x", padx=5, pady=5)
        # === Frame para tabla ===
        frame_tabla = tk.Frame(self, bg=self.bg_color)
        frame_tabla.pack(fill="both", expand=True, padx=10, pady=10)
        # === Tabla de alumnos ===
        self.tree = ttk.Treeview(
            frame_tabla,
            columns=("nif", "alumno", "telefono", "email", "estado"),
            show="headings",
            height=15
        )
        columnas = [
            ("nif", "NIF", 100, "center"),
            ("alumno", "Alumno", 200, "w"),
            ("telefono", "Teléfono", 150, "center"),
            ("email", "Email", 200, "w"),
            ("estado", "Estado del curso", 150, "center")
        ]
        for col, texto, ancho, align in columnas:
            self.tree.heading(col, text=texto, anchor="center")
            self.tree.column(col, width=ancho, anchor=align)
        # === Barras de desplazamiento ===
        scroll_y = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tree.yview)
        scroll_x = ttk.Scrollbar(frame_tabla, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        # Posicionamiento con grid
        self.tree.grid(row=0, column=0, sticky="nsew")
        scroll_y.grid(row=0, column=1, sticky="ns")
        scroll_x.grid(row=1, column=0, sticky="ew")
        frame_tabla.grid_rowconfigure(0, weight=1)
        frame_tabla.grid_columnconfigure(0, weight=1)

    # === Buscar curso ===
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
        alumnos_curso = model.obtener_alumnos_por_curso(codigo)
        if not alumnos_curso:
            messagebox.showinfo("Alumnos", "Este curso no tiene alumnos matriculados.")
            return
        for alumno in alumnos_curso:
            self.tree.insert("", tk.END, values=alumno)
        auto_ajustar_columnas(self.tree)
        ajustar_tamano_ventana(self.tree, self)
