# models/db_connection.py
import psycopg2
from psycopg2 import sql, OperationalError

# === CONFIGURACIÓN DE CONEXIÓN ===
DB_CONFIG = {
    "host": "localhost",        # más adelante lo cambias por la IP del servidor
    "database": "gestor_cursos",
    "user": "postgres",
    "password": "JuntaAdmin123",     # pon tu contraseña real
    "port": 5432
}

# === FUNCIÓN DE CONEXIÓN GLOBAL ===
def get_connection():
    """
    Devuelve una conexión abierta a la base de datos PostgreSQL.
    """
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except OperationalError as e:
        print(f"[ERROR] No se pudo conectar a la base de datos: {e}")
        raise

# === TEST DIRECTO ===
if __name__ == "__main__":
    try:
        with get_connection() as conn:
            print("✅ Conexión exitosa a PostgreSQL")
    except Exception as e:
        print("❌ Error de conexión:", e)
