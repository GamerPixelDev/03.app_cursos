# models/db_connection.py
import psycopg2
from psycopg2 import OperationalError
import time

# === CONFIGURACIÓN DE CONEXIÓN ===
DB_CONFIG = {
    "host": "localhost",        # más adelante lo cambias por la IP del servidor
    "database": "gestor_cursos",
    "user": "postgres",
    "password": "JuntaAdmin123",     # pon tu contraseña real
    "port": 5432
}

# === FUNCIÓN DE CONEXIÓN GLOBAL ===
def get_connection(reintentos=2, espera=2):
    """Devuelve una conexión a PostgreSQL con reintento automático."""
    for intento in range(reintentos):
        try:
            conn = psycopg2.connect(**DB_CONFIG)
            return conn
        except OperationalError as e:
            print(f"⚠️ Fallo al conectar a la base de datos (intento {intento+1}/{reintentos}): {e}")
            if intento < reintentos - 1:
                time.sleep(espera)
            else:
                raise RuntimeError("❌ No se pudo establecer conexión con el servidor PostgreSQL.")

# === TEST DIRECTO ===
if __name__ == "__main__":
    try:
        with get_connection() as conn:
            print("✅ Conexión exitosa a PostgreSQL")
    except Exception as e:
        print("❌ Error de conexión:", e)
