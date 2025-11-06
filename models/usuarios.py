import sqlite3
import bcrypt
import os

# === CONEXIÓN A LA BASE DE DATOS ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)
DB_PATH = os.path.join(ROOT_DIR, "data", "database.db")

def get_connection():
    return sqlite3.connect(DB_PATH)

# === Crear hash seguro ===
def _hash_password(contrasena: str) -> bytes:
    return bcrypt.hashpw(contrasena.encode("utf-8"), bcrypt.gensalt())

# === Crear usuario ===
def crear_usuario(usuario, contrasena, rol):
    conn = get_connection()
    cur = conn.cursor()
    hashed = _hash_password(contrasena)
    try:
        cur.execute(
            "INSERT INTO usuarios (usuario, contrasena, rol) VALUES (?, ?, ?)",
            (usuario, hashed, rol)
        )
        conn.commit()
        print(f"✅ Usuario '{usuario}' creado correctamente ({rol}).")
    except sqlite3.IntegrityError:
        print(f"⚠️  El usuario '{usuario}' ya existe.")
    finally:
        conn.close()

# === Autenticar usuario (login) ===
def autenticar_usuario(usuario, contrasena):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT contrasena, rol FROM usuarios WHERE usuario = ?", (usuario,))
    fila = cur.fetchone()
    conn.close()
    if fila:
        hashed, rol = fila
        try:
            if bcrypt.checkpw(contrasena.encode("utf-8"), hashed):
                return True, rol
        except Exception:
            pass
    return False, None

# === Verificar contraseña actual (para MiCuentaWindow) ===
def verificar_contrasena(usuario, contrasena):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT contrasena FROM usuarios WHERE usuario = ?", (usuario,))
    fila = cur.fetchone()
    conn.close()
    return fila and bcrypt.checkpw(contrasena.encode("utf-8"), fila[0])

# === Cambiar contraseña ===
def cambiar_contrasena(usuario, nueva_contrasena):
    conn = get_connection()
    cur = conn.cursor()
    hashed = _hash_password(nueva_contrasena)
    cur.execute("UPDATE usuarios SET contrasena = ? WHERE usuario = ?", (hashed, usuario))
    conn.commit()
    conn.close()

# === Obtener usuarios (para ventana admin/GOD) ===
def obtener_usuarios(incluir_god=False):
    conn = get_connection()
    cur = conn.cursor()
    if incluir_god:
        cur.execute("SELECT nombre, rol FROM usuarios")
    else:
        cur.execute("SELECT nombre, rol FROM usuarios WHERE rol != 'god'")
    usuarios = cur.fetchall()
    conn.close()
    return usuarios

# === Eliminar usuario ===
def eliminar_usuario(usuario):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM usuarios WHERE usuario = ?", (usuario,))
    conn.commit()
    conn.close()

# === Crear admin por defecto si no existe ===
def iniciar_admin():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM usuarios WHERE usuario = 'admin'")
    existe = cur.fetchone()
    conn.close()
    if not existe:
        crear_usuario("admin", "admin123", "admin")
        print("🛠️  Usuario 'admin' creado (contraseña: admin123)")
    else:
        print("Admin ya existe, no se recrea.")

# === Ejecución directa ===
if __name__ == "__main__":
    iniciar_admin()
