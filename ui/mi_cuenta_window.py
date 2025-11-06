import tkinter as tk
from tkinter import ttk, messagebox
from models import usuarios as model
from ui.utils_style import aplicar_estilo_global

class MiCuentaWindow(tk.Toplevel):
    def __init__(self, parent, usuario, modo="claro"):
        super().__init__(parent)
        self.usuario = usuario
        self.modo = modo
        self.style, self.bg_color = aplicar_estilo_global(modo)
        self.configure(bg=self.bg_color)
        self.title("Mi cuenta")
        self.geometry("400x250")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        # === Encabezado ===
        tk.Label(
            self,
            text=f"🔐 Cambiar contraseña ({usuario})",
            font=("Segoe UI", 12, "bold"),
            fg="#3E64FF",
            bg=self.bg_color
        ).pack(pady=(15, 10))
        # === Formulario ===
        frame = tk.Frame(self, bg=self.bg_color)
        frame.pack(padx=10, pady=10)
        ttk.Label(frame, text="Contraseña actual:", background=self.bg_color).grid(row=0, column=0, sticky="w", padx=5, pady=5)
        entry_actual = ttk.Entry(frame, width=25, show="*")
        entry_actual.grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(frame, text="Nueva contraseña:", background=self.bg_color).grid(row=1, column=0, sticky="w", padx=5, pady=5)
        entry_nueva = ttk.Entry(frame, width=25, show="*")
        entry_nueva.grid(row=1, column=1, padx=5, pady=5)
        ttk.Label(frame, text="Confirmar nueva:", background=self.bg_color).grid(row=2, column=0, sticky="w", padx=5, pady=5)
        entry_confirma = ttk.Entry(frame, width=25, show="*")
        entry_confirma.grid(row=2, column=1, padx=5, pady=5)
        ttk.Button(
            self,
            text="💾 Guardar cambios",
            command=lambda: self.cambiar_contrasena(entry_actual.get(), entry_nueva.get(), entry_confirma.get())
        ).pack(pady=15)

    def cambiar_contrasena(self, actual, nueva, confirma):
        if not actual or not nueva:
            messagebox.showwarning("Campos vacíos", "Rellena todos los campos.")
            return
        if nueva != confirma:
            messagebox.showwarning("No coincide", "Las contraseñas nuevas no coinciden.")
            return
        if not model.verificar_contrasena(self.usuario, actual):
            messagebox.showerror("Error", "La contraseña actual es incorrecta.")
            return
        model.cambiar_contrasena(self.usuario, nueva)
        messagebox.showinfo("Éxito", "Contraseña actualizada correctamente.")
        self.destroy()
