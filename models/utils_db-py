from psycopg2 import OperationalError, IntegrityError
from tkinter import messagebox

def manejar_error_db(e, accion="operación en la base de datos"):
    if isinstance(e, OperationalError):
        messagebox.showerror("Error de conexión", "⚠️ No se pudo conectar al servidor de datos.\nVerifica tu conexión o contacta al administrador.")
    elif isinstance(e, IntegrityError):
        messagebox.showwarning("Dato duplicado", "Este registro ya existe en la base de datos.")
    else:
        messagebox.showerror("Error", f"❌ Error durante {accion}:\n{e}")
