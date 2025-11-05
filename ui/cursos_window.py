import tkinter as tk
import tkinter.font as tkfont
from tkinter import ttk, messagebox
from models import cursos as model

class CursosWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Gestión de cursos")
        self.geometry("1100x600")
        self.resizable(True, True)
        self.transient(parent) #La asocia visualmente a la ventana principal
        self.grab_set() # Bloquea interacción con otras ventanas hasta cerrar esta
        self.focus_set() # Trae el foco a la ventana actual
        # ----- Tabla -----
        self.tree = ttk.Treeview(self, columns=(
            "codigo_curso", "nombre", "fecha_inicio", "fecha_fin",
            "lugar", "modalidad", "horas", "responsable"),
            show="headings", height=15
        )
        columnas = [
            ("codigo_curso", "Código", 100),
            ("nombre", "Nombre", 160),
            ("fecha_inicio", "Inicio", 100),
            ("fecha_fin", "Fin", 100),
            ("lugar", "Lugar", 120),
            ("modalidad", "Modalidad", 100),
            ("horas", "Horas", 60),
            ("responsable", "Responsable", 120)
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
        # ----- Botones -----
        frame_btns = tk.Frame(self)
        frame_btns.pack(pady=10)
        ttk.Button(frame_btns, text="Actualizar lista", command=self.cargar_datos).grid(row=0, column=0, padx=5)
        ttk.Button(frame_btns, text="Añadir curso", command=self.ventana_nuevo_curso).grid(row=0, column=1, padx=5)
        ttk.Button(frame_btns, text="Eliminar seleccionado", command=self.eliminar_seleccionado).grid(row=0, column=2, padx=5)
        self.cargar_datos()

    # ----- Cargar datos -----
    def cargar_datos(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        cursos = model.obtener_cursos()
        for curso in cursos:
            self.tree.insert("", tk.END, values=curso)
            self.ajustar_columnas()

    # ----- Eliminar curso -----
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

    # ----- Ventana para añadir curso -----
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

    # ----- Guardar curso -----
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

    #--- Ajustar columnas ---
    def ajustar_columnas(self):
        #Ajusta automáticamente el ancho de cada columna al contenido
        font = tkfont.Font()
        # Reiniciamos los anchos a un mínimo para permitir que se reduzcan
        for col in self.tree["columns"]:
            self.tree.column(col, width=10)
        for col in self.tree["columns"]:
            # Calculamos el ancho del encabezado
            max_len = font.measure(self.tree.heading(col)["text"])
            # Calculamos el ancho máximo entre celdas
            for item in self.tree.get_children():
                texto = str(self.tree.set(item, col))
                ancho = font.measure(texto)
                if ancho > max_len:
                    max_len = ancho
            # Márgenes personalizados
            extra = 18
            if col in ("email", "estudios", "nombre", "lugar", "responsable"):
                extra = 50
        self.tree.column(col, width=max_len + extra)