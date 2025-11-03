import sqlite3
import bcrypt # Asegúrate de tener bcrypt instalado: pip install bcrypt
import os

#=== CONEXIÓN A LA BASE DE DATOS ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)
DB_PATH = os.path.join(ROOT_DIR, "data", "database.db") # Ruta absoluta a la base de datos

def get_connection():
    return sqlite3.connect(DB_PATH) #Devuelve una conexión a la base de datos

#=== FUNCIÓN PARA CREAR UN NUEVO USUARIO ===
def crear_usuario(nombre, contraseña, rol):
    conn = get_connection()
    cursor = conn.cursor()
    #Ciframos la contraseña antes de guardarla
    hashed = bcrypt.hashpw(contraseña.encode('utf-8'), bcrypt.gensalt())
    try:
        cursor.execute("INSERT INTO usuarios (nombre, contraseña, rol) VALUES (?, ?, ?)", (nombre, hashed, rol))
        conn.commit()
        print(f"Usuario '{nombre}' creado correctamente.")
    except sqlite3.IntegrityError:
        print(f"Error: El usuario '{nombre}' ya existe.")
    finally:
        conn.close()

#=== FUNCIÓN PARA AUTENTICAR UN USUARIO ===
def autenticar_usuario(nombre, contraseña):
    #COmprobamos si el usuario y la contraseña son correctos
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT contraseña, rol FROM usuarios WHERE nombre = ?", (nombre,))
    result = cursor.fetchone()
    conn.close()
    if result:
        hashed, rol = result
        if bcrypt.checkpw(contraseña.encode('utf-8'), hashed):
            return True, rol
    return False, None

#=== CREAR USUARIO ADMIN POR DEFECTO SI NO EXISTE ===
def iniciar_admin():
    crear_usuario("admin", "admin123", "admin")

#=== EJECUCIÓN INICIAL ===
if __name__ == "__main__":
    iniciar_admin()