import tkinter as tk
from tkinter import ttk, messagebox
from models import usuarios as model
from ui.utils_style import aplicar_estilo_global
from ui.utils_treeview import auto_ajustar_columnas, ajustar_tamano_ventana
import bcrypt

class UsuariosWindow(tk.Toplevel):
    def __init__(self, parent, modo="claro", rol_actual="usuario"):
        super().__init__(parent)
        self.rol_actual = rol_actual
        self.modo = modo
        self.style, self.bg_color = aplicar_estilo_global(modo)
        self.configure(bg=self.bg_color)
        self.title("Gestión de usuarios")
        self.geometry("900x500")
        self.minsize(750, 400)
        self.resizable(True, True)
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        # === Encabezado ===
        tk.Label(
            self,
            text="👥 Administración de usuarios",
            font=("Segoe UI", 13, "bold"),
            fg="#3E64FF",
            bg=self.bg_color
        ).pack(pady=(10, 8))

        # === Frame principal (tabla + scroll) ===
        frame_tabla = tk.Frame(self, bg=self.bg_color)
        frame_tabla.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        self.tree = ttk.Treeview(
            frame_tabla,
            columns=("usuario", "rol"),
            show="headings"
        )
        self.tree.heading("usuario", text="Usuario", anchor="center")
        self.tree.heading("rol", text="Rol", anchor="center")
        self.tree.column("usuario", width=280, anchor="center")
        self.tree.column("rol", width=150, anchor="center")

        # Scrollbar vertical
        scroll_y = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll_y.set)

        # Distribución con grid
        self.tree.grid(row=0, column=0, sticky="nsew")
        scroll_y.grid(row=0, column=1, sticky="ns")

        frame_tabla.grid_rowconfigure(0, weight=1)
        frame_tabla.grid_columnconfigure(0, weight=1)

        # === Frame inferior (botones centrados) ===
        frame_btns = tk.Frame(self, bg=self.bg_color)
        frame_btns.pack(pady=10)

        ttk.Button(frame_btns, text="🔄 Actualizar", command=self.cargar_usuarios).pack(side="left", padx=8)

        if self.rol_actual in ("admin", "god"):
            ttk.Button(frame_btns, text="➕ Añadir usuario", command=self.ventana_nuevo_usuario).pack(side="left", padx=8)
            ttk.Button(frame_btns, text="🗑️ Eliminar", command=self.eliminar_usuario).pack(side="left", padx=8)

        if self.rol_actual == "god":
            ttk.Button(frame_btns, text="🔐 Cambiar contraseña", command=self.cambiar_contrasena).pack(side="left", padx=8)

        # Centramos todo el grupo
        frame_btns.pack_configure(anchor="center")

        self.cargar_usuarios()

    # --- Cargar usuarios ---
    def cargar_usuarios(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        usuarios = model.obtener_usuarios()
        for u in usuarios:
            self.tree.insert("", "end", values=u)
        auto_ajustar_columnas(self.tree)
        ajustar_tamano_ventana(self.tree, self)

    # --- Nueva ventana para añadir usuario ---
    def ventana_nuevo_usuario(self):
        win = tk.Toplevel(self)
        win.title("Nuevo usuario")
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

    # --- Eliminar usuario ---
    def eliminar_usuario(self):
        item = self.tree.selection()
        if not item:
            messagebox.showwarning("Aviso", "Selecciona un usuario para eliminar.")
            return
        usuario = self.tree.item(item, "values")[0]
        if usuario.lower() == "god":
            messagebox.showwarning("Acción no permitida", "No se puede eliminar el usuario GOD.")
            return
        confirmar = messagebox.askyesno("Confirmar", f"¿Eliminar el usuario '{usuario}'?")
        if confirmar:
            model.eliminar_usuario(usuario)
            self.cargar_usuarios()

    # --- Cambiar contraseña (solo GOD) ---
    def cambiar_contrasena(self):
        item = self.tree.selection()
        if not item:
            messagebox.showwarning("Aviso", "Selecciona un usuario para cambiar la contraseña.")
            return
        usuario = self.tree.item(item, "values")[0]
        if usuario.lower() == "god":
            messagebox.showwarning("Acción no permitida", "No se puede modificar la contraseña del GOD.")
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
            text="✅ Confirmar cambio",
            command=lambda: self._guardar_nueva_contra(usuario, entry_pass.get(), win)
        ).pack(pady=15)

    def _guardar_nueva_contra(self, usuario, nueva_contra, ventana):
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
