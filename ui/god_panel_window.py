import tkinter as tk
from tkinter import ttk, messagebox
from models import usuarios as model
from ui.utils_style import aplicar_estilo_global
from ui.utils_treeview import auto_ajustar_columnas, ajustar_tamano_ventana
import bcrypt

class GodPanelWindow(tk.Toplevel):
    def __init__(self, parent, modo="claro"):
        super().__init__(parent)
        self.modo = modo
        self.style, self.bg_color = aplicar_estilo_global(modo)
        self.configure(bg=self.bg_color)
        self.title("👑 Panel del usuario GOD")
        self.geometry("950x550")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        # === Encabezado ===
        tk.Label(
            self,
            text="⚙️ Administración avanzada del sistema",
            font=("Segoe UI", 13, "bold"),
            fg="#3E64FF",
            bg=self.bg_color
        ).pack(pady=(15, 10))
        # === Tabla de usuarios ===
        self.tree = ttk.Treeview(
            self,
            columns=("usuario", "rol"),
            show="headings",
            height=15
        )
        self.tree.heading("usuario", text="Usuario", anchor="center")
        self.tree.heading("rol", text="Rol", anchor="center")
        self.tree.column("usuario", width=280, anchor="center")
        self.tree.column("rol", width=120, anchor="center")
        scroll_y = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll_y.set)
        scroll_y.pack(side="right", fill="y")
        self.tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        # === Botones ===
        frame_btns = tk.Frame(self, bg=self.bg_color)
        frame_btns.pack(pady=10)
        ttk.Button(frame_btns, text="🔄 Actualizar", command=self.cargar_usuarios).grid(row=0, column=0, padx=5)
        ttk.Button(frame_btns, text="➕ Crear usuario", command=self.ventana_nuevo_usuario).grid(row=0, column=1, padx=5)
        ttk.Button(frame_btns, text="🗑️ Eliminar usuario", command=self.eliminar_usuario).grid(row=0, column=2, padx=5)
        ttk.Button(frame_btns, text="✏️ Cambiar rol", command=self.cambiar_rol).grid(row=0, column=3, padx=5)
        ttk.Button(frame_btns, text="🔐 Editar contraseña", command=self.cambiar_contrasena).grid(row=0, column=4, padx=5)
        self.cargar_usuarios()

    # === Cargar usuarios ===
    def cargar_usuarios(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        usuarios = model.obtener_usuarios()
        for u in usuarios:
            self.tree.insert("", "end", values=u)
        auto_ajustar_columnas(self.tree)
        ajustar_tamano_ventana(self.tree, self)

    # === Crear nuevo usuario ===
    def ventana_nuevo_usuario(self):
        win = tk.Toplevel(self)
        win.title("Nuevo usuario (modo GOD)")
        win.geometry("450x300")
        win.configure(bg=self.bg_color)
        win.transient(self)
        win.grab_set()
        tk.Label(win, text="Crear nuevo usuario", font=("Segoe UI", 11, "bold"),
                fg="#3E64FF", bg=self.bg_color).pack(pady=(10, 15))
        frame = tk.Frame(win, bg=self.bg_color)
        frame.pack(pady=5)
        ttk.Label(frame, text="Usuario:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        entry_usuario = ttk.Entry(frame, width=30)
        entry_usuario.grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(frame, text="Contraseña:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        entry_contra = ttk.Entry(frame, width=30, show="*")
        entry_contra.grid(row=1, column=1, padx=5, pady=5)
        ttk.Label(frame, text="Rol:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        combo_rol = ttk.Combobox(frame, values=["usuario", "admin", "god"], state="readonly", width=28)
        combo_rol.set("usuario")
        combo_rol.grid(row=2, column=1, padx=5, pady=5)
        ttk.Button(
            win,
            text="💾 Guardar usuario",
            command=lambda: self._guardar_usuario(win, entry_usuario.get(), entry_contra.get(), combo_rol.get())
        ).pack(pady=15)

    def _guardar_usuario(self, ventana, usuario, contrasena, rol):
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

    # === Eliminar usuario ===
    def eliminar_usuario(self):
        item = self.tree.selection()
        if not item:
            messagebox.showwarning("Aviso", "Selecciona un usuario para eliminar.")
            return
        usuario = self.tree.item(item, "values")[0]
        if usuario.lower() == "god":
            messagebox.showwarning("No permitido", "No puedes eliminar al propio GOD.")
            return
        confirmar = messagebox.askyesno("Confirmar", f"¿Eliminar usuario '{usuario}'?")
        if confirmar:
            model.eliminar_usuario(usuario)
            self.cargar_usuarios()

    # === Cambiar rol ===
    def cambiar_rol(self):
        item = self.tree.selection()
        if not item:
            messagebox.showwarning("Aviso", "Selecciona un usuario para cambiar el rol.")
            return
        usuario, rol_actual = self.tree.item(item, "values")
        if usuario.lower() == "god":
            messagebox.showwarning("No permitido", "No se puede modificar el rol de GOD.")
            return
        win = tk.Toplevel(self)
        win.title(f"Cambiar rol de {usuario}")
        win.geometry("350x200")
        win.configure(bg=self.bg_color)
        win.transient(self)
        win.grab_set()
        ttk.Label(win, text=f"Rol actual: {rol_actual}").pack(pady=10)
        combo_rol = ttk.Combobox(win, values=["usuario", "admin", "god"], state="readonly", width=25)
        combo_rol.set(rol_actual)
        combo_rol.pack(pady=5)
        ttk.Button(
            win,
            text="✅ Guardar cambio",
            command=lambda: self._guardar_cambio_rol(usuario, combo_rol.get(), win)
        ).pack(pady=15)

    def _guardar_cambio_rol(self, usuario, nuevo_rol, ventana):
        conn = model.get_connection()
        cur = conn.cursor()
        cur.execute("UPDATE usuarios SET rol = ? WHERE nombre = ?", (nuevo_rol, usuario))
        conn.commit()
        conn.close()
        ventana.destroy()
        self.cargar_usuarios()
        messagebox.showinfo("Hecho", f"Rol de '{usuario}' actualizado a '{nuevo_rol}'.")

    # === Cambiar contraseña ===
    def cambiar_contrasena(self):
        item = self.tree.selection()
        if not item:
            messagebox.showwarning("Aviso", "Selecciona un usuario para editar la contraseña.")
            return
        usuario = self.tree.item(item, "values")[0]
        if usuario.lower() == "god":
            messagebox.showwarning("No permitido", "No puedes editar la contraseña del GOD.")
            return
        win = tk.Toplevel(self)
        win.title(f"Cambiar contraseña: {usuario}")
        win.geometry("400x220")
        win.configure(bg=self.bg_color)
        win.transient(self)
        win.grab_set()
        ttk.Label(win, text="Nueva contraseña:").pack(pady=10)
        entry_pass = ttk.Entry(win, show="*", width=30)
        entry_pass.pack(pady=5)
        ttk.Button(
            win,
            text="✅ Guardar nueva contraseña",
            command=lambda: self._guardar_contra(usuario, entry_pass.get(), win)
        ).pack(pady=15)

    def _guardar_contra(self, usuario, nueva_contra, ventana):
        if not nueva_contra:
            messagebox.showwarning("Aviso", "Introduce una contraseña válida.")
            return
        hashed = bcrypt.hashpw(nueva_contra.encode('utf-8'), bcrypt.gensalt())
        conn = model.get_connection()
        cur = conn.cursor()
        cur.execute("UPDATE usuarios SET contraseña = ? WHERE nombre = ?", (hashed, usuario))
        conn.commit()
        conn.close()
        messagebox.showinfo("Hecho", f"Contraseña de '{usuario}' actualizada.")
        ventana.destroy()
