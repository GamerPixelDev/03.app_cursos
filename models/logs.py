import datetime
from models.db_connection import get_connection

def registrar_evento(usuario, accion, detalle=""):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id SERIAL PRIMARY KEY,
            usuario VARCHAR(50),
            accion TEXT,
            detalle TEXT,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cur.execute(
        "INSERT INTO logs (usuario, accion, detalle) VALUES (%s, %s, %s)",
        (usuario, accion, detalle)
    )
    conn.commit()
    conn.close()

def obtener_logs(limit=100):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT usuario, accion, detalle, fecha FROM logs ORDER BY fecha DESC LIMIT %s",
        (limit,)
    )
    datos = cur.fetchall()
    conn.close()
    return datos
