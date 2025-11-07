import tkinter as tk
from tkinter import ttk, messagebox
from models import usuarios as model
from ui.utils_style import aplicar_estilo_global
from ui.utils_treeview import auto_ajustar_columnas, ajustar_tamano_ventana
import datetime
import os

class GodPanelWindow(tk.Toplevel):
    def __init__(self, parent, modo="claro"):
        super().__init__(parent)
        self.modo = modo
        self.style, self.bg_color = aplicar_estilo_global(modo)
        self.configure(bg=self.bg_color)
        self.title("👁️ Panel GOD - Control total del sistema")
        self.geometry("900x550")
        self.resizable(True, True)
        self.transient(parent)
        self.grab_set()
        # === Encabezado ===
        tk.Label(
            self,
            text="⚡ Panel de control del usuario ROOT_GOD",
            font=("Segoe UI", 13, "bold"),
            fg="#FF3E3E",
            bg=self.bg_color
        ).pack(pady=(10, 5))
        tk.Label(
            self,
            text=f"Sesión iniciada: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}",
            font=("Segoe UI", 9),
            fg="#333",
            bg=self.bg_color
        ).pack(pady=(0, 10))
        # === Frame principal ===
        frame = tk.Frame(self, bg=self.bg_color)
        frame.pack(fill="both", expand=True, padx=10, pady=10)
        # === Tabla de usuarios (incluye GOD) ===
        self.tree = ttk.Treeview(
            frame,
            columns=("usuario", "rol"),
            show="headings",
            height=15
        )
        self.tree.heading("usuario", text="Usuario", anchor="center")
        self.tree.heading("rol", text="Rol", anchor="center")
        self.tree.column("usuario", width=250, anchor="center")
        self.tree.column("rol", width=120, anchor="center")
        scroll_y = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll_y.set)
        scroll_y.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)
        # === Botones ===
        frame_btns = tk.Frame(self, bg=self.bg_color)
        frame_btns.pack(pady=15)
        ttk.Button(frame_btns, text="🔄 Actualizar", command=self.cargar_usuarios).grid(row=0, column=0, padx=8)
        ttk.Button(frame_btns, text="➕ Crear usuario", command=self.ventana_nuevo_usuario).grid(row=0, column=1, padx=8)
        ttk.Button(frame_btns, text="🔑 Cambiar contraseña", command=self.cambiar_contrasena).grid(row=0, column=2, padx=8)
        ttk.Button(frame_btns, text="🗑️ Eliminar usuario", command=self.eliminar_usuario).grid(row=0, column=3, padx=8)
        ttk.Button(frame_btns, text="📁 Información del sistema", command=self.ver_info_sistema).grid(row=0, column=4, padx=8)
        self.cargar_usuarios()

    # === Cargar usuarios (incluye GOD) ===
    def cargar_usuarios(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        usuarios = model.obtener_usuarios(incluir_god=True)
        for u in usuarios:
            self.tree.insert("", "end", values=u)
        auto_ajustar_columnas(self.tree)
        ajustar_tamano_ventana(self.tree, self)

    # === Crear usuario nuevo ===
    def ventana_nuevo_usuario(self):
        win = tk.Toplevel(self)
        win.title("Crear nuevo usuario")
        win.geometry("350x250")
        win.configure(bg=self.bg_color)
        win.transient(self)
        win.grab_set()
        tk.Label(win, text="Nuevo usuario", font=("Segoe UI", 11, "bold"),
                fg="#3E64FF", bg=self.bg_color).pack(pady=(10, 15))
        frame = tk.Frame(win, bg=self.bg_color)
        frame.pack(pady=5)
        ttk.Label(frame, text="Usuario:", background=self.bg_color).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        entry_usuario = ttk.Entry(frame, width=25)
        entry_usuario.grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(frame, text="Contraseña:", background=self.bg_color).grid(row=1, column=0, padx=5, pady=5, sticky="w")
        entry_contra = ttk.Entry(frame, width=25, show="*")
        entry_contra.grid(row=1, column=1, padx=5, pady=5)
        ttk.Label(frame, text="Rol:", background=self.bg_color).grid(row=2, column=0, padx=5, pady=5, sticky="w")
        combo_rol = ttk.Combobox(frame, values=["usuario", "admin", "god"], state="readonly", width=23)
        combo_rol.set("usuario")
        combo_rol.grid(row=2, column=1, padx=5, pady=5)
        ttk.Button(
            win,
            text="💾 Guardar usuario",
            command=lambda: self.guardar_usuario(win, entry_usuario.get(), entry_contra.get(), combo_rol.get())
        ).pack(pady=15)

    def guardar_usuario(self, ventana, usuario, contrasena, rol):
        if not usuario or not contrasena:
            messagebox.showwarning("Campos vacíos", "Completa todos los campos.")
            return
        try:
            model.crear_usuario(usuario, contrasena, rol)
            messagebox.showinfo("Éxito", f"Usuario '{usuario}' creado correctamente.")
            ventana.destroy()
            self.cargar_usuarios()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # === Cambiar contraseña ===
    def cambiar_contrasena(self):
        item = self.tree.selection()
        if not item:
            messagebox.showwarning("Aviso", "Selecciona un usuario.")
            return
        usuario = self.tree.item(item, "values")[0]
        win = tk.Toplevel(self)
        win.title(f"Cambiar contraseña: {usuario}")
        win.geometry("350x200")
        win.configure(bg=self.bg_color)
        win.transient(self)
        win.grab_set()
        ttk.Label(win, text="Nueva contraseña:", background=self.bg_color).pack(pady=10)
        entry_pass = ttk.Entry(win, show="*", width=25)
        entry_pass.pack(pady=5)
        ttk.Button(
            win,
            text="✅ Confirmar cambio",
            command=lambda: self._guardar_nueva_contra(usuario, entry_pass.get(), win)
        ).pack(pady=15)

    def _guardar_nueva_contra(self, usuario, nueva_contra, ventana):
        if not nueva_contra:
            messagebox.showwarning("Aviso", "Introduce una contraseña válida.")
            return
        model.cambiar_contrasena(usuario, nueva_contra)
        messagebox.showinfo("Hecho", f"Contraseña de '{usuario}' actualizada.")
        ventana.destroy()

    # === Eliminar usuario ===
    def eliminar_usuario(self):
        item = self.tree.selection()
        if not item:
            messagebox.showwarning("Aviso", "Selecciona un usuario.")
            return
        usuario = self.tree.item(item, "values")[0]
        if usuario == "root_god":
            messagebox.showinfo("Prohibido", "No puedes eliminar al usuario raíz.")
            return
        confirmar = messagebox.askyesno("Confirmar", f"¿Eliminar el usuario '{usuario}'?")
        if confirmar:
            model.eliminar_usuario(usuario)
            self.cargar_usuarios()

    # === Información del sistema ===
    def ver_info_sistema(self):
        conn_path = model.DB_PATH
        tamano = os.path.getsize(conn_path) / 1024
        num_usuarios = len(model.obtener_usuarios(incluir_god=True))
        msg = (
            f"🧩 Información del sistema\n\n"
            f"📁 Base de datos: {conn_path}\n"
            f"💾 Tamaño: {tamano:.2f} KB\n"
            f"👥 Usuarios totales: {num_usuarios}\n"
            f"🕒 Último acceso: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"
        )
        messagebox.showinfo("Estado del sistema", msg)
