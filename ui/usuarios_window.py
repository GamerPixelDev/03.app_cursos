import tkinter as tk
from tkinter import ttk, messagebox
from models import usuarios as model
from ui.utils_style import aplicar_estilo_global
from ui.utils_treeview import auto_ajustar_columnas, ajustar_tamano_ventana

class UsuariosWindow(tk.Toplevel):
    def __init__(self, parent, modo="claro"):
        super().__init__(parent)
        self.modo = modo
        self.style, self.bg_color = aplicar_estilo_global(modo)
        self.configure(bg=self.bg_color)
        self.title("Gestión de usuarios")
        self.geometry("700x400")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        # === Encabezado ===
        tk.Label(
            self,
            text="Administración de usuarios",
            font=("Segoe UI", 12, "bold"),
            fg="#3E64FF",
            bg=self.bg_color
        ).pack(pady=(10, 10))
        # === Tabla de usuarios ===
        self.tree = ttk.Treeview(
            self,
            columns=("usuario", "rol"),
            show="headings",
            height=12
        )
        self.tree.heading("usuario", text="Usuario", anchor="center")
        self.tree.heading("rol", text="Rol", anchor="center")
        self.tree.column("usuario", width=250, anchor="center")
        self.tree.column("rol", width=150, anchor="center")
        scroll_y = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll_y.set)
        scroll_y.pack(side="right", fill="y")
        self.tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        # === Botones ===
        frame_btns = tk.Frame(self, bg=self.bg_color)
        frame_btns.pack(pady=10)
        ttk.Button(frame_btns, text="➕ Añadir usuario", command=self.ventana_nuevo_usuario).grid(row=0, column=0, padx=5)
        ttk.Button(frame_btns, text="🗑️ Eliminar seleccionado", command=self.eliminar_usuario).grid(row=0, column=1, padx=5)
        self.cargar_usuarios()

    # === Cargar datos ===
    def cargar_usuarios(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        usuarios = model.obtener_usuarios()
        for u in usuarios:
            self.tree.insert("", "end", values=u)
        auto_ajustar_columnas(self.tree)
        ajustar_tamano_ventana(self.tree, self)

    # === Añadir usuario ===
    def ventana_nuevo_usuario(self):
        win = tk.Toplevel(self)
        win.title("Nuevo usuario")
        win.geometry("350x250")
        win.configure(bg=self.bg_color)
        win.transient(self)
        win.grab_set()
        tk.Label(win, text="Crear nuevo usuario", font=("Segoe UI", 11, "bold"),
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
        combo_rol = ttk.Combobox(frame, values=["admin", "usuario"], state="readonly", width=23)
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

    # === Eliminar usuario ===
    def eliminar_usuario(self):
        item = self.tree.selection()
        if not item:
            messagebox.showwarning("Aviso", "Selecciona un usuario para eliminar.")
            return
        usuario = self.tree.item(item, "values")[0]
        confirmar = messagebox.askyesno("Confirmar", f"¿Eliminar el usuario '{usuario}'?")
        if confirmar:
            model.eliminar_usuario(usuario)
            self.cargar_usuarios()
