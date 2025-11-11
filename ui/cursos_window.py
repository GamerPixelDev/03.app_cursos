import tkinter as tk
from tkcalendar import DateEntry
from tkinter import ttk, messagebox
from datetime import datetime
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
        ttk.Button(frame_btns, text="Editar seleccionado", command=self.editar_seleccionado).grid(row=0, column=0, padx=5)
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

    # === Editar curso seleccionado ===
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

    # === Ventana para editar curso ===
    def ventana_editar_curso(self, codigo, datos):
        win = tk.Toplevel(self)
        win.title(f"✏️ Editar curso ({codigo})")
        win.geometry("420x520")
        win.resizable(False, False)
        win.configure(bg=self.bg_color)
        win.transient(self)
        win.grab_set()
        tk.Label(
            win,
            text=f"Editar datos del curso {codigo}",
            font=("Segoe UI", 12, "bold"),
            fg="#3E64FF",
            bg=self.bg_color
        ).pack(pady=(10, 15))
        frame = tk.Frame(win, bg=self.bg_color)
        frame.pack(padx=15, pady=10, fill="both", expand=True)
        campos = [
            "Nombre", "Fecha inicio", "Fecha fin", "Lugar",
            "Modalidad", "Horas", "Responsable"
        ]
        claves = [
            "nombre", "fecha_inicio", "fecha_fin", "lugar",
            "modalidad", "horas", "responsable"
        ]
        self.entries_edit = {}
        for i, (label, clave, valor) in enumerate(zip(campos, claves, datos)):
            ttk.Label(frame, text=label + ":", background=self.bg_color).grid(row=i, column=0, sticky="w", padx=5, pady=5)
            # Campos con opciones desplegables
            if clave == "modalidad":
                entry = ttk.Combobox(
                    frame,
                    values=["Presencial", "Online", "Mixta"],
                    state="readonly",
                    width=25
                )
                entry.set(valor if valor in ["Presencial", "Online", "Mixta"] else "")
            else:
                entry = ttk.Entry(frame, width=28)
                entry.insert(0, valor if valor is not None else "")
            # Si el campo es de fecha, usamos DateEntry
            if clave in ("fecha_inicio", "fecha_fin"):
                entry = DateEntry(
                    frame,
                    width=25,
                    date_pattern="yyyy-mm-dd",
                    background="lightblue",
                    foreground="black",
                    borderwidth=2
                )
                entry.bind("<FocusOut>", lambda e: entry._top_cal.withdraw() if entry._top_cal else None)
            else:
                entry = ttk.Entry(frame, width=28)
            entry.grid(row=i, column=1, padx=5, pady=5, sticky="w")
            self.entries_edit[clave] = entry
        ttk.Button(
            win,
            text="💾 Guardar cambios",
            command=lambda: self.guardar_edicion(codigo, win)
        ).pack(pady=(15, 10))

    # === Guardar cambios del curso ===
    def guardar_edicion(self, codigo, ventana):
        try:
            for campo, entry in self.entries_edit.items():
                valor = entry.get().strip()
                if valor == "":
                    messagebox.showwarning("Campo vacío", f"El campo '{campo}' no puede estar vacío.")
                    return
                # Validar coherencia de fechas
                try:
                    inicio = datetime.strptime(self.entries_edit["fecha_inicio"].get(), "%Y-%m-%d")
                    fin = datetime.strptime(self.entries_edit["fecha_fin"].get(), "%Y-%m-%d")
                    if fin < inicio:
                        messagebox.showwarning("Fechas inválidas", "La fecha de fin no puede ser anterior a la de inicio.")
                        return
                except Exception:
                    messagebox.showwarning("Formato incorrecto", "Las fechas deben tener formato AAAA-MM-DD.")
                    return
                model.actualizar_curso(codigo, campo, valor)
            messagebox.showinfo("Éxito", "Curso actualizado correctamente.")
            ventana.destroy()
            self.cargar_datos()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar el curso:\n{e}")

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
        win.title("➕ Nuevo curso")
        win.geometry("430x460")
        win.resizable(False, False)
        win.configure(bg=self.bg_color)
        win.transient(self)
        win.grab_set()
        # === Encabezado ===
        tk.Label(
            win,
            text="Registro de nuevo curso",
            font=("Segoe UI", 12, "bold"),
            fg="#3E64FF",
            bg=self.bg_color
        ).pack(pady=(10, 15))
        # === Contenedor principal ===
        frame = tk.Frame(win, bg=self.bg_color)
        frame.pack(padx=15, pady=10, fill="both", expand=True)
        campos = [
            ("Código del curso", "codigo_curso"),
            ("Nombre del curso", "nombre"),
            ("Fecha inicio (AAAA-MM-DD)", "fecha_inicio"),
            ("Fecha fin (AAAA-MM-DD)", "fecha_fin"),
            ("Lugar", "lugar"),
            ("Modalidad", "modalidad"),
            ("Horas", "horas"),
            ("Responsable", "responsable")
        ]
        self.entries = {}
        for i, (etiqueta, clave) in enumerate(campos):
            ttk.Label(frame, text=etiqueta + ":", background=self.bg_color).grid(
                row=i, column=0, sticky="w", padx=5, pady=5
            )
            entry = ttk.Entry(frame, width=30)
            # Si el campo es de fecha, usamos DateEntry
            if clave in ("fecha_inicio", "fecha_fin"):
                entry = DateEntry(
                    frame,
                    width=25,
                    date_pattern="yyyy-mm-dd",
                    background="lightblue",
                    foreground="black",
                    borderwidth=2
                )
                entry.bind("<FocusOut>", lambda e: entry._top_cal.withdraw() if entry._top_cal else None)
            else:
                entry = ttk.Entry(frame, width=28)
            entry.grid(row=i, column=1, padx=5, pady=5, sticky="w")
            self.entries[clave] = entry
        # === Botón de guardar ===
        ttk.Button(
            win,
            text="💾 Guardar curso",
            command=lambda: self.guardar_curso(win)
        ).pack(pady=(15, 10))

    # === Guardar curso ===
    def guardar_curso(self, ventana):
        datos = [self.entries[c].get() for c in self.entries]
        if not all(datos):
            messagebox.showerror("Error", "Rellena todos los campos.")
            return
        try:
            # Validar coherencia de fechas
            try:
                inicio = datetime.strptime(self.entries_edit["fecha_inicio"].get(), "%Y-%m-%d")
                fin = datetime.strptime(self.entries_edit["fecha_fin"].get(), "%Y-%m-%d")
                if fin < inicio:
                    messagebox.showwarning("Fechas inválidas", "La fecha de fin no puede ser anterior a la de inicio.")
                    return
            except Exception:
                messagebox.showwarning("Formato incorrecto", "Las fechas deben tener formato AAAA-MM-DD.")
                return
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
