#=== Todo el código comentado pertenece a la version SQLite ===
#import sqlite3
#import os
from models.db_connection import get_connection
from models.utils_db import manejar_error_db

#BASE_DIR = os.path.dirname(os.path.abspath(__file__))
#ROOT_DIR = os.path.dirname(BASE_DIR)
#DB_PATH = os.path.join(ROOT_DIR, "data", "database.db")

#def get_connection():
#    return sqlite3.connect(DB_PATH)

#--- Crear curso ---
def crear_curso(codigo_curso, nombre, fecha_inicio, fecha_fin, lugar, modalidad, horas, responsable):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        # comprobamos si el código de curso ya existe
        cursor.execute("SELECT COUNT(*) FROM cursos WHERE codigo_curso = ?", (codigo_curso,))
        if cursor.fetchone()[0] > 0:
            conn.close()
            return False
        cursor.execute("""
            INSERT INTO cursos (codigo_curso, nombre, fecha_inicio, fecha_fin, lugar, modalidad, horas, responsable)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (codigo_curso, nombre, fecha_inicio, fecha_fin, lugar, modalidad, horas, responsable))
        conn.commit()
    except Exception as e:
        manejar_error_db(e, "crear curso")
    finally:
        conn.close()
        return True

#--- Ontener todos los cursos ---
def obtener_cursos():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM cursos ORDER BY codigo_curso DESC")
        datos = cursor.fetchall()
    except Exception as e:
        manejar_error_db(e, "obtener cursos")
        return []
    finally:
        conn.close()
        return datos

#--- Eliminar curso por el código ---
def eliminar_curso(codigo_curso):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM cursos WHERE codigo_curso = ?", (codigo_curso,))
        conn.commit()
    except Exception as e:
        manejar_error_db(e, "eliminar curso")
    finally:    
        conn.close()
        print(f"🗑️ Curso con CÓDIGO {codigo_curso} eliminado.")

#--- Actualizar curso ---
def actualizar_curso(codigo_curso, campo, nuevo_valor):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(f"UPDATE cursos SET {campo} = ? WHERE codigo_curso = ?", (nuevo_valor, codigo_curso))
        conn.commit()
    except Exception as e:
        manejar_error_db(e, "actualizar curso")
    finally:
        conn.close()
        print(f"✏️ Curso {codigo_curso} actualizado: {campo} = {nuevo_valor}")

#--- Obtener datos de un curso ---
def obtener_datos_curso(codigo_curso):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT nombre, fecha_inicio, fecha_fin, lugar, modalidad, horas, responsable
            FROM cursos
            WHERE codigo_curso = ?
        """, (codigo_curso,))
        datos = cursor.fetchone()
    except Exception as e:
        manejar_error_db(e, "obtener datos de un curso")
        return []
    finally:
        conn.close()
        return datos
