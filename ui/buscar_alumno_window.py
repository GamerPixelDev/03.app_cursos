import tkinter as tk
from tkinter import ttk, messagebox
from ui.utils_style import aplicar_estilo_global
from models import matriculas as model
from models import alumnos
from ui.utils_treeview import auto_ajustar_columnas, ajustar_tamano_ventana

class BuscarAlumnoWindow(tk.Toplevel):
    def __init__(self, parent, modo="claro"):
        super().__init__(parent)
        # === Estilo y configuración ===
        self.modo = modo
        self.style, self.bg_color = aplicar_estilo_global(modo)
        self.configure(bg=self.bg_color)
        self.title("Buscar alumno")
        self.geometry("850x500")
        self.resizable(True, True)
        self.transient(parent)
        self.grab_set()
        self.focus_set()
        # === Frame de búsqueda ===
        frame_buscar = tk.Frame(self, bg=self.bg_color)
        frame_buscar.pack(pady=10)
        tk.Label(
            frame_buscar,
            text="NIF del alumno:",
            font=("Segoe UI", 10),
            bg=self.bg_color
        ).grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.entry_nif = ttk.Entry(frame_buscar, width=20)
        self.entry_nif.grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(frame_buscar, text="Buscar", command=self.buscar).grid(row=0, column=2, padx=5, pady=5)
        # === Información del alumno ===
        self.frame_info = ttk.LabelFrame(self, text="Datos del alumno")
        self.frame_info.pack(fill="x", padx=10, pady=5)
        self.label_info = tk.Label(
            self.frame_info,
            text="Introduce un NIF y presiona Buscar.",
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
        # === Tabla de resultados ===
        self.tree = ttk.Treeview(
            frame_tabla,
            columns=("codigo", "nombre", "inicio", "fin", "estado"),
            show="headings",
            height=15
        )
        columnas = [
            ("codigo", "Código curso", 120, "center"),
            ("nombre", "Nombre del curso", 250, "w"),
            ("inicio", "Inicio", 100, "center"),
            ("fin", "Fin", 100, "center"),
            ("estado", "Estado", 100, "center")
        ]
        for col, texto, ancho, align in columnas:
            self.tree.heading(col, text=texto, anchor="center")
            self.tree.column(col, width=ancho, anchor=align)
        # === Barras de desplazamiento ===
        scroll_y = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tree.yview)
        scroll_x = ttk.Scrollbar(frame_tabla, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        # Posicionamiento con grid (igual que el resto de ventanas)
        self.tree.grid(row=0, column=0, sticky="nsew")
        scroll_y.grid(row=0, column=1, sticky="ns")
        scroll_x.grid(row=1, column=0, sticky="ew")
        frame_tabla.grid_rowconfigure(0, weight=1)
        frame_tabla.grid_columnconfigure(0, weight=1)

    # === Función de búsqueda ===
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
        nombre, apellidos, localidad, codigo_postal, telefono, email, sexo, edad, estudios, estado_laboral = datos_alumno
        texto_info = (
            f"Nombre: {nombre} {apellidos}\n"
            f"Localidad: {localidad} ({codigo_postal})\n"
            f"Email: {telefono} | Tel: {email}\n"
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
        auto_ajustar_columnas(self.tree)
        ajustar_tamano_ventana(self.tree, self)