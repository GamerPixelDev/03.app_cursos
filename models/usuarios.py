# models/usuarios.py
import bcrypt
from models.db_connection import get_connection
from models.utils_db import manejar_error_db

# --- helpers ---

def _hash_password(contrasena: str) -> str:
    #Devuelve el hash bcrypt como string UTF-8 (ideal para columna TEXT)
    return bcrypt.hashpw(contrasena.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

def _as_bytes(value) -> bytes:
    #Normaliza el valor leído de la BD (TEXT/BYTEA/memoryview) a bytes para checkpw
    if value is None:
        return b""
    if isinstance(value, bytes):
        return value
    if isinstance(value, memoryview):
        return bytes(value)
    if isinstance(value, str):
        return value.encode("utf-8")
    # último recurso
    return bytes(str(value), "utf-8")

def _es_duplicado_pg(err: Exception) -> bool:
    #Heurística simple para detectar violación de unicidad (sin depender de psycopg2)
    s = str(err).lower()
    return "duplicate key" in s or "unique constraint" in s or "ya existe" in s

# --- API ---

def crear_usuario(usuario: str, contrasena: str, rol: str):
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        hashed = _hash_password(contrasena)  # guardamos como TEXT
        cur.execute(
            "INSERT INTO usuarios (usuario, contrasena, rol) VALUES (%s, %s, %s)",
            (usuario, hashed, rol)
        )
        conn.commit()
        print(f"✅ Usuario '{usuario}' creado correctamente ({rol}).")
    except Exception as e:
        if _es_duplicado_pg(e):
            print(f"⚠️  El usuario '{usuario}' ya existe.")
        else:
            manejar_error_db(e, "crear usuario")
            print(f"⚠️  Error al crear el usuario '{usuario}': {e}")
    finally:
        if 'conn' in locals() and conn:
            conn.close()

def autenticar_usuario(usuario: str, contrasena: str):
    conn = None
    fila = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT contrasena, rol FROM usuarios WHERE usuario = %s", (usuario,))
        fila = cur.fetchone()
        print(f"[DEBUG] Resultado consulta: {fila}")  # 👈 Añadido
    except Exception as e:
        manejar_error_db(e, "autenticar usuario")
    finally:
        if 'conn' in locals() and conn:
            conn.close()
    if not fila:
        return False, None
    hashed_str_o_bytes, rol = fila
    hashed = _as_bytes(hashed_str_o_bytes)
    print(f"[DEBUG] Intentando validar usuario={usuario}, rol={rol}")  # 👈 Añadido
    try:
        if bcrypt.checkpw(contrasena.encode("utf-8"), hashed):
            print("[DEBUG] Contraseña válida ✅")  # 👈 Añadido
            # blindaje: solo root_god puede ostentar rol god
            if rol == "god" and usuario != "root_god":
                return False, None
            return True, rol
    except Exception as e:
        print("⚠️ Error al verificar hash:", e)
        print(f"[DEBUG] No se pudo autenticar: usuario={usuario}, fila={fila}") 
    return False, None

def verificar_contrasena(usuario: str, contrasena: str) -> bool:
    conn = None
    fila = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT contrasena FROM usuarios WHERE usuario = %s", (usuario,))
        fila = cur.fetchone()
    except Exception as e:
        manejar_error_db(e, "verificar contraseña")
        return False
    finally:
        if 'conn' in locals() and conn:
            conn.close()
    if not fila:
        return False
    hashed = _as_bytes(fila[0])
    return bcrypt.checkpw(contrasena.encode("utf-8"), hashed)

def cambiar_contrasena(usuario: str, nueva_contrasena: str):
    if not nueva_contrasena:
        return
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        hashed = _hash_password(nueva_contrasena)  # guardamos como TEXT
        cur.execute("UPDATE usuarios SET contrasena = %s WHERE usuario = %s", (hashed, usuario))
        conn.commit()
    except Exception as e:
        manejar_error_db(e, "cambiar contraseña")
    finally:
        if 'conn' in locals() and conn:
            conn.close()

def obtener_usuarios(incluir_god: bool = False):
    conn = None
    usuarios = []
    try:
        conn = get_connection()
        cur = conn.cursor()
        if incluir_god:
            cur.execute("SELECT usuario, rol FROM usuarios ORDER BY rol DESC, usuario ASC")
        else:
            cur.execute("SELECT usuario, rol FROM usuarios WHERE rol != 'god' ORDER BY rol DESC, usuario ASC")
        usuarios = cur.fetchall()
    except Exception as e:
        manejar_error_db(e, "obtener usuarios")
    finally:
        if 'conn' in locals() and conn:
            conn.close()
    return usuarios

def eliminar_usuario(usuario: str):
    if usuario == "root_god":
        print("❌ No se puede eliminar el usuario raíz.")
        return
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM usuarios WHERE usuario = %s", (usuario,))
        conn.commit()
    except Exception as e:
        manejar_error_db(e, "eliminar usuario")
    finally:
        if 'conn' in locals() and conn:
            conn.close()

def iniciar_admin():
    """Crea admin/admin123 si no existe."""
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM usuarios WHERE usuario = 'admin'")
        existe = cur.fetchone()
        if not existe:
            crear_usuario("admin", "admin123", "admin")
            print("🛠️  Usuario 'admin' creado (contraseña: admin123)")
        else:
            print("Admin ya existe, no se recrea.")
    except Exception as e:
        manejar_error_db(e, "iniciar admin")
    finally:
        if 'conn' in locals() and conn:
            conn.close()

def iniciar_god():
    """Crea root_god/root1234 si no existe."""
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM usuarios WHERE rol = 'god'")
        existe = cur.fetchone()
        if not existe:
            cur.execute(
                "INSERT INTO usuarios (usuario, contrasena, rol) VALUES (%s, %s, %s)",
                ("root_god", _hash_password("root1234"), "god")
            )
            conn.commit()
            print("⚡ Usuario 'root_god' creado automáticamente (contraseña: root1234)")
    except Exception as e:
        manejar_error_db(e, "iniciar god")
    finally:
        if 'conn' in locals() and conn:
            conn.close()

if __name__ == "__main__":
    # smoke test rápido
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT version();")
        print("Servidor responde:", cur.fetchone())
    except Exception as e:
        manejar_error_db(e, "conectando")
    finally:
        if 'conn' in locals() and conn:
            conn.close()
