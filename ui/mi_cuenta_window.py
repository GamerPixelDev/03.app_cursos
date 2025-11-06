import tkinter as tk
from tkinter import ttk, messagebox
from models import usuarios as model
from ui.utils_style import aplicar_estilo_global
import bcrypt

class MiCuentaWindow(tk.Toplevel):
    def __init__(self, parent, usuario, modo="claro"):
        super().__init__(parent)
        self.usuario = usuario
        self.modo = modo
        # === Estilo global ===
        self.style, self.bg_color = aplicar_estilo_global(modo)
        self.configure(bg=self.bg_color)
        self.title("Mi cuenta")
        self.geometry("500x300")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        # === Encabezado ===
        tk.Label(
            self,
            text=f"🔐 Cambiar contraseña de {usuario}",
            font=("Segoe UI", 13, "bold"),
            fg="#3E64FF",
            bg=self.bg_color
        ).pack(pady=(20, 10))
        # === Frame del formulario ===
        frame = tk.Frame(self, bg=self.bg_color)
        frame.pack(padx=20, pady=20)
        tk.Label(frame, text="Contraseña actual:", font=("Segoe UI", 10), bg=self.bg_color).grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.entry_actual = ttk.Entry(frame, width=30, show="*")
        self.entry_actual.grid(row=0, column=1, padx=5, pady=5)
        tk.Label(frame, text="Nueva contraseña:", font=("Segoe UI", 10), bg=self.bg_color).grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.entry_nueva = ttk.Entry(frame, width=30, show="*")
        self.entry_nueva.grid(row=1, column=1, padx=5, pady=5)
        tk.Label(frame, text="Confirmar nueva:", font=("Segoe UI", 10), bg=self.bg_color).grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.entry_confirma = ttk.Entry(frame, width=30, show="*")
        self.entry_confirma.grid(row=2, column=1, padx=5, pady=5)
        ttk.Button(
            self,
            text="💾 Guardar cambios",
            command=self.cambiar_contrasena
        ).pack(pady=20)

    def cambiar_contrasena(self):
        actual = self.entry_actual.get().strip()
        nueva = self.entry_nueva.get().strip()
        confirma = self.entry_confirma.get().strip()
        if not actual or not nueva or not confirma:
            messagebox.showwarning("Campos vacíos", "Rellena todos los campos.")
            return
        if nueva != confirma:
            messagebox.showwarning("No coincide", "Las contraseñas nuevas no coinciden.")
            return
        # Verificar contraseña actual usando bcrypt
        conn = model.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT contraseña FROM usuarios WHERE nombre = ?", (self.usuario,))
        fila = cur.fetchone()
        conn.close()
        if not fila:
            messagebox.showerror("Error", "Usuario no encontrado en la base de datos.")
            return
        hashed_guardado = fila[0]
        if not bcrypt.checkpw(actual.encode('utf-8'), hashed_guardado):
            messagebox.showerror("Error", "La contraseña actual es incorrecta.")
            return
        # Guardar nueva contraseña (re-hash)
        nuevo_hash = bcrypt.hashpw(nueva.encode('utf-8'), bcrypt.gensalt())
        conn = model.get_connection()
        cur = conn.cursor()
        cur.execute("UPDATE usuarios SET contraseña = ? WHERE nombre = ?", (nuevo_hash, self.usuario))
        conn.commit()
        conn.close()
        messagebox.showinfo("Éxito", "Contraseña actualizada correctamente.")
        self.destroy()
