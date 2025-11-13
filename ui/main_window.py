import tkinter as tk
from tkinter import messagebox, ttk, filedialog
from ui.utils_style import aplicar_estilo_global
from ui.alumnos_window import AlumnosWindows
from ui.cursos_window import CursosWindow
from ui.matriculas_window import MatriculasWindow
from ui.buscar_alumno_window import BuscarAlumnoWindow
from ui.buscar_curso_window import BuscarCursoWindow
from ui.usuarios_window import UsuariosWindow
from ui.mi_cuenta_window import MiCuentaWindow
from ui.god_panel_window import GodPanelWindow
from ui.main_menu_window import MainMenuWindow
from datetime import datetime
from models import export_utils, export_pdf, import_utils

class MainWindow:
    def __init__(self, usuario, rol):
        self.root = tk.Tk()
        self.usuario = usuario
        self.rol = rol
        self.modo = "claro"
        # === Estilo ===
        self.style, self.bg_color = aplicar_estilo_global(self.modo)
        self.root.configure(bg=self.bg_color)
        self.root.title(f"Gestión de Cursos - Usuario: {usuario} ({rol})")
        self.root.geometry("1100x700")
        self.root.resizable(True, True)
        # === Menú del usuario (Mi cuenta / Cerrar sesión) ===
        self._crear_menu_usuario()
        # === Banner ===
        self._crear_banner_superior()
        # === Menús ===
        self._crear_menus()
        # === Separador ===
        ttk.Separator(self.root, orient="horizontal").pack(fill="x")
        # Menú visual principal
        self.menu_principal = MainMenuWindow(
            self.root,
            usuario=self.usuario,
            rol=self.rol,
            modo=self.modo,
            callbacks={
                "alumnos": lambda: self.ver_alumnos(),
                "cursos": lambda: self.ver_cursos(),
                "matriculas": lambda: self.ver_matriculas(),
                "usuarios": lambda: self.gestion_usuarios(),
                "god": lambda: self.panel_god(),
                "editar_nombre": lambda: messagebox.showinfo("En desarrollo", "Funcionalidad para cambiar nombre próximamente."),
                "cambiar_contra": lambda: self.mi_cuenta(),
            },
            logout_callback=self.logout
        )
        # === Footer ===
        self._crear_footer()
        self.root.mainloop()

    # === Menú desplegable del usuario (Mi cuenta / Cerrar sesión) ===
    def _crear_menu_usuario(self):
        self.menu_usuario = tk.Menu(self.root, tearoff=0)
        self.menu_usuario.add_command(label="Mi cuenta", command=self.mi_cuenta)
        self.menu_usuario.add_separator()
        self.menu_usuario.add_command(label="Cerrar sesión", command=self.logout)

    def _mostrar_menu_usuario(self, event=None):
        # Mostrar el menú justo debajo de la etiqueta del usuario
        x = self.lbl_usuario.winfo_rootx()
        y = self.lbl_usuario.winfo_rooty() + self.lbl_usuario.winfo_height()
        try:
            self.menu_usuario.tk_popup(x, y)
        finally:
            self.menu_usuario.grab_release()

    def _hover_usuario(self, entrar: bool):
        # Efecto visual al pasar el ratón por encima del usuario
        base_bg = "#3E64FF"
        hover_bg = "#2f53e8"
        self.lbl_usuario.config(
            bg=hover_bg if entrar else base_bg,
            fg="white"
        )

    # Banner superior
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
        # Etiqueta de usuario con menú desplegable
        self.lbl_usuario = tk.Label(
            banner,
            text=f"👤 {self.usuario} ({self.rol})",
            bg="#3E64FF",
            fg="white",
            font=("Segoe UI", 10, "italic"),
            cursor="hand2"
        )
        self.lbl_usuario.pack(side="right", padx=15)
        # Eventos: click para mostrar menú, hover para resaltar
        self.lbl_usuario.bind("<Button-1>", self._mostrar_menu_usuario)
        self.lbl_usuario.bind("<Enter>", lambda e: self._hover_usuario(True))
        self.lbl_usuario.bind("<Leave>", lambda e: self._hover_usuario(False))
        # Botón modo claro/oscuro
        self.icon_modo = tk.Label(
            banner,
            text="🌞",
            bg="#3E64FF",
            fg="white",
            font=("Segoe UI", 16),
            cursor="hand2"
        )
        self.icon_modo.pack(side="right", padx=10)
        self.icon_modo.bind("<Button-1>", self.toggle_modo)

    # Menús principales
    def _crear_menus(self):
        menu_bar = tk.Menu(self.root)
        # === ALUMNOS ===
        menu_alumnos = tk.Menu(menu_bar, tearoff=0)
        menu_alumnos.add_command(label="Ver alumnos", command=self.ver_alumnos)
        menu_alumnos.add_command(label="Buscar alumno", command=self.buscar_alumno)
        submenu_export_alumnos = tk.Menu(menu_alumnos, tearoff=0)
        submenu_export_alumnos.add_command(label="Excel", command=lambda: self.export_excel("alumnos"))
        submenu_export_alumnos.add_command(label="PDF", command=lambda: self.export_pdf("alumnos"))
        menu_alumnos.add_cascade(label="Exportar", menu=submenu_export_alumnos)
        submenu_import_alumnos = tk.Menu(menu_alumnos, tearoff=0)
        submenu_import_alumnos.add_command(label="Desde Excel", command=lambda: self.import_excel("alumnos"))
        menu_alumnos.add_cascade(label="Importar", menu=submenu_import_alumnos)
        menu_bar.add_cascade(label="🎓 Alumnos", menu=menu_alumnos)
        # === CURSOS ===
        menu_cursos = tk.Menu(menu_bar, tearoff=0)
        menu_cursos.add_command(label="Ver cursos", command=self.ver_cursos)
        menu_cursos.add_command(label="Buscar curso", command=self.buscar_curso)
        submenu_export_cursos = tk.Menu(menu_cursos, tearoff=0)
        submenu_export_cursos.add_command(label="Excel", command=lambda: self.export_excel("cursos"))
        submenu_export_cursos.add_command(label="PDF", command=lambda: self.export_pdf("cursos"))
        menu_cursos.add_cascade(label="Exportar", menu=submenu_export_cursos)
        submenu_import_cursos = tk.Menu(menu_cursos, tearoff=0)
        submenu_import_cursos.add_command(label="Desde Excel", command=lambda: self.import_excel("cursos"))
        menu_cursos.add_cascade(label="Importar", menu=submenu_import_cursos)
        menu_bar.add_cascade(label="📚 Cursos", menu=menu_cursos)
        # === MATRÍCULAS ===
        menu_matriculas = tk.Menu(menu_bar, tearoff=0)
        menu_matriculas.add_command(label="Ver matrículas", command=self.ver_matriculas)
        submenu_export_matriculas = tk.Menu(menu_matriculas, tearoff=0)
        submenu_export_matriculas.add_command(label="Excel", command=lambda: self.export_excel("matriculas"))
        submenu_export_matriculas.add_command(label="PDF", command=lambda: self.export_pdf("matriculas"))
        menu_matriculas.add_cascade(label="Exportar", menu=submenu_export_matriculas)
        submenu_import_matriculas = tk.Menu(menu_matriculas, tearoff=0)
        submenu_import_matriculas.add_command(label="Desde Excel", command=lambda: self.import_excel("matriculas"))
        menu_matriculas.add_cascade(label="Importar", menu=submenu_import_matriculas)
        menu_bar.add_cascade(label="📜 Matrículas", menu=menu_matriculas)
        # === USUARIOS / CUENTA ===
        menu_usuarios = tk.Menu(menu_bar, tearoff=0)
        if self.rol in ("admin", "god"):
            menu_usuarios.add_command(label="Gestionar usuarios", command=self.gestion_usuarios)
        if self.rol == "god":
            menu_usuarios.add_separator()
            menu_usuarios.add_command(label="Panel GOD", command=self.panel_god)
        # Solo añadimos el menú si tiene algo
        if menu_usuarios.index("end") is not None:
            menu_bar.add_cascade(label="👥 Usuarios", menu=menu_usuarios)
        # === SALIR === -> ahora hace logout
        menu_bar.add_command(label="Salir", command=self.logout)

        self.root.config(menu=menu_bar)

    # Footer
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

    # Métodos de acción
    def ver_alumnos(self): AlumnosWindows(self.root, self.modo)
    def buscar_alumno(self): BuscarAlumnoWindow(self.root, self.modo)
    def ver_cursos(self): CursosWindow(self.root, self.modo)
    def buscar_curso(self): BuscarCursoWindow(self.root, self.modo)
    def ver_matriculas(self): MatriculasWindow(self.root, self.modo)
    # --- Usuarios / Roles ---
    def mi_cuenta(self): MiCuentaWindow(self.root, self.usuario, self.modo)
    def gestion_usuarios(self): UsuariosWindow(self.root, self.modo, rol_actual=self.rol)
    def panel_god(self): GodPanelWindow(self.root, self.modo)

    # Exportar / Importar
    def export_excel(self, tipo):
        try:
            rutas = {
                "alumnos": export_utils.exportar_alumnos_excel,
                "cursos": export_utils.exportar_cursos_excel,
                "matriculas": export_utils.exportar_matriculas_excel
            }
            ruta = rutas[tipo]()
            messagebox.showinfo("Exportar a Excel", f"Archivo generado correctamente:\n{ruta}")
        except Exception as e:
            messagebox.showerror("Error al exportar", str(e))
    def export_pdf(self, tipo):
        try:
            rutas = {
                "alumnos": export_pdf.exportar_alumnos_pdf,
                "cursos": export_pdf.exportar_cursos_pdf,
                "matriculas": export_pdf.exportar_matriculas_pdf
            }
            ruta = rutas[tipo]()
            messagebox.showinfo("Exportar a PDF", f"Archivo generado correctamente:\n{ruta}")
        except Exception as e:
            messagebox.showerror("Error al exportar", str(e))
    def import_excel(self, tipo):
        ruta = filedialog.askopenfilename(title="Seleccionar archivo Excel", filetypes=[("Archivos Excel", "*.xlsx")])
        if not ruta:
            return
        try:
            funciones = {
                "alumnos": import_utils.importar_alumnos_desde_excel,
                "cursos": import_utils.importar_cursos_desde_excel,
                "matriculas": import_utils.importar_matriculas_desde_excel
            }
            resumen = funciones[tipo](ruta)
            mensaje = (
                f"Importación completada.\n\n"
                f"📥 Nuevos: {resumen['nuevos']}\n"
                f"⚠️ Duplicados: {resumen['duplicados']}\n\n"
                f"Origen: {ruta}"
            )
            messagebox.showinfo("Importación completada", mensaje)
        except Exception as e:
            messagebox.showerror("Error en importación", str(e))

    # Modo claro / oscuro
    def toggle_modo(self, event=None):
        # Cambiar modo
        self.modo = "oscuro" if self.modo == "claro" else "claro"
        self.style, self.bg_color = aplicar_estilo_global(self.modo)
        # Repintar fondo general
        self.root.configure(bg=self.bg_color)
        # Repintar todos los frames/labels sin tocar banner azul
        from ui.utils_style import pintar_fondo_recursivo
        pintar_fondo_recursivo(self.root, self.bg_color)
        # Actualizar icono
        self.icon_modo.config(text="🌙" if self.modo == "oscuro" else "🌞")

    # === Cerrar sesión (logout) ===
    def logout(self):
        from ui.login_window import LoginWindow
        self.root.destroy()
        LoginWindow()  # vuelve a la ventana de login

    # Menú abrir Mi cuenta
    def abrir_mi_cuenta(self):
        from ui.mi_cuenta_window import MiCuentaWindow
        MiCuentaWindow(self.root, self.usuario, self.modo)
