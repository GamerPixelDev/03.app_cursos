import sqlite3
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)
DB_PATH = os.path.join(ROOT_DIR, "data", "database.db")

def get_connection():
    return sqlite3.connect(DB_PATH)

# --- Crear matrícula ---
def crear_matricula(nif_alumno, codigo_curso, fecha_matricula=None):
    conn = get_connection()
    cursor = conn.cursor()
    # Si no se indica fecha, usamos la actual
    if fecha_matricula is None:
        fecha_matricula = datetime.now().strftime("%Y-%m-%d")
    # comprobamos si ya existe la matrícula
    cursor.execute("""
        SELECT COUNT(*) FROM matriculas
        WHERE nif_alumno = ? AND codigo_curso = ?
    """, (nif_alumno, codigo_curso))
    if cursor.fetchone()[0] > 0:
        conn.close()
        return False
    cursor.execute("INSERT INTO matriculas (nif_alumno, codigo_curso) VALUES (?, ?)", (nif_alumno, codigo_curso))
    conn.commit()
    conn.close()
    return True

# --- Obtener todas las matrículas (con JOINs para mostrar nombres) ---
def obtener_matriculas():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT a.nif, a.nombre || ' ' || a.apellidos as nombre,
            c.codigo_curso, c.nombre AS curso, m.fecha_matricula
        FROM matriculas m
        JOIN alumnos a ON m.nif_alumno = a.nif
        JOIN cursos c ON m.codigo_curso = c.codigo_curso
        ORDER BY m.fecha_matricula DESC
    """)
    datos = cursor.fetchall()
    conn.close()
    return datos

# --- Eliminar matrícula ---
def eliminar_matricula(id_matricula):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM matriculas WHERE id = ?", (id_matricula,))
    conn.commit()
    conn.close()
    print(f"🗑️ Matrícula {id_matricula} eliminada.")

#--- Buscar cursos por alumno ---
def obtener_cursos_por_alumno(nif_alumno):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            c.codigo_curso,
            c.nombre,
            c.fecha_inicio,
            c.fecha_fin,
            CASE 
                WHEN date(c.fecha_fin) < date('now') THEN 'Finalizado'
                WHEN date(c.fecha_inicio) > date('now') THEN 'Abierto'
                ELSE 'En curso'
            END AS estado
        FROM matriculas m
        JOIN cursos c ON m.codigo_curso = c.codigo_curso
        WHERE m.nif_alumno = ?
        ORDER BY c.fecha_inicio DESC
    """, (nif_alumno,))
    datos = cursor.fetchall()
    conn.close()
    return datos

#--- Buscar alumnos por curso ---
def obtener_alumnos_por_curso(codigo_curso):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            a.nif,
            a.nombre || ' ' || a.apellidos AS alumno,
            a.telefono,
            a.email,
            CASE 
                WHEN date(c.fecha_fin) < date('now') THEN 'Finalizado'
                WHEN date(c.fecha_inicio) > date('now') THEN 'Pendiente'
                ELSE 'En curso'
            END AS estado_curso
        FROM matriculas m
        JOIN alumnos a ON m.nif_alumno = a.nif
        JOIN cursos c ON m.codigo_curso = c.codigo_curso
        WHERE m.codigo_curso = ?
        ORDER BY a.apellidos, a.nombre
    """, (codigo_curso,))
    datos = cursor.fetchall()
    conn.close()
    return datos

