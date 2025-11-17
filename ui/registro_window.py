import tkinter as tk
from tkinter import ttk, messagebox
from ui.utils_style import aplicar_estilo_global
from models.usuarios import crear_usuario


class RegistroWindow(tk.Toplevel):
    def __init__(self, parent, modo="claro"):
        super().__init__(parent)
        self.modo = modo
        self.style, self.bg_color = aplicar_estilo_global(modo)
        self.title("Crear nueva cuenta")
        self.geometry("420x380")
        self.resizable(False, False)
        self.configure(bg=self.bg_color)
        self.transient(parent)
        self.grab_set()
        # --------- Título ---------
        tk.Label(
            self,
            text="📝 Registro de usuario",
            bg=self.bg_color,
            fg="#3E64FF",
            font=("Segoe UI", 15, "bold")
        ).pack(pady=(15, 5))
        # --------- Contenedor ---------
        frame = tk.Frame(self, bg=self.bg_color)
        frame.pack(padx=20, pady=10, fill="both")
        # Campos
        campos = [
            ("Usuario", False),
            ("Contraseña", True),
            ("Confirmar contraseña", True),
            ("Email", False)
        ]
        self.entries = {}
        for i, (label, ocultar) in enumerate(campos):
            tk.Label(
                frame,
                text=label + ":",
                bg=self.bg_color,
                font=("Segoe UI", 10)
            ).grid(row=i, column=0, sticky="w", pady=8)
            entry = ttk.Entry(frame, width=30, show="•" if ocultar else "")
            entry.grid(row=i, column=1, pady=8)
            clave = label.lower().replace(" ", "_")
            self.entries[clave] = entry
        # --------- Botón registrar ---------
        ttk.Button(
            self,
            text="Crear cuenta",
            command=self._registrar
        ).pack(pady=15)

    # ======= Registro real =======
    def _registrar(self):
        usuario = self.entries["usuario"].get().strip()
        password = self.entries["contraseña"].get().strip()
        confirm = self.entries["confirmar_contraseña"].get().strip()
        email = self.entries["email"].get().strip()
        # Validaciones básicas
        if not usuario or not password or not confirm or not email:
            messagebox.showerror("Error", "Rellena todos los campos.")
            return
        if password != confirm:
            messagebox.showwarning("Error", "Las contraseñas no coinciden.")
            return
        # Crear usuario con rol por defecto
        try:
            crear_usuario(usuario, password, "usuario", email=email)
            messagebox.showinfo("Éxito", "Usuario creado correctamente.")
            self.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo crear el usuario:\n{e}")
