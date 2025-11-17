import tkinter as tk
from tkinter import ttk, messagebox
from models import alumnos as model
from ui.detalle_alumno_window import DetalleAlumnoWindow
from ui.utils_style import aplicar_estilo_global
from ui.utils_treeview import auto_ajustar_columnas, ajustar_tamano_ventana

class AlumnosView(tk.Frame):
    def __init__(self, parent, modo="claro"):
        super().__init__(parent)
        self.modo = modo
        self.style, self.bg_color = aplicar_estilo_global(modo)
        self.configure(bg=self.bg_color)
        # ===== Título de la vista =====
        lbl_title = tk.Label(
            self,
            text="🎓 Gestión de Alumnos",
            font=("Segoe UI", 16, "bold"),
            fg="#3E64FF",
            bg=self.bg_color
        )
        lbl_title.pack(pady=10)
        # ===== Frame tabla =====
        frame_tabla = tk.Frame(self, bg=self.bg_color)
        frame_tabla.pack(fill="both", expand=True, padx=10, pady=10)
        # ===== Treeview =====
        self.tree = ttk.Treeview(
            frame_tabla,
            columns=(
                "nif", "nombre", "apellidos", "localidad", "codigo_postal",
                "telefono", "email", "sexo", "edad", "estudios", "estado_laboral"
            ),
            show="headings",
            height=15
        )
        self.tree.bind("<Double-1>", self.ver_detalle_alumno)
        columnas = [
            ("nif", "NIF", 80),
            ("nombre", "Nombre", 120),
            ("apellidos", "Apellidos", 150),
            ("localidad", "Localidad", 100),
            ("codigo_postal", "CP", 70),
            ("telefono", "Teléfono", 100),
            ("email", "Email", 180),
            ("sexo", "Sexo", 70),
            ("edad", "Edad", 60),
            ("estudios", "Estudios", 150),
            ("estado_laboral", "Estado laboral", 150)
        ]
        for col, texto, ancho in columnas:
            self.tree.heading(col, text=texto)
            anchor = "center" if col in ("nif", "codigo_postal", "telefono", "sexo", "edad") else "w"
            self.tree.column(col, width=ancho, anchor=anchor)
        # Scrollbars
        scroll_y = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tree.yview)
        scroll_x = ttk.Scrollbar(frame_tabla, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        # Grid
        self.tree.grid(row=0, column=0, sticky="nsew")
        scroll_y.grid(row=0, column=1, sticky="ns")
        scroll_x.grid(row=1, column=0, sticky="ew")
        frame_tabla.grid_rowconfigure(0, weight=1)
        frame_tabla.grid_columnconfigure(0, weight=1)
        # ===== Botones inferiores =====
        frame_btns = tk.Frame(self, bg=self.bg_color)
        frame_btns.pack(pady=10)
        ttk.Button(frame_btns, text="Editar alumno", command=self.editar_seleccionado).grid(row=0, column=0, padx=5)
        ttk.Button(frame_btns, text="Añadir alumno", command=self.ventana_nuevo_alumno).grid(row=0, column=1, padx=5)
        ttk.Button(frame_btns, text="Eliminar", command=self.eliminar_seleccionado).grid(row=0, column=2, padx=5)
        # Cargar datos
        self.cargar_datos()

    #  FUNCIONES DE LISTADO
    def cargar_datos(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        datos = model.obtener_alumnos()
        for a in datos:
            self.tree.insert("", tk.END, values=a)
        auto_ajustar_columnas(self.tree)

    # FUNCIONES CRUD
    def editar_seleccionado(self):
        item = self.tree.selection()
        if not item:
            messagebox.showwarning("Aviso", "Selecciona un alumno para editar.")
            return
        valores = self.tree.item(item, "values")
        nif = valores[0]
        datos = model.obtener_datos_alumno(nif)
        if not datos:
            messagebox.showerror("Error", "No se pudieron obtener los datos.")
            return
        self.ventana_editar_alumno(nif, datos)

    def eliminar_seleccionado(self):
        item = self.tree.selection()
        if not item:
            messagebox.showwarning("Aviso", "Selecciona un alumno a eliminar.")
            return
        alumno = self.tree.item(item, "values")
        nif = alumno[0]
        if messagebox.askyesno("Confirmar", "¿Eliminar este alumno?"):
            model.eliminar_alumno(nif)
            self.cargar_datos()

    def ventana_nuevo_alumno(self):
        win = tk.Toplevel(self)
        win.title("➕ Nuevo alumno")
        win.geometry("420x560")
        win.resizable(False, False)
        win.configure(bg=self.bg_color)
        win.transient(self)
        win.grab_set()
        tk.Label(
            win,
            text="Registro de nuevo alumno",
            font=("Segoe UI", 12, "bold"),
            fg="#3E64FF",
            bg=self.bg_color
        ).pack(pady=(10, 15))
        frame = tk.Frame(win, bg=self.bg_color)
        frame.pack(padx=15, pady=10, fill="both", expand=True)
        campos = [
            "NIF", "Nombre", "Apellidos", "Localidad", "Código postal",
            "Teléfono", "Email", "Sexo", "Edad", "Estudios", "Estado laboral"
        ]
        claves = [
            "nif", "nombre", "apellidos", "localidad", "codigo_postal",
            "telefono", "email", "sexo", "edad", "estudios", "estado_laboral"
        ]
        self.entries_nuevo = {}
        for i, (label, clave) in enumerate(zip(campos, claves)):
            ttk.Label(frame, text=label + ":", background=self.bg_color).grid(
                row=i, column=0, sticky="w", padx=5, pady=5
            )
            if clave == "sexo":
                entry = ttk.Combobox(
                    frame, values=["Mujer", "Hombre", "Otro"],
                    state="readonly", width=25
                )
            elif clave == "estado_laboral":
                entry = ttk.Combobox(
                    frame, values=["Empleado", "Desempleado", "Estudiante"],
                    state="readonly", width=25
                )
            else:
                entry = ttk.Entry(frame, width=28)
            entry.grid(row=i, column=1, padx=5, pady=5, sticky="w")
            self.entries_nuevo[clave] = entry
        ttk.Button(
            win,
            text="💾 Guardar alumno",
            command=lambda: self.guardar_alumno(win)
        ).pack(pady=(15, 10))

    def guardar_alumno(self, ventana):
        datos = [self.entries_nuevo[c].get() for c in self.entries_nuevo]
        if not all(datos):
            messagebox.showerror("Error", "Rellena todos los campos.")
            return
        try:
            model.crear_alumno(*datos)
            messagebox.showinfo("Éxito", "Alumno añadido correctamente.")
            ventana.destroy()
            self.cargar_datos()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def ventana_editar_alumno(self, nif, datos):
        win = tk.Toplevel(self)
        win.title(f"Editar alumno ({nif})")
        win.geometry("420x560")
        win.configure(bg=self.bg_color)
        win.transient(self)
        win.grab_set()
        tk.Label(
            win,
            text=f"✏️ Editar datos de {datos[0]} {datos[1]}",
            font=("Segoe UI", 12, "bold"),
            fg="#3E64FF",
            bg=self.bg_color
        ).pack(pady=(10, 15))
        frame = tk.Frame(win, bg=self.bg_color)
        frame.pack(padx=15, pady=10, fill="both", expand=True)
        campos = [
            "Nombre", "Apellidos", "Localidad", "Código postal", "Teléfono",
            "Email", "Sexo", "Edad", "Estudios", "Estado laboral"
        ]
        claves = [
            "nombre", "apellidos", "localidad", "codigo_postal", "telefono",
            "email", "sexo", "edad", "estudios", "estado_laboral"
        ]
        self.entries_edit = {}
        for i, (label, clave, valor) in enumerate(zip(campos, claves, datos)):
            ttk.Label(frame, text=label + ":", background=self.bg_color).grid(row=i, column=0, sticky="w", padx=5, pady=5)
            if clave == "sexo":
                entry = ttk.Combobox(frame, values=["Mujer", "Hombre", "Otro"], state="readonly", width=25)
                entry.set(valor if valor in ["Mujer", "Hombre", "Otro"] else "")
            elif clave == "estado_laboral":
                entry = ttk.Combobox(frame, values=["Empleado/a", "Desempleado/a", "Estudiante"], state="readonly", width=25)
                entry.set(valor if valor in ["Empleado/a", "Desempleado/a", "Estudiante"] else "")
            else:
                entry = ttk.Entry(frame, width=28)
                entry.insert(0, valor if valor is not None else "")
            entry.grid(row=i, column=1, padx=5, pady=5, sticky="w")
            self.entries_edit[clave] = entry
        ttk.Button(win, text="💾 Guardar cambios", command=lambda: self.guardar_edicion(nif, win)).pack(pady=(15, 10))

    # DETALLE
    def ver_detalle_alumno(self, event):
        sel = self.tree.selection()
        if not sel:
            return
        nif = self.tree.item(sel[0])["values"][0]
        DetalleAlumnoWindow(self, nif, modo=self.modo)
