import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from ui.utils_style import aplicar_estilo_global
from models import usuarios as model_usuarios
import os


class MiCuentaWindow(tk.Toplevel):
    def __init__(self, parent, usuario, modo="claro"):
        super().__init__(parent)
        self.usuario = usuario
        self.modo = modo
        # Estilo
        self.style, self.bg_color = aplicar_estilo_global(modo)
        self.configure(bg=self.bg_color)
        self.title("Mi cuenta")
        self.geometry("450x500")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        # ======== TITULO ========
        tk.Label(
            self,
            text="⚙️ Configuración de la cuenta",
            font=("Segoe UI", 13, "bold"),
            bg=self.bg_color,
            fg="#3E64FF"
        ).pack(pady=15)
        # ======== CARD PRINCIPAL ========
        frame = ttk.Frame(self, style="Card.TFrame")
        frame.pack(padx=20, pady=10, fill="both", expand=True)
        # Obtener datos del usuario
        self._cargar_datos_usuario()
        # ---------- CAMPOS ----------
        lbl_cfg = ttk.Label(frame, text="Datos personales", font=("Segoe UI", 11, "bold"))
        lbl_cfg.grid(row=0, column=0, columnspan=2, pady=(10, 15))
        ttk.Label(frame, text="Usuario:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.entry_usuario = ttk.Entry(frame, width=30, state="readonly")
        self.entry_usuario.insert(0, self.usuario)
        self.entry_usuario.grid(row=1, column=1, padx=10, pady=5)
        ttk.Label(frame, text="Nombre completo:").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.entry_nombre = ttk.Entry(frame, width=30)
        self.entry_nombre.insert(0, self.nombre_actual)
        self.entry_nombre.grid(row=2, column=1, padx=10, pady=5)
        ttk.Label(frame, text="Email:").grid(row=3, column=0, sticky="w", padx=10, pady=5)
        self.entry_email = ttk.Entry(frame, width=30)
        self.entry_email.insert(0, self.email_actual)
        self.entry_email.grid(row=3, column=1, padx=10, pady=5)
        ttk.Label(frame, text="Rol:").grid(row=4, column=0, sticky="w", padx=10, pady=5)
        self.entry_rol = ttk.Entry(frame, width=30, state="readonly")
        self.entry_rol.insert(0, self.rol_actual)
        self.entry_rol.grid(row=4, column=1, padx=10, pady=5)
        # ---------- CAMBIO DE CONTRASEÑA ----------
        ttk.Label(frame, text="Cambiar contraseña", font=("Segoe UI", 11, "bold")).grid(
            row=5, column=0, columnspan=2, pady=(20, 10)
        )
        ttk.Label(frame, text="Contraseña actual:").grid(row=6, column=0, sticky="w", padx=10, pady=5)
        self.entry_pass_actual = ttk.Entry(frame, width=30, show="•")
        self.entry_pass_actual.grid(row=6, column=1, padx=10, pady=5)
        ttk.Label(frame, text="Nueva contraseña:").grid(row=7, column=0, sticky="w", padx=10, pady=5)
        self.entry_pass_nueva = ttk.Entry(frame, width=30, show="•")
        self.entry_pass_nueva.grid(row=7, column=1, padx=10, pady=5)
        # ---------- EXPORT PATH ----------
        ttk.Label(frame, text="Ruta exportaciones:", font=("Segoe UI", 11, "bold")).grid(
            row=8, column=0, columnspan=2, pady=(20, 10)
        )
        self.entry_ruta = ttk.Entry(frame, width=30)
        self.entry_ruta.insert(0, self.ruta_export)
        self.entry_ruta.grid(row=9, column=0, padx=10, pady=5)
        ttk.Button(frame, text="Cambiar ruta", command=self._seleccionar_ruta).grid(
            row=9, column=1, pady=5
        )
        # ---------- BOTÓN GUARDAR ----------
        ttk.Button(self, text="💾 Guardar cambios", command=self._guardar_cambios).pack(pady=15)

    #   CARGAR DATOS DEL USUARIO DESDE BBDD
    def _cargar_datos_usuario(self):
        datos = model_usuarios.obtener_datos_usuario(self.usuario)
        if datos:
            self.nombre_actual = datos.get("nombre", "")
            self.email_actual = datos.get("email", "")
            self.rol_actual = datos.get("rol", "")
            self.ruta_export = datos.get("ruta_export", os.getcwd())
        else:
            self.nombre_actual = ""
            self.email_actual = ""
            self.rol_actual = ""
            self.ruta_export = os.getcwd()

    #   BOTÓN PARA SELECCIONAR NUEVA RUTA
    def _seleccionar_ruta(self):
        ruta = filedialog.askdirectory()
        if ruta:
            self.entry_ruta.delete(0, tk.END)
            self.entry_ruta.insert(0, ruta)

    #   GUARDAR CAMBIOS EN DB
    def _guardar_cambios(self):
        nombre_nuevo = self.entry_nombre.get().strip()
        email_nuevo = self.entry_email.get().strip()
        ruta_nueva = self.entry_ruta.get().strip()
        # Validación básica
        if not nombre_nuevo:
            messagebox.showerror("Error", "El nombre no puede estar vacío.")
            return
        model_usuarios.actualizar_datos_usuario(
            self.usuario,
            nombre_nuevo,
            email_nuevo,
            ruta_nueva
        )
        # Cambiar contraseña si procede
        pass_actual = self.entry_pass_actual.get().strip()
        pass_nueva = self.entry_pass_nueva.get().strip()
        if pass_actual or pass_nueva:
            ok = model_usuarios.verificar_contrasena(self.usuario, pass_actual)
            if not ok:
                messagebox.showerror("Error", "La contraseña actual no es correcta.")
                return
            model_usuarios.cambiar_contrasena(self.usuario, pass_nueva)
        messagebox.showinfo("Éxito", "Cambios guardados correctamente.")
        self.destroy()
