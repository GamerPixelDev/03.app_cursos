import tkinter as tk
import os
from tkinter import messagebox, ttk, PhotoImage
from ui.alumnos_window import AlumnosWindows
from ui.cursos_window import CursosWindow
from ui.matriculas_window import MatriculasWindow
from ui.buscar_alumno_window import BuscarAlumnoWindow
from ui.buscar_curso_window import BuscarCursoWindow
from datetime import datetime
from models import export_utils, export_pdf
class MainWindow:
    def __init__(self, usuario, rol):
        self.root = tk.Tk()
        self._setup_style()
        self.root.title(f"Gestión de Cursos - Usuario: {usuario} ({rol})")
        self.root.geometry("1000x650")
        self.root.resizable(True, True)
        # --- Banner superior ---
        banner = tk.Frame(self.root, bg="#3E64FF", height=60)
        banner.pack(fill="x", side="top")
        titulo = tk.Label(banner, text="💼 Gestor de Cursos", bg="#3E64FF", fg="white", font=("Segoe UI", 14, "bold"))
        titulo.pack(side="left", padx=5)
        usuario_label = tk.Label(banner, text=f"👤 {usuario} ({rol})", bg="#3E64FF", fg="white", font=("Segoe UI", 10, "italic"))
        usuario_label.pack(side="right", padx=20)
        separator = ttk.Separator(self.root, orient="horizontal")
        separator.pack(fill="x")
        #Menu principal
        menu_bar = tk.Menu(self.root)
        #Menú alumnos
        menu_alumnos = tk.Menu(menu_bar, tearoff=0)
        menu_alumnos.add_command(label="Ver alumnos", command=self.ver_alumnos)
        menu_alumnos.add_command(label="Buscar alumno", command=self.buscar_alumno)
        if rol == "admin":
            menu_alumnos.add_command(label="Añadir alumno", command=self.add_alumno)
        menu_bar.add_cascade(label="🎓 Alumnos", menu=menu_alumnos)
        #Menú cursos
        menu_cursos = tk.Menu(menu_bar, tearoff=0)
        menu_cursos.add_command(label="Ver cursos", command=self.ver_cursos)
        menu_cursos.add_command(label="Buscar curso", command=self.buscar_curso)
        if rol == "admin":
            menu_cursos.add_command(label="Añadir curso", command=self.add_curso)
        menu_bar.add_cascade(label="📚 Cursos", menu=menu_cursos)
        #Menú matrículas
        menu_matriculas = tk.Menu(menu_bar, tearoff=0)
        menu_matriculas.add_command(label="Ver Matrículas", command=self.ver_matriculas)
        if rol == "admin":
            menu_matriculas.add_command(label="Agregar Matrícula", command=self.add_matricula)
        menu_bar.add_cascade(label="📜 Matrículas", menu=menu_matriculas)
        #Menú Consultas (Está comentando porque de momento no se va a usar este menú)
        """menu_consultas = tk.Menu(menu_bar, tearoff=0)
        menu_consultas.add_command(label="Buscar alumno", command=self.buscar_alumno)
        menu_bar.add_cascade(label="Consultas", menu=menu_consultas)"""
        #Menú Exportar / Importar
        menu_export = tk.Menu(menu_bar, tearoff=0)
        menu_export.add_command(label="Exportar a Excel", command=self.export_excel)
        menu_export.add_command(label="Exportar a PDF", command=self.export_pdf)
        if rol == "admin":
            menu_export.add_separator()
            menu_export.add_command(label="Importar desde Excel", command=self.import_excel)
        menu_bar.add_cascade(label="Exportar / Importar", menu=menu_export)
        #Menu usuarios (sólo admin)
        if rol == "admin":
            menu_usuarios = tk.Menu(menu_bar, tearoff=0)
            menu_usuarios.add_command(label="Gestionar Usuarios", command=self.manage_users)
            menu_bar.add_cascade(label="Usuarios", menu=menu_usuarios)
        #Menú salir
        menu_bar.add_command(label="Salir", command=self.root.quit)
        self.root.config(menu=menu_bar)
        #--- footer ---
        footer = tk.Frame(self.root, bg="#E9ECEF", height=25)
        footer.pack(fill="x", side="bottom")
        texto_footer = tk.Label(
            footer,
            text=f"Versión 1.0 · {datetime.now().strftime('%d/%m/%Y %H:%M')}",
            bg="#E9ECEF",
            fg="#555555",
            font=("Segoe UI", 9)
        )
        texto_footer.pack(side="right", padx=10)
        self.root.mainloop()

    def _setup_style(self):
        style = ttk.Style()
        # Tema un poco más moderno que el default
        try:
            style.theme_use("clam")
        except Exception:
            pass  # si no existe, sigue con el tema por defecto
        # ---- Treeview (tabla)
        style.configure(
            "Treeview",
            background="#fdfdfd",
            foreground="#222222",
            rowheight=24,
            fieldbackground="#fdfdfd",
            font=("Segoe UI", 10)
        )
        style.configure(
            "Treeview.Heading",
            background="#3E64FF",
            foreground="#ffffff",
            font=("Segoe UI", 10, "bold")
        )
        style.map(
            "Treeview",
            background=[("selected", "#4A90E2")]
        )
        # ---- Botones
        style.configure(
            "TButton",
            font=("Segoe UI", 10),
            padding=6
        )
        style.map(
            "TButton",
            relief=[("pressed", "sunken"), ("!pressed", "raised")]
        )

    #=== Métodos placeholder para las funcionalidades del menú ===
    #--- Menu alumnos ---
    def ver_alumnos(self):
        AlumnosWindows(self.root)
    def buscar_alumno(self):
        BuscarAlumnoWindow(self.root)
    def add_alumno(self): messagebox.showinfo("Alumnos", "Agregar Alumno (admin)") #Se puede comentar porque no se usa de momento
    #--- Menú cursos ---
    def ver_cursos(self):
        CursosWindow(self.root)
    def buscar_curso(self):
        BuscarCursoWindow(self.root)
    def add_curso(self): messagebox.showinfo("Cursos", "Agregar Curso (admin)") #Se puede comentar porque no se usa de momento
    #--- Menú matrículas ---
    def ver_matriculas(self):
        MatriculasWindow(self.root)
    def add_matricula(self): messagebox.showinfo("Matrículas", "Agregar Matrícula (admin)") #Se puede comentar porque no se usa de momento
    #--- Menú Exportar/Importar ---
    def export_excel(self):
        try:
            ruta = export_utils.exportar_alumnos_excel()
            messagebox.showinfo("Exportar a Excel", f"Archivo generado correctamente:\n{ruta}")
        except Exception as e:
            messagebox.showerror("Error al exportar", f"No se pudo generar el Excel:\n{e}")
    def export_pdf(self):
        try:
            ruta = export_pdf.exportar_alumnos_pdf()
            messagebox.showinfo("Exportar a PDF", f"Archivo generado correctamente:\n{ruta}")
        except Exception as e:
            messagebox.showerror("Error al exportar", f"No se pudo generar el PDF:\n{e}")
    def import_excel(self): messagebox.showinfo("Importar", "Importar desde Excel (admin)")
    #--- Menú usuarios ---
    def manage_users(self): messagebox.showinfo("Usuarios", "Gestión de Usuarios (admin)")