import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from ui.utils_style import aplicar_estilo_global
from models import usuarios as model_usuarios


class MiCuentaWindow(tk.Toplevel):
    def __init__(self, parent, usuario, modo="claro"):
        super().__init__(parent)
        self.usuario = usuario
        self.modo = modo
        # Estilo
        self.style, self.bg_color = aplicar_estilo_global(modo)
        self.configure(bg=self.bg_color)
        self.title("Mi cuenta")
        self.geometry("420x350")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        # ======= Título =======
        tk.Label(
            self,
            text=f"⚙️ Mi cuenta — {usuario}",
            font=("Segoe UI", 12, "bold"),
            fg="#3E64FF",
            bg=self.bg_color
        ).pack(pady=(10, 15))
        frame = tk.Frame(self, bg=self.bg_color)
        frame.pack(padx=20, pady=10, fill="both", expand=True)
        # CAMPO: NOMBRE USUARIO
        ttk.Label(frame, text="Nombre de usuario:", background=self.bg_color).grid(
            row=0, column=0, sticky="w", pady=5
        )
        self.entry_nombre = ttk.Entry(frame, width=28)
        self.entry_nombre.grid(row=0, column=1, pady=5)
        self.entry_nombre.insert(0, usuario)
        # CAMBIO DE CONTRASEÑA
        ttk.Label(frame, text="Nueva contraseña:", background=self.bg_color).grid(
            row=1, column=0, sticky="w", pady=5
        )
        self.entry_pass1 = ttk.Entry(frame, width=28, show="•")
        self.entry_pass1.grid(row=1, column=1, pady=5)
        ttk.Label(frame, text="Repetir contraseña:", background=self.bg_color).grid(
            row=2, column=0, sticky="w", pady=5
        )
        self.entry_pass2 = ttk.Entry(frame, width=28, show="•")
        self.entry_pass2.grid(row=2, column=1, pady=5)
        # CARPETA EXPORTACIÓN
        ttk.Label(frame, text="Carpeta exportación:", background=self.bg_color).grid(
            row=3, column=0, sticky="w", pady=10
        )
        self.export_path_var = tk.StringVar(value=model_usuarios.obtener_carpeta_exportacion(usuario))
        ttk.Entry(frame, width=28, textvariable=self.export_path_var).grid(
            row=3, column=1, pady=10, sticky="w"
        )
        ttk.Button(frame, text="📁 Elegir carpeta", command=self.elegir_carpeta).grid(
            row=3, column=2, padx=5
        )
        # BOTÓN GUARDAR
        ttk.Button(
            self,
            text="💾 Guardar cambios",
            command=self.guardar_cambios
        ).pack(pady=(10, 10))

    # Elegir carpeta exportación
    def elegir_carpeta(self):
        carpeta = filedialog.askdirectory(title="Elegir carpeta de exportación")
        if carpeta:
            self.export_path_var.set(carpeta)

    # Guardar cambios
    def guardar_cambios(self):
        nuevo_nombre = self.entry_nombre.get().strip()
        pass1 = self.entry_pass1.get().strip()
        pass2 = self.entry_pass2.get().strip()
        carpeta = self.export_path_var.get().strip()
        # Cambiar nombre
        if nuevo_nombre and nuevo_nombre != self.usuario:
            ok = model_usuarios.cambiar_nombre(self.usuario, nuevo_nombre)
            if ok:
                messagebox.showinfo("Nombre actualizado", "Nombre de usuario cambiado correctamente.")
                self.usuario = nuevo_nombre
            else:
                messagebox.showerror("Error", "No se pudo cambiar el nombre.")
        # Cambiar contraseña
        if pass1 or pass2:
            if pass1 != pass2:
                messagebox.showwarning("Contraseña", "Las contraseñas no coinciden.")
                return
            if len(pass1) < 4:
                messagebox.showwarning("Contraseña", "Debe tener al menos 4 caracteres.")
                return
            model_usuarios.cambiar_contraseña(self.usuario, pass1)
            messagebox.showinfo("Contraseña", "Contraseña actualizada correctamente.")
        # Guardar carpeta exportación
        model_usuarios.guardar_carpeta_exportacion(self.usuario, carpeta)
        self.destroy()
