import tkinter as tk
import os
from tkinter import messagebox, ttk, filedialog
from ui.alumnos_window import AlumnosWindows
from ui.cursos_window import CursosWindow
from ui.matriculas_window import MatriculasWindow
from ui.buscar_alumno_window import BuscarAlumnoWindow
from ui.buscar_curso_window import BuscarCursoWindow
from datetime import datetime
from models import export_utils, export_pdf, import_utils
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
        #=== Menú alumnos ===
        menu_alumnos = tk.Menu(menu_bar, tearoff=0)
        menu_alumnos.add_command(label="Ver alumnos", command=self.ver_alumnos)
        menu_alumnos.add_command(label="Buscar alumno", command=self.buscar_alumno)
        menu_alumnos.add_command(label="Añadir alumno", command=self.add_alumno)
        #--- Submenú Exportar ---
        submenu_export_alumnos = tk.Menu(menu_alumnos, tearoff=0)
        submenu_export_alumnos.add_command(label="Excel", command=lambda: self.export_excel("alumnos"))
        submenu_export_alumnos.add_command(label="PDF", command=lambda: self.export_pdf("alumnos"))
        menu_alumnos.add_cascade(label="Exportar", menu=submenu_export_alumnos)
        #--- Submenú Importar ---
        submenu_import_alumnos = tk.Menu(menu_alumnos, tearoff=0)
        submenu_import_alumnos.add_command(label="Desde Excel", command=lambda: self.import_excel("alumnos"))
        menu_alumnos.add_cascade(label="Importar", menu=submenu_import_alumnos)
        menu_bar.add_cascade(label="🎓 Alumnos", menu=menu_alumnos)
        #=== Menú cursos ===
        menu_cursos = tk.Menu(menu_bar, tearoff=0)
        menu_cursos.add_command(label="Ver cursos", command=self.ver_cursos)
        menu_cursos.add_command(label="Buscar curso", command=self.buscar_curso)
        menu_cursos.add_command(label="Añadir curso", command=self.add_curso)
        #--- Submenú Exportar ---
        submenu_export_cursos = tk.Menu(menu_cursos, tearoff=0)
        submenu_export_cursos.add_command(label="Excel", command=lambda: self.export_excel("cursos"))
        submenu_export_cursos.add_command(label="PDF", command=lambda: self.export_pdf("cursos"))
        menu_cursos.add_cascade(label="Exportar", menu=submenu_export_cursos)
        #--- Submenú Importar ---
        submenu_import_cursos = tk.Menu(menu_cursos, tearoff=0)
        submenu_import_cursos.add_command(label="Desde Excel", command=lambda: self.import_excel("cursos"))
        menu_cursos.add_cascade(label="Importar", menu=submenu_import_cursos)
        menu_bar.add_cascade(label="📚 Cursos", menu=menu_cursos)
        #=== Menú matrículas ===
        menu_matriculas = tk.Menu(menu_bar, tearoff=0)
        menu_matriculas.add_command(label="Ver Matrículas", command=self.ver_matriculas)
        menu_matriculas.add_command(label="Agregar Matrícula", command=self.add_matricula)
        #--- Submenú Exportar ---
        submenu_export_matriculas = tk.Menu(menu_matriculas, tearoff=0)
        submenu_export_matriculas.add_command(label="Excel", command=lambda: self.export_excel("matriculas"))
        submenu_export_matriculas.add_command(label="PDF", command=lambda: self.export_pdf("matriculas"))
        menu_matriculas.add_cascade(label="Exportar", menu=submenu_export_matriculas)
        #--- Submenú Importar
        submenu_import_matriculas = tk.Menu(menu_matriculas, tearoff=0)
        submenu_import_matriculas.add_command(label="Desde Excel", command=lambda: self.import_excel("matriculas"))
        menu_cursos.add_cascade(label="Importar", menu=submenu_import_matriculas)
        menu_bar.add_cascade(label="📜 Matrículas", menu=menu_matriculas)
        #Menú Consultas (Está comentando porque de momento no se va a usar este menú)
        """menu_consultas = tk.Menu(menu_bar, tearoff=0)
        menu_consultas.add_command(label="Buscar alumno", command=self.buscar_alumno)
        menu_bar.add_cascade(label="Consultas", menu=menu_consultas)"""
        #Menú Importar (sólo admin)
        if rol == "admin":
            menu_import = tk.Menu(menu_bar, tearoff=0)
            menu_import.add_command(label="Importar desde Excel", command=self.import_excel)
            menu_bar.add_cascade(label="Importar", menu=menu_import)
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
    def export_excel(self, tipo):
        try:
            if tipo == "alumnos":
                ruta = export_utils.exportar_alumnos_excel()
            elif tipo == "cursos":
                ruta = export_utils.exportar_cursos_excel()
            elif tipo == "matriculas":
                ruta = export_utils.exportar_matriculas_excel()
            else:
                messagebox.showwarning("Aviso", "Tipo no reconocido.")
                return
            messagebox.showinfo("Exportar a Excel", f"Archivo generado correctamente:\n{ruta}")
        except Exception as e:
            messagebox.showerror("Error al exportar", f"No se pudo generar el Excel:\n{e}")
    def export_pdf(self, tipo):
        try:
            if tipo == "alumnos":
                ruta = export_pdf.exportar_alumnos_pdf()
            elif tipo == "cursos":
                ruta = export_pdf.exportar_cursos_pdf()
            elif tipo == "matriculas":
                ruta = export_pdf.exportar_matriculas_pdf()
            else:
                messagebox.showwarning("Aviso", "Tipo no reconocido.")
                return
            messagebox.showinfo("Exportar a PDF", f"Archivo generado correctamente:\n{ruta}")
        except Exception as e:
            messagebox.showerror("Error al exportar", f"No se pudo generar el PDF:\n{e}")
    def import_excel(self, tipo):
        ruta = filedialog.askopenfilename(
            title="Seleccionar archivo Excel",
            filetypes=[("Archivos Excel", "*.xlsx")]
        )
        if not ruta:
            return
        try:
            if tipo == "alumnos":
                resumen = import_utils.importar_alumnos_desde_excel(ruta)
            elif tipo == "cursos":
                resumen = import_utils.importar_cursos_desde_excel(ruta)
            elif tipo == "matriculas":
                resumen = import_utils.importar_matriculas_desde_excel(ruta)
            else:
                messagebox.showwarning("Aviso", "Tipo no reconocido.")
                return
            nuevos = resumen["nuevos"]
            duplicados = resumen["duplicados"]
            entidad = resumen["entidad"].capitalize()
            mensaje = (
                f"Importación de {entidad} completada.\n\n"
                f"📥 Nuevos registros añadidos: {nuevos}\n"
                f"⚠️ Duplicados ignorados: {duplicados}\n\n"
                f"Origen del archivo:\n{ruta}"
            )
            messagebox.showinfo("Importación completada", mensaje)
        except Exception as e:
            messagebox.showerror("Error en importación", f"No se pudo importar el archivo:\n{e}")
    #--- Menú usuarios ---
    def manage_users(self): messagebox.showinfo("Usuarios", "Gestión de Usuarios (admin)")