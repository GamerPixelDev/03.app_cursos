import tkinter as tk
import os
from tkinter import messagebox, ttk, filedialog
from ui.utils_style import aplicar_estilo_global
from ui.alumnos_window import AlumnosWindows
from ui.cursos_window import CursosWindow
from ui.matriculas_window import MatriculasWindow
from ui.buscar_alumno_window import BuscarAlumnoWindow
from ui.buscar_curso_window import BuscarCursoWindow
from ui.usuarios_window import UsuariosWindow
from datetime import datetime
from models import export_utils, export_pdf, import_utils

class MainWindow:
    def __init__(self, usuario, rol):
        # === Configuración inicial ===
        self.root = tk.Tk()
        self.usuario = usuario
        self.rol = rol
        self.modo = "claro"  # modo por defecto
        # === Estilo global ===
        self.style, self.bg_color = aplicar_estilo_global(self.modo)
        self.root.configure(bg=self.bg_color)
        self.root.title(f"Gestión de Cursos - Usuario: {usuario} ({rol})")
        self.root.geometry("1100x700")
        self.root.resizable(True, True)
        # === Banner superior ===
        self._crear_banner_superior()
        # === Menú principal ===
        self._crear_menus()
        # === Separador ===
        ttk.Separator(self.root, orient="horizontal").pack(fill="x")
        # === Footer ===
        self._crear_footer()
        self.root.mainloop()
    # -------------------------------------------------
    # Banner superior
    # -------------------------------------------------
    def _crear_banner_superior(self):
        banner = tk.Frame(self.root, bg="#3E64FF", height=60)
        banner.pack(fill="x", side="top")
        # Título
        tk.Label(
            banner,
            text="💼 Gestor de Cursos",
            bg="#3E64FF",
            fg="white",
            font=("Segoe UI", 14, "bold")
        ).pack(side="left", padx=10)
        # Usuario
        tk.Label(
            banner,
            text=f"👤 {self.usuario} ({self.rol})",
            bg="#3E64FF",
            fg="white",
            font=("Segoe UI", 10, "italic")
        ).pack(side="right", padx=15)
        # Botón cambio modo (🌞 / 🌙)
        self.icon_modo = tk.Label(
            banner,
            text="🌞",
            bg="#3E64FF",
            fg="white",
            font=("Segoe UI", 16)
        )
        self.icon_modo.pack(side="right", padx=10)
        self.icon_modo.bind("<Button-1>", self.toggle_modo)
        self.icon_modo.config(cursor="hand2")
    # -------------------------------------------------
    # Menús
    # -------------------------------------------------
    def _crear_menus(self):
        menu_bar = tk.Menu(self.root)
        # === Alumnos ===
        menu_alumnos = tk.Menu(menu_bar, tearoff=0)
        menu_alumnos.add_command(label="Ver alumnos", command=self.ver_alumnos)
        menu_alumnos.add_command(label="Buscar alumno", command=self.buscar_alumno)
        menu_alumnos.add_command(label="Añadir alumno", command=self.add_alumno)
        # Submenú Exportar
        submenu_export_alumnos = tk.Menu(menu_alumnos, tearoff=0)
        submenu_export_alumnos.add_command(label="Excel", command=lambda: self.export_excel("alumnos"))
        submenu_export_alumnos.add_command(label="PDF", command=lambda: self.export_pdf("alumnos"))
        menu_alumnos.add_cascade(label="Exportar", menu=submenu_export_alumnos)
        # Submenú Importar
        submenu_import_alumnos = tk.Menu(menu_alumnos, tearoff=0)
        submenu_import_alumnos.add_command(label="Desde Excel", command=lambda: self.import_excel("alumnos"))
        menu_alumnos.add_cascade(label="Importar", menu=submenu_import_alumnos)
        menu_bar.add_cascade(label="🎓 Alumnos", menu=menu_alumnos)
        # === Cursos ===
        menu_cursos = tk.Menu(menu_bar, tearoff=0)
        menu_cursos.add_command(label="Ver cursos", command=self.ver_cursos)
        menu_cursos.add_command(label="Buscar curso", command=self.buscar_curso)
        menu_cursos.add_command(label="Añadir curso", command=self.add_curso)
        # Submenú Exportar
        submenu_export_cursos = tk.Menu(menu_cursos, tearoff=0)
        submenu_export_cursos.add_command(label="Excel", command=lambda: self.export_excel("cursos"))
        submenu_export_cursos.add_command(label="PDF", command=lambda: self.export_pdf("cursos"))
        menu_cursos.add_cascade(label="Exportar", menu=submenu_export_cursos)
        # Submenú Importar
        submenu_import_cursos = tk.Menu(menu_cursos, tearoff=0)
        submenu_import_cursos.add_command(label="Desde Excel", command=lambda: self.import_excel("cursos"))
        menu_cursos.add_cascade(label="Importar", menu=submenu_import_cursos)
        menu_bar.add_cascade(label="📚 Cursos", menu=menu_cursos)
        # === Matrículas ===
        menu_matriculas = tk.Menu(menu_bar, tearoff=0)
        menu_matriculas.add_command(label="Ver Matrículas", command=self.ver_matriculas)
        menu_matriculas.add_command(label="Agregar Matrícula", command=self.add_matricula)
        # Submenú Exportar
        submenu_export_matriculas = tk.Menu(menu_matriculas, tearoff=0)
        submenu_export_matriculas.add_command(label="Excel", command=lambda: self.export_excel("matriculas"))
        submenu_export_matriculas.add_command(label="PDF", command=lambda: self.export_pdf("matriculas"))
        menu_matriculas.add_cascade(label="Exportar", menu=submenu_export_matriculas)
        # Submenú Importar
        submenu_import_matriculas = tk.Menu(menu_matriculas, tearoff=0)
        submenu_import_matriculas.add_command(label="Desde Excel", command=lambda: self.import_excel("matriculas"))
        menu_matriculas.add_cascade(label="Importar", menu=submenu_import_matriculas)
        menu_bar.add_cascade(label="📜 Matrículas", menu=menu_matriculas)
        # === Usuarios (solo admin) ===
        if self.rol == "admin":
            menu_usuarios = tk.Menu(menu_bar, tearoff=0)
            menu_usuarios.add_command(label="Gestionar Usuarios", command=self.manage_users)
            menu_bar.add_cascade(label="👥 Usuarios", menu=menu_usuarios)
        # === Salir ===
        menu_bar.add_command(label="Salir", command=self.root.quit)

        self.root.config(menu=menu_bar)

    # -------------------------------------------------
    # Footer
    # -------------------------------------------------
    def _crear_footer(self):
        footer = tk.Frame(self.root, bg="#E9ECEF", height=25)
        footer.pack(fill="x", side="bottom")
        tk.Label(
            footer,
            text=f"Versión 1.0 · {datetime.now().strftime('%d/%m/%Y %H:%M')}",
            bg="#E9ECEF",
            fg="#555555",
            font=("Segoe UI", 9)
        ).pack(side="right", padx=10)

    # -------------------------------------------------
    # Métodos de acción
    # -------------------------------------------------
    def ver_alumnos(self): AlumnosWindows(self.root, self.modo)
    def buscar_alumno(self): BuscarAlumnoWindow(self.root, self.modo)
    def add_alumno(self): messagebox.showinfo("Alumnos", "Agregar Alumno (admin)")

    def ver_cursos(self): CursosWindow(self.root, self.modo)
    def buscar_curso(self): BuscarCursoWindow(self.root, self.modo)
    def add_curso(self): messagebox.showinfo("Cursos", "Agregar Curso (admin)")

    def ver_matriculas(self): MatriculasWindow(self.root, self.modo)
    def add_matricula(self): messagebox.showinfo("Matrículas", "Agregar Matrícula (admin)")
    # -------------------------------------------------
    # Exportar / Importar
    # -------------------------------------------------
    def export_excel(self, tipo):
        try:
            rutas = {
                "alumnos": export_utils.exportar_alumnos_excel,
                "cursos": export_utils.exportar_cursos_excel,
                "matriculas": export_utils.exportar_matriculas_excel
            }
            if tipo in rutas:
                ruta = rutas[tipo]()
                messagebox.showinfo("Exportar a Excel", f"Archivo generado correctamente:\n{ruta}")
            else:
                messagebox.showwarning("Aviso", "Tipo no reconocido.")
        except Exception as e:
            messagebox.showerror("Error al exportar", f"No se pudo generar el Excel:\n{e}")

    def export_pdf(self, tipo):
        try:
            rutas = {
                "alumnos": export_pdf.exportar_alumnos_pdf,
                "cursos": export_pdf.exportar_cursos_pdf,
                "matriculas": export_pdf.exportar_matriculas_pdf
            }
            if tipo in rutas:
                ruta = rutas[tipo]()
                messagebox.showinfo("Exportar a PDF", f"Archivo generado correctamente:\n{ruta}")
            else:
                messagebox.showwarning("Aviso", "Tipo no reconocido.")
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
            funciones = {
                "alumnos": import_utils.importar_alumnos_desde_excel,
                "cursos": import_utils.importar_cursos_desde_excel,
                "matriculas": import_utils.importar_matriculas_desde_excel
            }
            if tipo in funciones:
                resumen = funciones[tipo](ruta)
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
            else:
                messagebox.showwarning("Aviso", "Tipo no reconocido.")
        except Exception as e:
            messagebox.showerror("Error en importación", f"No se pudo importar el archivo:\n{e}")
    # -------------------------------------------------
    # Gestión de usuarios
    # -------------------------------------------------
    def manage_users(self): UsuariosWindow(self.root, self.modo, rol_actual=self.rol)
    # -------------------------------------------------
    # Tema claro / oscuro
    # -------------------------------------------------
    def toggle_modo(self, event=None):
        self.modo = "oscuro" if self.modo == "claro" else "claro"
        self.style, self.bg_color = aplicar_estilo_global(self.modo)
        self.root.configure(bg=self.bg_color)
        self.icon_modo.config(text="🌙" if self.modo == "oscuro" else "🌞")
