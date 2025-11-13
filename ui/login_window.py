import tkinter as tk
from tkinter import ttk, messagebox
from models.usuarios import autenticar_usuario
#from models.usuarios import iniciar_admin, iniciar_god
from ui.main_window import MainWindow
from ui.utils_style import aplicar_estilo_global

class LoginWindow:
    def __init__(self, modo="claro"):
        self.modo = modo
        # === Inicializar usuarios base si no existen === (De momento no se usa ya)
        #try:
        #    iniciar_admin()
        #    iniciar_god()
        #except Exception as e:
        #    print(f"[ERROR] No se pudieron crear usuarios base: {e}")
        # === Ventana principal ===
        self.root = tk.Tk()
        self.style, self.bg_color = aplicar_estilo_global(modo)
        self.root.configure(bg=self.bg_color)
        self.root.title("Inicio de sesión")
        self.root.geometry("380x380")
        self.root.resizable(False, False)
        # Centrar ventana en pantalla
        self.root.update_idletasks()
        ancho = 380
        alto = 300
        x = (self.root.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.root.winfo_screenheight() // 2) - (alto // 2)
        self.root.geometry(f"{ancho}x{alto}+{x}+{y}")
        # === Frame principal ===
        frame = tk.Frame(self.root, bg=self.bg_color)
        frame.pack(expand=True, padx=20, pady=20)
        # === Título ===
        lbl_titulo = tk.Label(
            frame,
            text="🔐 Inicio de sesión",
            font=("Segoe UI", 14, "bold"),
            bg=self.bg_color,
            fg="#3E64FF"
        )
        lbl_titulo.pack(pady=(0, 15))
        # === Campo usuario ===
        lbl_usuario = tk.Label(
            frame,
            text="Usuario:",
            font=("Segoe UI", 10),
            bg=self.bg_color
        )
        lbl_usuario.pack(anchor="w")
        self.entry_usuario = ttk.Entry(frame, width=30)
        self.entry_usuario.pack(pady=(0, 10))
        # === Campo contraseña ===
        lbl_pass = tk.Label(
            frame,
            text="Contraseña:",
            font=("Segoe UI", 10),
            bg=self.bg_color
        )
        lbl_pass.pack(anchor="w")
        self.entry_contraseña = ttk.Entry(frame, width=30, show="•")
        self.entry_contraseña.pack(pady=(0, 15))
        # === Botón de inicio ===
        ttk.Button(
            frame,
            text="Iniciar sesión",
            command=self.iniciar_sesion
        ).pack(pady=5)
        # === Pie de ventana ===
        lbl_pie = tk.Label(
            self.root,
            text="Gestor de Cursos © 2025",
            font=("Segoe UI", 8),
            fg="#666",
            bg=self.bg_color
        )
        lbl_pie.pack(side="bottom", pady=5)
        # Ejecutar
        self.root.mainloop()

    # === Iniciar sesión ===
    def iniciar_sesion(self):
        usuario = self.entry_usuario.get().strip()
        contraseña = self.entry_contraseña.get().strip()
        if not usuario or not contraseña:
            messagebox.showwarning("Aviso", "Introduce usuario y contraseña.")
            return
        valido, rol = autenticar_usuario(usuario, contraseña)
        if valido:
            self.root.destroy()
            MainWindow(usuario, rol)
        else:
            messagebox.showerror("Acceso denegado", "Usuario o contraseña incorrectos.")