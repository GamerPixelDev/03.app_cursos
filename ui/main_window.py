import tkinter as tk
from tkinter import messagebox
from ui.alumnos_window import AlumnosWindows
from ui.cursos_window import CursosWindow
from ui.matriculas_window import MatriculasWindow
from ui.buscar_alumno_window import BuscarAlumnoWindow

class MainWindow:
    def __init__(self, usuario, rol):
        self.root = tk.Tk()
        self.root.title(f"Gestión ed Cursos - Usuario: {usuario} - Rol: {rol}")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        #Menu principal
        menu_bar = tk.Menu(self.root)
        #Menú alumnos
        menu_alumnos = tk.Menu(menu_bar, tearoff=0)
        menu_alumnos.add_command(label="Ver alumnos", command=self.ver_alumnos)
        menu_alumnos.add_command(label="Buscar alumno", command=self.buscar_alumno)
        if rol == "admin":
            menu_alumnos.add_command(label="Añadir alumno", command=self.add_alumno)
        menu_bar.add_cascade(label="Alumnos", menu=menu_alumnos)
        #Menú cursos
        menu_cursos = tk.Menu(menu_bar, tearoff=0)
        menu_cursos.add_command(label="Ver cursos", command=self.ver_cursos)
        menu_cursos.add_command(label="Buscar curso", command=self.buscar_curso)
        if rol == "admin":
            menu_cursos.add_command(label="Añadir curso", command=self.add_curso)
        menu_bar.add_cascade(label="Cursos", menu=menu_cursos)
        #Menú matrículas
        menu_matriculas = tk.Menu(menu_bar, tearoff=0)
        menu_matriculas.add_command(label="Ver Matrículas", command=self.ver_matriculas)
        if rol == "admin":
            menu_matriculas.add_command(label="Agregar Matrícula", command=self.add_matricula)
        menu_bar.add_cascade(label="Matrículas", menu=menu_matriculas)
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
        self.root.mainloop()

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
    def export_excel(self): messagebox.showinfo("Exportar", "Exportar a Excel")
    def export_pdf(self): messagebox.showinfo("Exportar", "Exportar a PDF")
    def import_excel(self): messagebox.showinfo("Importar", "Importar desde Excel (admin)")
    #--- Menú usuarios ---
    def manage_users(self): messagebox.showinfo("Usuarios", "Gestión de Usuarios (admin)")