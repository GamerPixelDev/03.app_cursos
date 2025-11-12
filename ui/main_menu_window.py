import tkinter as tk
from tkinter import ttk
from ui.utils_style import aplicar_estilo_global

class MainMenuWindow(tk.Frame):
    def __init__(self, parent, usuario, rol, modo, callbacks):
        super().__init__(parent, bg=aplicar_estilo_global(modo)[1])
        self.modo = modo
        self.usuario = usuario
        self.rol = rol
        self.callbacks = callbacks
        self._crear_interfaz()
        self.pack(fill="both", expand=True)

    def _crear_interfaz(self):
        _, bg_color = aplicar_estilo_global(self.modo)
        self.configure(bg=bg_color)
        tk.Label(
            self,
            text="💼 Gestor de Cursos",
            font=("Segoe UI", 18, "bold"),
            bg=bg_color,
            fg="#3E64FF"
        ).pack(pady=(20, 10))
        tk.Label(
            self,
            text=f"Bienvenido, {self.usuario} ({self.rol})",
            font=("Segoe UI", 10, "italic"),
            bg=bg_color,
            fg="#555"
        ).pack(pady=(0, 30))
        botones = [
            ("🎓 Alumnos", self.callbacks["alumnos"]),
            ("📚 Cursos", self.callbacks["cursos"]),
            ("📜 Matrículas", self.callbacks["matriculas"]),
            ("👤 Mi cuenta", self.callbacks["cuenta"]),
        ]
        if self.rol in ("admin", "god"):
            botones.append(("👥 Usuarios", self.callbacks["usuarios"]))
        if self.rol == "god":
            botones.append(("⚡ Panel GOD", self.callbacks["god"]))
        botones.append(("🚪 Salir", self.callbacks["salir"]))
        frame_botones = tk.Frame(self, bg=bg_color)
        frame_botones.pack(expand=True)
        for i, (texto, comando) in enumerate(botones):
            ttk.Button(
                frame_botones,
                text=texto,
                command=comando,
                width=25
            ).grid(row=i // 2, column=i % 2, padx=20, pady=15)
        tk.Label(
            self,
            text="Versión 1.0",
            bg=bg_color,
            fg="#999",
            font=("Segoe UI", 8)
        ).pack(side="bottom", pady=10)