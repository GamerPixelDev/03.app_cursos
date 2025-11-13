# models/usuarios.py
import bcrypt
from models.db_connection import get_connection
from models.utils_db import manejar_error_db

# --- helpers ---
def _hash_password(contrasena: str) -> str:
    return bcrypt.hashpw(contrasena.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

def _as_bytes(value) -> bytes:
    if value is None:
        return b""
    if isinstance(value, bytes):
        return value
    if isinstance(value, memoryview):
        return bytes(value)
    if isinstance(value, str):
        return value.encode("utf-8")
    return bytes(str(value), "utf-8")

#                    CRUD BÁSICO
def obtener_datos_usuario(usuario):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT usuario, email, rol, ruta_export
        FROM usuarios
        WHERE usuario = %s
    """, (usuario,))
    fila = cur.fetchone()
    conn.close()
    if not fila:
        return None
    return {
        "usuario": fila[0],
        "email": fila[1],
        "rol": fila[2],
        "ruta_export": fila[3]
    }

def actualizar_datos_usuario(usuario, email, ruta_export):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE usuarios
        SET email=%s, ruta_export=%s
        WHERE usuario=%s
    """, (email, ruta_export, usuario))
    conn.commit()
    conn.close()

#                   CONTRASEÑA
def verificar_contrasena(usuario: str, contrasena: str) -> bool:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT contrasena FROM usuarios WHERE usuario = %s", (usuario,))
    fila = cur.fetchone()
    conn.close()
    if not fila:
        return False
    hashed = _as_bytes(fila[0])
    return bcrypt.checkpw(contrasena.encode("utf-8"), hashed)

def autenticar_usuario(usuario: str, contrasena: str):

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT contrasena, rol FROM usuarios WHERE usuario = %s",
        (usuario,)
    )
    fila = cur.fetchone()
    conn.close()
    # Usuario no existe
    if not fila:
        return False, None
    hashed, rol = fila
    hashed = _as_bytes(hashed)
    # Comprobar contraseña
    if bcrypt.checkpw(contrasena.encode("utf-8"), hashed):
        return True, rol
    return False, None


def cambiar_contrasena(usuario: str, nueva_contrasena: str):
    if not nueva_contrasena:
        return False
    conn = get_connection()
    cur = conn.cursor()
    hashed = _hash_password(nueva_contrasena)
    cur.execute("UPDATE usuarios SET contrasena = %s WHERE usuario = %s",
                (hashed, usuario))
    conn.commit()
    conn.close()
    return True
