import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from os import path
from ui.utils_style import aplicar_estilo_global
from models.usuarios import obtener_datos_usuario, actualizar_datos_usuario, verificar_contrasena, cambiar_contrasena

class MiCuentaWindow(tk.Toplevel):
    def __init__(self, parent, usuario, modo="claro"):
        super().__init__(parent)
        self.usuario = usuario
        self.modo = modo
        self.style, self.bg_color = aplicar_estilo_global(modo)
        self.configure(bg=self.bg_color)
        self.title("Mi cuenta")
        self.geometry("450x520")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        # === Cargamos TODO con 1 sola consulta ===
        datos = obtener_datos_usuario(self.usuario) # datos["usuario"], datos["email"], datos["rol"], datos["ruta_export"]
        # ========== TITULO PRINCIPAL ==========
        titulo = tk.Label(
            self,
            text="⚙️ Configuración de la cuenta",
            font=("Segoe UI", 14, "bold"),
            bg=self.bg_color,
            fg="#3E64FF"
        )
        titulo.pack(pady=(15, 5))
        # ========== USUARIO Y ROL CENTRADOS ==========
        lbl_user = tk.Label(
            self,
            text=datos["usuario"],
            font=("Segoe UI", 12, "bold"),
            bg=self.bg_color,
            fg="#1a1a1a"
        )
        lbl_user.pack(pady=(0, 2))
        lbl_rol = tk.Label(
            self,
            text=f"Rol: {datos["rol"]}",
            font=("Segoe UI", 10),
            bg=self.bg_color,
            fg="#555"
        )
        lbl_rol.pack(pady=(0, 10))
        # Contenedor principal
        card = tk.Frame(self, bg="white", bd=1, relief="solid")
        card.pack(padx=20, pady=10, fill="both", expand=False)
        # ========== DATOS PERSONALES ==========
        tk.Label(card, text="Datos personales",
                font=("Segoe UI", 11, "bold"),
                bg="white", fg="#3E64FF").pack(pady=(10, 5))
        form = tk.Frame(card, bg="white")
        form.pack(padx=15, pady=5)
        # Campo usuario (solo lectura)
        tk.Label(form, text="Usuario:", bg="white").grid(row=0, column=0, sticky="w")
        self.entry_usuario = ttk.Entry(form, width=30, state="readonly")
        self.entry_usuario.grid(row=0, column=1, pady=5)
        self.entry_usuario.insert(0, datos["usuario"])
        # Campo email
        tk.Label(form, text="Email:", bg="white").grid(row=1, column=0, sticky="w")
        self.entry_email = ttk.Entry(form, width=30)
        self.entry_email.grid(row=1, column=1, pady=5)
        self.entry_email.insert(0, datos["email"])
        # ========== CONTRASEÑA ==========
        tk.Label(card, text="Cambiar contraseña",
                font=("Segoe UI", 11, "bold"),
                bg="white", fg="#3E64FF").pack(pady=(15, 5))
        form_pass = tk.Frame(card, bg="white")
        form_pass.pack(padx=15, pady=5)
        tk.Label(form_pass, text="Contraseña actual:", bg="white").grid(row=0, column=0, sticky="w")
        self.pass_actual = ttk.Entry(form_pass, width=30, show="•")
        self.pass_actual.grid(row=0, column=1, pady=5)

        tk.Label(form_pass, text="Nueva contraseña:", bg="white").grid(row=1, column=0, sticky="w")
        self.pass_nueva = ttk.Entry(form_pass, width=30, show="•")
        self.pass_nueva.grid(row=1, column=1, pady=5)
        # ========== RUTA EXPORTACIONES ==========
        tk.Label(card, text="Ruta exportaciones",
                font=("Segoe UI", 11, "bold"),
                bg="white", fg="#3E64FF").pack(pady=(15, 5))
        ruta_frame = tk.Frame(card, bg="white")
        ruta_frame.pack(padx=10, pady=5)
        self.lbl_ruta_actual = tk.Label(
            ruta_frame,
            text=f"Actual: {datos["ruta_export"]}" or "(sin definir)",
            bg="white",
            fg="#555",
            anchor="center"
        )
        self.lbl_ruta_actual.pack(fill="x", pady=(0, 5))
        ttk.Button(
            ruta_frame,
            text="Cambiar ruta",
            command=self._cambiar_ruta_export
        ).pack(pady=5)
        # ========== BOTÓN GUARDAR ==========
        ttk.Button(
            self,
            text="💾 Guardar cambios",
            command=self._guardar_cambios
        ).pack(pady=15)

    # ====================================================
    #   MÉTODOS AUXILIARES (te los creo si no los tienes)
    # ====================================================
    def _cambiar_ruta_export(self):
        carpeta = filedialog.askdirectory(title="Seleccionar carpeta de exportación")
        if carpeta:
            self.datos["ruta_export"] = carpeta
            self.lbl_ruta_actual.config(text=f"Actual: {carpeta}")
    def _guardar_cambios(self):
        # Guardar email + ruta (con tu función ya existente)
        actualizar_datos_usuario(
            self.usuario,
            self.entry_email.get().strip(),
            self.datos["ruta_export"]
        )
        # Guardar contraseña si se ha cambiado
        if self.pass_nueva.get().strip():
            if not verificar_contrasena(self.usuario, self.pass_actual.get().strip()):
                messagebox.showerror("Error", "La contraseña actual es incorrecta.")
                return
            cambiar_contrasena(self.usuario, self.pass_nueva.get().strip())
        messagebox.showinfo("Éxito", "Datos actualizados correctamente.")
        self.destroy()
