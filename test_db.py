from models.db_connection import get_connection
from models.utils_db import manejar_error_db

def probar_conexion():
    print("🔌 Probando conexión con PostgreSQL...")
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT version();")
        version = cur.fetchone()
        print(f"✅ Conectado correctamente a PostgreSQL {version[0]}")
        conn.close()
    except Exception as e:
        manejar_error_db(e, "probar conexión")

if __name__ == "__main__":
    probar_conexion()
