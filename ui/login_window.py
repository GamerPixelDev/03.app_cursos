import tkinter as tk
from tkinter import messagebox
from models.usuarios import autenticar_usuario
from ui.main_window import MainWindow

#=== Ventana de Login ===
class LoginWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Inicio de sesión")
        self.root.geometry("300x200")
        self.root.resizable(False, False)
        #Etiquetas y campos de entrada
        tk.Label(self.root, text="Usuario:").pack(pady=5)
        self.entry_usuario = tk.Entry(self.root)
        self.entry_usuario.pack()
        tk.Label(self.root, text="Contraseña:").pack(pady=5)
        self.entry_contraseña = tk.Entry(self.root, show="*")
        self.entry_contraseña.pack()
        #Botón de inicio de sesión
        tk.Button(self.root, text="Iniciar sesión", command=self.iniciar_sesion).pack(pady=10) # Llama al método iniciar_sesion al hacer clic
        #Ejecutar la ventana
        self.root.mainloop()
    
    def iniciar_sesion(self):
        #Validar las credenciales del usuario
        usuario = self.entry_usuario.get()
        contraseña = self.entry_contraseña.get()
        valido, rol = autenticar_usuario(usuario, contraseña)
        if valido:
            messagebox.showinfo("Acceso concedido", f"Bienvenido, {usuario}! Rol: {rol}")
            self.root.destroy() # Cierra la ventana de login al iniciar sesión correctamente
            MainWindow(usuario, rol) # Abre la ventana principal pasando el usuario y rol
        else:
            messagebox.showerror("Acceso denegado", "Usuario o contraseña incorrectos.")