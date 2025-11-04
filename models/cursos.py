import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)
DB_PATH = os.path.join(ROOT_DIR, "data", "database.db")

def get_conection():
    return sqlite3.connect(DB_PATH)

#--- Crear curso ---
def crear_curso(codigo_curso, nombre, fecha_inicio, fecha_fin, lugar, modalidad, horas, responsable):
    conn = get_conection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO cursos (codigo_curso, nombre, fecha_inicio, fecha_fin, lugar, modalidad, horas, responsable)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (codigo_curso, nombre, fecha_inicio, fecha_fin, lugar, modalidad, horas, responsable)
        )
        conn.commit()
        print(f"✅ Curso '{nombre}' añadido correctamente.")
    except sqlite3.IntegrityError:
        print(f"⚠️ El código de curso '{codigo_curso}' ya existe.")
    finally:
        conn.close()

#--- Ontener todos los cursos ---
def obtener_cursos():
    conn = get_conection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cursos ORDER BY codigo_curso DESC")
    datos = cursor.fetchall()
    conn.close()
    return datos

#--- Eliminar curso por el código ---
def eliminar_curso(codigo_curso):
    conn = get_conection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM cursos WHERE codigo_curso = ?", (codigo_curso,))
    conn.commit()
    conn.close()
    print(f"🗑️ Curso con CÓDIGO {codigo_curso} eliminado.")

#--- Actualizar curso ---
def actualizar_curso(codigo_curso, campo, nuevo_valor):
    conn = get_conection()
    cursor = conn.cursor()
    cursor.execute(f"UPDATE cursos SET {campo} = ? WHERE codigo_curso = ?", (nuevo_valor, codigo_curso))
    conn.commit()
    conn.close()
    print(f"✏️ Curso {codigo_curso} actualizado: {campo} = {nuevo_valor}")

#--- Obtener datos de un curso ---
def obtener_datos_curso(codigo_curso):
    conn = get_conection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT nombre, fecha_inicio, fecha_fin, lugar, modalidad, horas, responsable
        FROM cursos
        WHERE codigo_curso = ?
    """, (codigo_curso,))
    datos = cursor.fetchone()
    conn.close()
    return datos