import tkinter as tk
from tkinter import ttk, messagebox
from models import cursos as model
from ui.utils_style import aplicar_estilo_global
from ui.utils_treeview import auto_ajustar_columnas, ajustar_tamano_ventana
from ui.detalle_curso_window import DetalleCursoWindow


class CursosWindow(tk.Toplevel):
    def __init__(self, parent, modo="claro"):
        super().__init__(parent)
        self.modo = modo
        self.style, self.bg_color = aplicar_estilo_global(modo)
        self.configure(bg=self.bg_color)
        self.title("Gestión de cursos")
        self.geometry("1100x600")
        self.resizable(True, True)
        self.transient(parent)
        self.grab_set()
        self.focus_set()
        # === Frame contenedor de la tabla ===
        frame_tabla = tk.Frame(self, bg=self.bg_color)
        frame_tabla.pack(fill="both", expand=True, padx=10, pady=10)
        # === Tabla ===
        self.tree = ttk.Treeview(
            frame_tabla,
            columns=(
                "codigo_curso", "nombre", "fecha_inicio", "fecha_fin",
                "lugar", "modalidad", "horas", "responsable"
            ),
            show="headings",
            height=15
        )
        self.tree.bind("<Double-1>", self.ver_detalle_curso)
        columnas = [
            ("codigo_curso", "Código", 100),
            ("nombre", "Nombre", 200),
            ("fecha_inicio", "Inicio", 100),
            ("fecha_fin", "Fin", 100),
            ("lugar", "Lugar", 120),
            ("modalidad", "Modalidad", 100),
            ("horas", "Horas", 60),
            ("responsable", "Responsable", 150)
        ]
        for col, texto, ancho in columnas:
            self.tree.heading(col, text=texto, anchor="center")
            anchor = "center" if col in ("codigo_curso", "fecha_inicio", "fecha_fin", "horas") else "w"
            self.tree.column(col, width=ancho, anchor=anchor)
        # === Barras de desplazamiento ===
        scroll_y = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tree.yview)
        scroll_x = ttk.Scrollbar(frame_tabla, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        # Posicionamiento con grid
        self.tree.grid(row=0, column=0, sticky="nsew")
        scroll_y.grid(row=0, column=1, sticky="ns")
        scroll_x.grid(row=1, column=0, sticky="ew")
        # Permitir expansión del frame
        frame_tabla.grid_rowconfigure(0, weight=1)
        frame_tabla.grid_columnconfigure(0, weight=1)
        # === Botones inferiores ===
        frame_btns = tk.Frame(self, bg=self.bg_color)
        frame_btns.pack(pady=10)
        ttk.Button(frame_btns, text="Actualizar lista", command=self.cargar_datos).grid(row=0, column=0, padx=5)
        ttk.Button(frame_btns, text="Añadir curso", command=self.ventana_nuevo_curso).grid(row=0, column=1, padx=5)
        ttk.Button(frame_btns, text="Eliminar seleccionado", command=self.eliminar_seleccionado).grid(row=0, column=2, padx=5)
        self.cargar_datos()

    # === Cargar datos en tabla ===
    def cargar_datos(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        cursos = model.obtener_cursos()
        for curso in cursos:
            self.tree.insert("", tk.END, values=curso)
        auto_ajustar_columnas(self.tree)
        ajustar_tamano_ventana(self.tree, self)

    # === Eliminar curso seleccionado ===
    def eliminar_seleccionado(self):
        item = self.tree.selection()
        if not item:
            messagebox.showwarning("Aviso", "Selecciona un curso para eliminar.")
            return
        curso = self.tree.item(item, "values")
        codigo_curso = curso[0]
        confirmar = messagebox.askyesno("Confirmar", f"¿Eliminar el curso {curso[1]}?")
        if confirmar:
            model.eliminar_curso(codigo_curso)
            self.cargar_datos()

    # === Ventana nuevo curso ===
    def ventana_nuevo_curso(self):
        win = tk.Toplevel(self)
        win.title("Nuevo curso")
        win.geometry("400x400")

        campos = [
            "codigo_curso", "nombre", "fecha_inicio", "fecha_fin",
            "lugar", "modalidad", "horas", "responsable"
        ]
        self.entries = {}
        for i, campo in enumerate(campos):
            ttk.Label(win, text=campo.replace("_", " ").capitalize()).grid(row=i, column=0, sticky="w", padx=10, pady=5)
            entry = ttk.Entry(win)
            entry.grid(row=i, column=1, padx=10, pady=5)
            self.entries[campo] = entry

        ttk.Button(win, text="Guardar", command=lambda: self.guardar_curso(win)).grid(row=len(campos), columnspan=2, pady=10)

    # === Guardar curso ===
    def guardar_curso(self, ventana):
        datos = [self.entries[c].get() for c in self.entries]
        if not all(datos):
            messagebox.showerror("Error", "Rellena todos los campos.")
            return
        try:
            model.crear_curso(*datos)
            messagebox.showinfo("Éxito", "Curso añadido correctamente.")
            ventana.destroy()
            self.cargar_datos()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # === Doble click: abrir detalle ===
    def ver_detalle_curso(self, event):
        selection = self.tree.selection()
        if not selection:
            return
        item = self.tree.item(selection[0])
        codigo_curso = item["values"][0]
        DetalleCursoWindow(self, codigo_curso, modo=self.modo)
