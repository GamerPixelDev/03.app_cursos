import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)
DB_PATH = os.path.join(ROOT_DIR, "data", "database.db")

def get_connection():
    return sqlite3.connect(DB_PATH)

# --- Crear matrícula ---
def crear_matricula(nif_alumno, codigo_curso, fecha_matricula):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO matriculas (nif_alumno, codigo_curso, fecha_matricula)
            VALUES (?, ?, ?)
        """, (nif_alumno, codigo_curso, fecha_matricula))
        conn.commit()
        print(f"✅ Matrícula creada: alumno {nif_alumno} → curso {codigo_curso}")
    except sqlite3.IntegrityError:
        print("⚠️ Error: posible duplicado o datos inválidos.")
    finally:
        conn.close()

# --- Obtener todas las matrículas (con JOINs para mostrar nombres) ---
def obtener_matriculas():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT m.id, a.nombre || ' ' || a.apellidos AS alumno, 
            c.nombre AS curso, m.fecha_matricula
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