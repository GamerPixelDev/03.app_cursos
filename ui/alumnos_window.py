import tkinter  as tk
import tkinter.font as tkfont
from tkinter import ttk, messagebox
from models import alumnos as model
from ui.detalle_alumno_window import DetalleAlumnoWindow

class AlumnosWindows(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Gestión de alumnos")
        self.geometry("1100x600")
        self.resizable(True, True)
        self.transient(parent) #La asocia visualmente a la ventana principal
        self.grab_set() # Bloquea interacción con otras ventanas hasta cerrar esta
        self.focus_set() # Trae el foco a la ventana actual
        #--- Tabla ---
        self.tree = ttk.Treeview(self, columns=("nif", "nombre", "apellidos", "localidad", "codigo_postal", "telefono", "email", "sexo", "edad", "estudios", "estado_laboral"),
                                show="headings", height=15
                                )
        self.tree.bind("<Double-1>", self.ver_detalle_alumno)
        columnas = [
            ("nif", "NIF", 40),
            ("nombre", "Nombre", 100),
            ("apellidos", "Apellidos", 120),
            ("localidad", "Localidad", 100),
            ("codigo_postal", "CP", 20),
            ("telefono", "Teléfono", 60),
            ("email", "Email", 150),
            ("sexo", "Sexo", 5),
            ("edad", "Edad", 5),
            ("estudios", "Estudios", 100),
            ("estado_laboral", "Estado laboral", 30)
        ]
        for col, texto, ancho in columnas:
            self.tree.heading(col, text=texto)
            if col in ("nif", "codigo_postal", "telefono", "sexo", "edad"):  # centrados
                self.tree.column(col, width=ancho, anchor="center")
            else:
                self.tree.column(col, width=ancho)
        #--- Barras de desplazamiento ---
        scroll_y = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        scroll_x = ttk.Scrollbar(self, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

        scroll_y.pack(side="right", fill="y")
        scroll_x.pack(side="bottom", fill="x")
        self.tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        #--- Botones ---
        frame_btns = tk.Frame(self)
        frame_btns.pack(pady=10)
        ttk.Button(frame_btns, text="Actualizar lista", command=self.cargar_datos).grid(row=0, column=0, padx=5)
        ttk.Button(frame_btns, text="Añadir alumno", command=self.ventana_nuevo_alumno).grid(row=0, column=1, padx=5)
        ttk.Button(frame_btns, text="Eliminar seleccionado", command=self.eliminar_seleccionado).grid(row=0, column=2, padx=5)
        self.cargar_datos()

    #--- Cargar datos en tabla ---
    def cargar_datos(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        alumnos = model.obtener_alumnos()
        for a in alumnos:
            # Orden correcto: nif, nombre, apellidos, localidad, codigo_postal, telefono, email, sexo, edad, estudios, estado_laboral
            self.tree.insert("", tk.END, values=a)
        self.ajustar_columnas()

    #--- Eliminar alumno seleccionado ---
    def eliminar_seleccionado(self):
        item = self.tree.selection()
        if not item:
            messagebox.showwarning("Aviso", "Selecciona un alumno a eliminar.")
            return
        alumno = self.tree.item(item, "values")
        nif_alumno = alumno[0]
        confirmar = messagebox.askyesno("Confirmar", f"¿Eliminar al alumno {alumno[2]} {alumno[3]}?")
        if confirmar:
            model.eliminar_alumno(nif_alumno)
            self.cargar_datos()

    #--- Ventana para añadir alumno ---
    def ventana_nuevo_alumno(self):
        win = tk.Toplevel(self)
        win.title("Nuevo alumno")
        win.geometry("400x550")
        campos = [
            "nif", "nombre", "apellidos", "localidad", "codigo_postal",
            "telefono", "email", "sexo", "edad", "estudios", "estado_laboral"
        ]
        self.entries = {}
        for i, campo in enumerate(campos):
            ttk.Label(win, text=campo.capitalize()).grid(row=i, column=0, sticky="w", padx=10, pady=5)
            entry = ttk.Entry(win)
            entry.grid(row=i, column=1, padx=10, pady=5)
            self.entries[campo] = entry
        ttk.Button(win, text="Guardar", command=lambda: self.guardar_alumno(win)).grid(row=len(campos), columnspan=2, pady=10)

    #--- Guardar alumno ---
    def guardar_alumno(self, ventana):
        datos = [self.entries[c].get() for c in self.entries]
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

    def ver_detalle_alumno(self, event):
        selection = self.tree.selection()
        if not selection:
            return
        item = self.tree.item(selection[0])
        nif = item["values"][0] #asumiendo que la primera columna es NIF
        DetalleAlumnoWindow(self, nif)

    def ajustar_columnas(self):
        """Ajusta cada columna al texto más largo y fuerza el repintado."""
        self.update_idletasks()
        font = tkfont.Font()
        for col in self.tree["columns"]:
            header_text = self.tree.heading(col)["text"]
            max_width = font.measure(header_text)
            for item_id in self.tree.get_children():
                text = str(self.tree.set(item_id, col))
                w = font.measure(text)
                if w > max_width:
                    max_width = w
            # Aplica ancho y bloquea estiramiento
            self.tree.column(col, width=max_width + 10, stretch=False)
        # Fuerza redibujo tras aplicar todos los anchos
        self.update_idletasks()

    #=== Funcion usada para comprobar que anchos se dibujaban al mostrar alumnos ===
    def ajustar_columnas_debug(self):
        """Versión de depuración: muestra por consola las medidas."""
        self.update_idletasks()
        font = tkfont.Font()
        print("=== Ajuste de columnas ===")
        for col in self.tree["columns"]:
            header_text = self.tree.heading(col)["text"]
            max_width = font.measure(header_text)
            print(f"Encabezado {header_text}: {max_width}px")
            for item_id in self.tree.get_children():
                text = str(self.tree.set(item_id, col))
                w = font.measure(text)
                if w > max_width:
                    max_width = w
            print(f"  -> Máx. {col}: {max_width}px")
            self.tree.column(col, width=max_width + 25)
        print("=== Fin de ajuste ===")



