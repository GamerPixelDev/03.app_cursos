import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from ui.utils_style import aplicar_estilo_global
from models.usuarios import (
    obtener_datos_usuario,
    actualizar_datos_usuario,
    verificar_contrasena,
    cambiar_contrasena
)

class MiCuentaWindow(tk.Toplevel):
    def __init__(self, parent, usuario, modo="claro"):
        super().__init__(parent)
        self.usuario = usuario
        self.modo = modo
        self.style, self.bg_color = aplicar_estilo_global(modo)
        # Datos desde BD
        self.datos = obtener_datos_usuario(usuario)
        self.configure(bg=self.bg_color)
        self.title("Mi cuenta")
        self.geometry("470x600")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        # ---------- TITULO ----------
        tk.Label(
            self,
            text="⚙️ Configuración de la cuenta",
            font=("Segoe UI", 15, "bold"),
            bg=self.bg_color,
            fg="#3E64FF"
        ).pack(pady=(15, 5))
        tk.Label(
            self,
            text=self.usuario,
            font=("Segoe UI", 12, "bold"),
            bg=self.bg_color
        ).pack()
        tk.Label(
            self,
            text=f"Rol: {self.datos['rol']}",
            font=("Segoe UI", 10),
            bg=self.bg_color,
            fg="#555"
        ).pack(pady=(0, 10))
        # ---------- CARD ----------
        card = tk.Frame(self, bg="white", bd=1, relief="solid")
        card.pack(padx=20, pady=10, fill="both")
        # ===== Datos personales =====
        tk.Label(card, text="Datos personales",
                font=("Segoe UI", 11, "bold"),
                bg="white", fg="#3E64FF").pack(pady=(10, 5))
        form = tk.Frame(card, bg="white")
        form.pack(padx=15, pady=5)
        tk.Label(form, text="Email:", bg="white").grid(row=0, column=0, sticky="w")
        self.entry_email = ttk.Entry(form, width=30)
        self.entry_email.grid(row=0, column=1, pady=5)
        self.entry_email.insert(0, self.datos["email"] or "")
        # ===== Contraseña =====
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
        # ===== Rutas =====
        tk.Label(card, text="Ruta exportaciones",
                font=("Segoe UI", 11, "bold"),
                bg="white", fg="#3E64FF").pack(pady=(15, 5))
        ruta_frame = tk.Frame(card, bg="white")
        ruta_frame.pack(padx=10, pady=5)
        ttk.Button(ruta_frame, text="Cambiar ruta", command=self._cambiar_ruta).pack(pady=(5, 10))
        self.lbl_ruta_actual = tk.Label(
            ruta_frame,
            text=f"Actual: {self.datos['ruta_export']}",
            bg="white", fg="#555"
        )
        self.lbl_ruta_actual.pack(fill="x")
        self.lbl_ruta_nueva = tk.Label(
            ruta_frame,
            text="Nueva: (sin seleccionar)",
            bg="white", fg="#555"
        )
        self.lbl_ruta_nueva.pack(fill="x", pady=(5, 5))
        # -------- BOTONES GUARDAR + CANCELAR ----------
        btn_frame = tk.Frame(self, bg=self.bg_color)
        btn_frame.pack(pady=25)
        ttk.Button(btn_frame, text="💾 Guardar cambios",
                    command=self._guardar).grid(row=0, column=0, padx=10)
        ttk.Button(btn_frame, text="Cancelar",
                    command=self.destroy).grid(row=0, column=1, padx=10)

    # =======================================================
    def _cambiar_ruta(self):
        carpeta = filedialog.askdirectory(title="Seleccionar carpeta de exportación")
        if carpeta:
            self.datos["ruta_export"] = carpeta
            self.lbl_ruta_nueva.config(text=f"Nueva: {carpeta}")

    # =======================================================
    def _guardar(self):
        email_actual = self.datos["email"] or ""
        ruta_actual = self.datos["ruta_export"] or ""
        email_nuevo = self.entry_email.get().strip()
        ruta_nueva = self.datos["ruta_export"]  # ya actualizada al usar Cambiar ruta
        hay_cambio_email = (email_nuevo != email_actual)
        hay_cambio_ruta  = (ruta_nueva != ruta_actual)
        hay_cambio_pass  = bool(self.pass_nueva.get().strip())
        # Si NO hay nada que guardar
        if not (hay_cambio_email or hay_cambio_ruta or hay_cambio_pass):
            messagebox.showinfo("Sin cambios", "No hay datos nuevos que guardar.")
            return
        # --- Guardar email o ruta si cambia CUALQUIERA de los dos ---
        if hay_cambio_email or hay_cambio_ruta:
            actualizar_datos_usuario(
                self.usuario,
                email_nuevo,
                ruta_nueva
            )
        # --- Guardar contraseña si procede ---
        if hay_cambio_pass:
            if not verificar_contrasena(self.usuario, self.pass_actual.get().strip()):
                messagebox.showerror("Error", "La contraseña actual es incorrecta.")
                return
            cambiar_contrasena(self.usuario, self.pass_nueva.get().strip())
        messagebox.showinfo("Éxito", "Datos actualizados correctamente.")
        self.destroy()
