import tkinter as tk
from tkinter import ttk
from ui.utils_style import aplicar_estilo_global


class MainMenuWindow(tk.Frame):
    def __init__(self, parent, usuario, rol, modo, callbacks, logout_callback):
        super().__init__(parent, bg=aplicar_estilo_global(modo)[1])
        self.modo = modo
        self.usuario = usuario
        self.rol = rol
        self.callbacks = callbacks
        self.logout_callback = logout_callback
        self._crear_interfaz()
        self.pack(fill="both", expand=True)

    def _crear_interfaz(self):
        _, bg_color = aplicar_estilo_global(self.modo)
        self.configure(bg=bg_color)
        # === CABECERA ===
        header = tk.Frame(self, bg=bg_color)
        header.pack(fill="x", pady=(10, 20))
        # Título principal
        tk.Label(
            header,
            text="💼 Gestor de Cursos",
            font=("Segoe UI", 18, "bold"),
            bg=bg_color,
            fg="#3E64FF"
        ).pack(side="left", padx=20)
        # === Menú desplegable de usuario ===
        self.menu_usuario = tk.Menu(self, tearoff=0)
        self.menu_usuario.add_command(label="✏️ Cambiar nombre de usuario", command=self.callbacks["editar_nombre"])
        self.menu_usuario.add_command(label="🔑 Cambiar contraseña", command=self.callbacks["cambiar_contra"])
        self.menu_usuario.add_separator()
        self.menu_usuario.add_command(label="🚪 Cerrar sesión", command=self.logout_callback)
        self.btn_usuario = ttk.Menubutton(
            header,
            text=f"👤 {self.usuario} ({self.rol})",
            direction="below",
            style="Custom.TMenubutton"
        )
        self.btn_usuario["menu"] = self.menu_usuario
        self.btn_usuario.pack(side="right", padx=20)
        # === BOTONES PRINCIPALES ===
        frame_botones = tk.Frame(self, bg=bg_color)
        frame_botones.pack(expand=True)
        botones = [
            ("🎓 Alumnos", self.callbacks["alumnos"]),
            ("📚 Cursos", self.callbacks["cursos"]),
            ("📜 Matrículas", self.callbacks["matriculas"]),
        ]
        if self.rol in ("admin", "god"):
            botones.append(("👥 Usuarios", self.callbacks["usuarios"]))
        if self.rol == "god":
            botones.append(("⚡ Panel GOD", self.callbacks["god"]))
        for i, (texto, comando) in enumerate(botones):
            ttk.Button(
                frame_botones,
                text=texto,
                command=comando,
                width=25
            ).grid(row=i // 2, column=i % 2, padx=25, pady=20)
        # === PIE ===
        tk.Label(
            self,
            text="Versión 1.0",
            bg=bg_color,
            fg="#999",
            font=("Segoe UI", 8)
        ).pack(side="bottom", pady=10)