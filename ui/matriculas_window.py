import tkinter as tk
import tkinter.font as tkfont
from tkinter import ttk, messagebox
from models import matriculas as model
from models import alumnos, cursos
from datetime import datetime

class MatriculasWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Gestión de matrículas")
        self.geometry("1100x600")
        self.resizable(True, True)
        self.transient(parent) #La asocia visualmente a la ventana principal
        self.grab_set() # Bloquea interacción con otras ventanas hasta cerrar esta
        self.focus_set() # Trae el foco a la ventana actual
        # ----- Tabla -----
        self.tree = ttk.Treeview(self, columns=("nif", "alumno","codigo_curso", "curso", "fecha"), show="headings", height=15)
        self.tree.heading("nif", text="NIF")
        self.tree.heading("alumno", text="Alumno")
        self.tree.heading("codigo_curso", text="Código curso")
        self.tree.heading("curso", text="Curso")
        self.tree.heading("fecha", text="Fecha matrícula")
        self.tree.column("nif", width=100)
        self.tree.column("alumno", width=200)
        self.tree.column("codigo_curso", width=120)
        self.tree.column("curso", width=200)
        self.tree.column("fecha", width=120)
        columnas = [
            ("nif", "NIF Alumno", 100),
            ("alumno", "Alumno", 150),
            ("codigo_curso", "Código Curso", 120),
            ("curso", "Curso", 180),
            ("fecha", "Fecha Matrícula", 120)
        ]
        for col, texto, ancho in columnas:
            self.tree.heading(col, text=texto, anchor="center")
            if col in ("nif", "codigo_curso", "fecha"):
                self.tree.column(col, anchor="center", width=ancho)
            else:
                self.tree.column(col, anchor="w", width=ancho)

        self.tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        # ----- Botones -----
        frame_btns = tk.Frame(self)
        frame_btns.pack(pady=10)
        ttk.Button(frame_btns, text="Actualizar lista", command=self.cargar_datos).grid(row=0, column=0, padx=5)
        ttk.Button(frame_btns, text="Nueva matrícula", command=self.ventana_nueva_matricula).grid(row=0, column=1, padx=5)
        ttk.Button(frame_btns, text="Eliminar seleccionada", command=self.eliminar_seleccionada).grid(row=0, column=2, padx=5)
        self.cargar_datos()

    # ----- Cargar datos -----
    def cargar_datos(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        matriculas = model.obtener_matriculas()
        for m in matriculas:
            self.tree.insert("", tk.END, values=m)
        self.ajustar_columnas()

    # ----- Eliminar matrícula -----
    def eliminar_seleccionada(self):
        item = self.tree.selection()
        if not item:
            messagebox.showwarning("Aviso", "Selecciona una matrícula para eliminar.")
            return
        matricula = self.tree.item(item, "values")
        id_matricula = matricula[0]
        confirmar = messagebox.askyesno("Confirmar", f"¿Eliminar la matrícula de {matricula[1]} en {matricula[2]}?")
        if confirmar:
            model.eliminar_matricula(id_matricula)
            self.cargar_datos()

    # ----- Ventana para nueva matrícula -----
    def ventana_nueva_matricula(self):
        win = tk.Toplevel(self)
        win.title("Nueva matrícula")
        win.geometry("400x250")
        ttk.Label(win, text="Alumno:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        alumno = alumnos.obtener_alumnos()
        self.combo_alumnos = ttk.Combobox(win, values=[f"{a[0]} - {a[1]} {a[2]}" for a in alumno], width=30)
        self.combo_alumnos.grid(row=0, column=1, padx=10, pady=5)
        ttk.Label(win, text="Curso:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        curso = cursos.obtener_cursos()
        self.combo_cursos = ttk.Combobox(win, values=[f"{c[0]} - {c[2]}" for c in curso], width=30)
        self.combo_cursos.grid(row=1, column=1, padx=10, pady=5)
        ttk.Button(win, text="Guardar", command=lambda: self.guardar_matricula(win)).grid(row=3, columnspan=2, pady=20)

    # ----- Guardar matrícula -----
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
            messagebox.showinfo("Éxito", "Matrícula creeada correctamente.")
            ventana.destroy()
            self.cargar_datos()
        else:
            messagebox.showwarning("Duplicado", "⚠️ Este alumno ya está matriculado en este curso.")
        #Se comenta lo de abajo porque se ha implementado por un if/else
        """try:
            model.crear_matricula(nif_alumno, codigo_curso, fecha_matricula)
        except sqlite3.IntegrityError:
            messagebox.showwarning("Duplicado", "⚠️ Este alumno ya está matriculado en este curso.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        else:
            messagebox.showinfo("Éxito", "Matrícula creada correctamente.")
            ventana.destroy()
            self.cargar_datos()"""
        
    def ajustar_columnas(self):
        """Ajusta cada columna al texto más largo y bloquea el estiramiento."""
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
            # Desactiva stretch y añade margen visual
            self.tree.column(col, width=max_width + 25, stretch=False)
        self.update_idletasks()