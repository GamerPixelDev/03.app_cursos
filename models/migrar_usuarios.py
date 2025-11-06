import sqlite3
import bcrypt
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)
DB_PATH = os.path.join(ROOT_DIR, "data", "database.db")

def get_connection():
    return sqlite3.connect(DB_PATH)

def migrar_usuarios():
    conn = get_connection()
    cur = conn.cursor()

    # 1. Verificar si ya existe la nueva tabla
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='usuarios_nueva'")
    if cur.fetchone():
        print("⚠️  Ya existe 'usuarios_nueva'. Posiblemente la migración ya se hizo.")
        conn.close()
        return

    # 2. Crear nueva tabla con estructura moderna
    cur.execute("""
        CREATE TABLE usuarios_nueva (
            usuario TEXT PRIMARY KEY,
            contrasena BLOB NOT NULL,
            rol TEXT NOT NULL
        )
    """)

    # 3. Detectar si existe la tabla vieja
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='usuarios'")
    if not cur.fetchone():
        print("❌ No existe tabla 'usuarios' para migrar.")
        conn.close()
        return

    # 4. Leer usuarios antiguos
    try:
        cur.execute("SELECT nombre, contraseña, rol FROM usuarios")
        antiguos = cur.fetchall()
    except Exception as e:
        print(f"❌ Error al leer usuarios antiguos: {e}")
        conn.close()
        return

    # 5. Migrar usuarios con hash bcrypt
    for nombre, contrasena, rol in antiguos:
        hashed = bcrypt.hashpw(str(contrasena).encode("utf-8"), bcrypt.gensalt())
        cur.execute(
            "INSERT INTO usuarios_nueva (usuario, contrasena, rol) VALUES (?, ?, ?)",
            (nombre, hashed, rol)
        )

    conn.commit()

    # 6. Reemplazar tabla antigua
    cur.execute("DROP TABLE usuarios")
    cur.execute("ALTER TABLE usuarios_nueva RENAME TO usuarios")
    conn.commit()
    conn.close()
    print("✅ Migración completada correctamente.")
    print("   - Contraseñas convertidas a bcrypt")
    print("   - Estructura estandarizada: usuario / contrasena / rol")

if __name__ == "__main__":
    migrar_usuarios()
