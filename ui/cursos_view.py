import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from tkcalendar import DateEntry
from models import cursos as model
from ui.detalle_curso_window import DetalleCursoWindow
from ui.utils_style import aplicar_estilo_global
from ui.utils_treeview import auto_ajustar_columnas, ajustar_tamano_ventana

class CursosView(tk.Frame):
    def __init__(self, parent, modo="claro"):
        super().__init__(parent)
        self.modo = modo
        self.style, self.bg_color = aplicar_estilo_global(modo)
        self.configure(bg=self.bg_color)
        # ===== Título de la vista =====
        lbl_title = tk.Label(
            self,
            text="🎓 Gestión de Cursos",
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
        ttk.Button(frame_btns, text="Editar seleccionado", command=self.editar_seleccionado).grid(row=0, column=0, padx=5)
        ttk.Button(frame_btns, text="Añadir curso", command=self.ventana_nuevo_curso).grid(row=0, column=1, padx=5)
        ttk.Button(frame_btns, text="Eliminar seleccionado", command=self.eliminar_seleccionado).grid(row=0, column=2, padx=5)
        # Cargar datos
        self.cargar_datos()

    #  FUNCIONES DE LISTADO
    def cargar_datos(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        datos = model.obtener_cursos()
        for a in datos:
            self.tree.insert("", tk.END, values=a)
        auto_ajustar_columnas(self.tree)

    # FUNCIONES CRUD
    def editar_seleccionado(self):
        item = self.tree.selection()
        if not item:
            messagebox.showwarning("Aviso", "Selecciona un curso para editar.")
            return
        valores = self.tree.item(item, "values")
        codigo = valores[0]
        datos = model.obtener_datos_curso(codigo)
        if not datos:
            messagebox.showerror("Error", "No se pudieron obtener los datos del curso.")
            return
        self.ventana_editar_curso(codigo, datos)

    def eliminar_seleccionado(self):
        item = self.tree.selection()
        if not item:
            messagebox.showwarning("Aviso", "Selecciona un curso a eliminar.")
            return
        curso = self.tree.item(item, "values")
        codigo_curso = curso[0]
        if messagebox.askyesno("Confirmar", "¿Eliminar este curso?"):
            model.eliminar_curso(codigo_curso)
            self.cargar_datos()

    def ventana_nuevo_curso(self):
        win = tk.Toplevel(self)
        win.title("➕ Nuevo curso")
        win.geometry("430x460")
        win.resizable(False, False)
        win.configure(bg=self.bg_color)
        win.transient(self)
        win.grab_set()
        tk.Label(
            win,
            text="Registro de nuevo curso",
            font=("Segoe UI", 12, "bold"),
            fg="#3E64FF",
            bg=self.bg_color
        ).pack(pady=(10, 15))
        frame = tk.Frame(win, bg=self.bg_color)
        frame.pack(padx=15, pady=10, fill="both", expand=True)
        campos = [
            ("Código del curso", "codigo_curso"),
            ("Nombre del curso", "nombre"),
            ("Fecha inicio", "fecha_inicio"),
            ("Fecha fin", "fecha_fin"),
            ("Lugar", "lugar"),
            ("Modalidad", "modalidad"),
            ("Horas", "horas"),
            ("Responsable", "responsable")
        ]
        self.entries = {}
        for i, (etiqueta, clave) in enumerate(campos):
            ttk.Label(frame, text=etiqueta + ":", background=self.bg_color).grid(row=i, column=0, sticky="w", padx=5, pady=5)
            if clave == "modalidad":
                entry = ttk.Combobox(frame, values=["Presencial", "Online", "Mixta"], state="readonly", width=25)
            elif clave in ("fecha_inicio", "fecha_fin"):
                entry = DateEntry(
                    frame,
                    width=25,
                    date_pattern="yyyy-mm-dd",
                    background="lightblue",
                    foreground="black",
                    borderwidth=2
                )
                entry.bind("<Button-1>", lambda e, de=entry: de.drop_down())
                entry.bind("<FocusOut>", lambda e, de=entry: de._top_cal.withdraw() if getattr(de, "_top_cal", None) else None)
            else:
                entry = ttk.Entry(frame, width=28)
            entry.grid(row=i, column=1, padx=5, pady=5, sticky="w")
            self.entries[clave] = entry
        ttk.Button(win, text="💾 Guardar curso", command=lambda: self.guardar_curso(win)).pack(pady=(15, 20))

    def guardar_curso(self, ventana):
        try:
            datos = [self.entries[c].get() for c in self.entries]
            if not all(datos):
                messagebox.showerror("Error", "Rellena todos los campos.")
                return
            # Validar coherencia de fechas
            inicio = datetime.strptime(self.entries["fecha_inicio"].get(), "%Y-%m-%d")
            fin = datetime.strptime(self.entries["fecha_fin"].get(), "%Y-%m-%d")
            if fin < inicio:
                messagebox.showwarning("Fechas inválidas", "La fecha de fin no puede ser anterior a la de inicio.")
                return
            model.crear_curso(*datos)
            messagebox.showinfo("Éxito", "Curso añadido correctamente.")
            ventana.destroy()
            self.cargar_datos()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # DETALLE
    def ver_detalle_curso(self, event):
        selection = self.tree.selection()
        if not selection:
            return
        item = self.tree.item(selection[0])
        codigo_curso = item["values"][0]
        DetalleCursoWindow(self, codigo_curso, modo=self.modo)
