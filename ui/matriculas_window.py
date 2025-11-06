import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from models import matriculas as model
from models import alumnos, cursos
from ui.utils_style import aplicar_estilo_global
from ui.utils_treeview import auto_ajustar_columnas, ajustar_tamano_ventana


class MatriculasWindow(tk.Toplevel):
    def __init__(self, parent, modo="claro"):
        super().__init__(parent)
        self.modo = modo
        self.style, self.bg_color = aplicar_estilo_global(modo)
        self.configure(bg=self.bg_color)
        self.title("Gestión de matrículas")
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
            columns=("nif", "alumno", "codigo_curso", "curso", "fecha"),
            show="headings",
            height=15
        )
        columnas = [
            ("nif", "NIF", 100),
            ("alumno", "Alumno", 200),
            ("codigo_curso", "Código Curso", 120),
            ("curso", "Curso", 200),
            ("fecha", "Fecha Matrícula", 120)
        ]
        for col, texto, ancho in columnas:
            self.tree.heading(col, text=texto, anchor="center")
            anchor = "center" if col in ("nif", "codigo_curso", "fecha") else "w"
            self.tree.column(col, width=ancho, anchor=anchor)
        # === Barras de desplazamiento ===
        scroll_y = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tree.yview)
        scroll_x = ttk.Scrollbar(frame_tabla, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
        scroll_y.grid(row=0, column=1, sticky="ns")
        scroll_x.grid(row=1, column=0, sticky="ew")
        frame_tabla.grid_rowconfigure(0, weight=1)
        frame_tabla.grid_columnconfigure(0, weight=1)
        # === Botones ===
        frame_btns = tk.Frame(self, bg=self.bg_color)
        frame_btns.pack(pady=10)
        ttk.Button(frame_btns, text="Actualizar lista", command=self.cargar_datos).grid(row=0, column=0, padx=5)
        ttk.Button(frame_btns, text="Nueva matrícula", command=self.ventana_nueva_matricula).grid(row=0, column=1, padx=5)
        ttk.Button(frame_btns, text="Eliminar seleccionada", command=self.eliminar_seleccionada).grid(row=0, column=2, padx=5)
        self.cargar_datos()

    # === Cargar datos en la tabla ===
    def cargar_datos(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        matriculas = model.obtener_matriculas()
        for m in matriculas:
            self.tree.insert("", tk.END, values=m)
        auto_ajustar_columnas(self.tree)
        ajustar_tamano_ventana(self.tree, self)

    # === Eliminar matrícula seleccionada ===
    def eliminar_seleccionada(self):
        item = self.tree.selection()
        if not item:
            messagebox.showwarning("Aviso", "Selecciona una matrícula para eliminar.")
            return
        matricula = self.tree.item(item, "values")

        nif = matricula[0]
        codigo_curso = matricula[2]
        confirmar = messagebox.askyesno(
            "Confirmar",
            f"¿Eliminar la matrícula de {matricula[1]} ({nif}) en {matricula[3]}?"
        )
        if confirmar:
            model.eliminar_matricula(nif, codigo_curso)
            self.cargar_datos()

    # === Ventana nueva matrícula ===
    def ventana_nueva_matricula(self):
        win = tk.Toplevel(self)
        win.title("Nueva matrícula")
        win.geometry("420x250")

        ttk.Label(win, text="Alumno:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        alumnos_lista = alumnos.obtener_alumnos()
        self.combo_alumnos = ttk.Combobox(
            win,
            values=[f"{a[0]} - {a[1]} {a[2]}" for a in alumnos_lista],
            width=35
        )
        self.combo_alumnos.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(win, text="Curso:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        cursos_lista = cursos.obtener_cursos()
        self.combo_cursos = ttk.Combobox(
            win,
            values=[f"{c[0]} - {c[1]}" for c in cursos_lista],  # nombre en lugar de fecha
            width=35
        )
        self.combo_cursos.grid(row=1, column=1, padx=10, pady=5)

        ttk.Button(win, text="Guardar", command=lambda: self.guardar_matricula(win)).grid(row=3, columnspan=2, pady=20)

    # === Guardar matrícula ===
    def guardar_matricula(self, ventana):
        alumno_sel = self.combo_alumnos.get()
        curso_sel = self.combo_cursos.get()

        if not alumno_sel or not curso_sel:
            messagebox.showerror("Error", "Selecciona alumno y curso.")
            return

        nif_alumno = alumno_sel.split(" - ")[0]
        codigo_curso = curso_sel.split(" - ")[0]
        fecha_matricula = datetime.now().strftime("%Y-%m-%d")

        exito = model.crear_matricula(nif_alumno, codigo_curso, fecha_matricula)
        if exito:
            messagebox.showinfo("Éxito", "Matrícula creada correctamente.")
            ventana.destroy()
            self.cargar_datos()
        else:
            messagebox.showwarning("Duplicado", "⚠️ Este alumno ya está matriculado en este curso.")
