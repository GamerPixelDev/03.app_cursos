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
def obtener_usuarios(incluir_god=False):
    conn = get_connection()
    cur = conn.cursor()
    consulta = "SELECT usuario, rol, email, ruta_export FROM usuarios"
    parametros = []
    if not incluir_god:
        consulta += " WHERE LOWER(BTRIM(usuario, E' \\t\\n\\r')) <> %s"
        parametros.append("god")
    consulta += " ORDER BY usuario"
    cur.execute(consulta, tuple(parametros))
    filas = cur.fetchall()
    conn.close()
    usuarios = []
    for usuario, rol, email, ruta in filas:
        nombre_normalizado = (usuario or "").strip().lower()
        if not incluir_god and nombre_normalizado == "god":
            continue
        usuarios.append((usuario, rol, email, ruta))
    return usuarios

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

def crear_usuario(usuario: str, contrasena: str, rol: str, email: str, ruta_export: str = None):
    if ruta_export is None:
        from pathlib import Path
        ruta_export = str(Path.home() / "Downloads")
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT 1 FROM usuarios WHERE usuario = %s", (usuario,))
        if cur.fetchone():
            raise ValueError(f"El usuario '{usuario}' ya existe.")
        hashed = _hash_password(contrasena)
        cur.execute(
            "INSERT INTO usuarios (usuario, contrasena, rol, email, ruta_export) VALUES (%s, %s, %s, %s, %s)",
            (usuario, hashed, rol, email, ruta_export)
        )
        conn.commit()
    finally:
        conn.close()

def eliminar_usuario(usuario: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM usuarios WHERE usuario = %s", (usuario,))
    conn.commit()
    conn.close()

def actualizar_rol(usuario: str, nuevo_rol: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE usuarios SET rol = %s WHERE usuario = %s", (nuevo_rol, usuario))
    conn.commit()
    conn.close()

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
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT contrasena FROM usuarios WHERE usuario = %s", (usuario,))
        fila = cur.fetchone()
    except Exception:
        return False
    finally:
        conn.close()
    if not fila:
        return False
    hashed = _as_bytes(fila[0])
    return bcrypt.checkpw(contrasena.encode("utf-8"), hashed)

def autenticar_usuario(usuario: str, contrasena: str):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT contrasena, rol FROM usuarios WHERE usuario = %s",(usuario,)
        )
        fila = cur.fetchone()
    except Exception as e:
        manejar_error_db(e, "autenticar usuario")
        return False, None
    finally:
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

def obtener_ruta_export(usuario):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT ruta_export FROM usuarios WHERE usuario=%s", (usuario,))
    fila = cur.fetchone()
    conn.close()
    return fila[0] if fila else ""

def actualizar_ruta_export(usuario, ruta):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE usuarios SET ruta_export=%s WHERE usuario=%s", (ruta, usuario))
    conn.commit()
    conn.close()