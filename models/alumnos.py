#=== Todo el código comentado pertenece a la version SQLite ===
#import sqlite3
import os
from models.db_connection import get_connection

#=== RUTA BASE DE DATOS ===#
#BASE_DIR = os.path.dirname(os.path.abspath(__file__))
#ROOT_DIR = os.path.dirname(BASE_DIR)
#DB_PATH = os.path.join(ROOT_DIR, "data", "database.db")

#def get_connection():
#    """Establece y devuelve una conexión a la base de datos SQLite."""
#   conn = sqlite3.connect(DB_PATH)
#    return conn

#Crear alumno
def crear_alumno(nif, nombre, apellidos, localidad, codigo_postal, telefono, email, sexo, edad, estudios, estado_laboral):
    conn = get_connection()
    cursor = conn.cursor()
    # comprobamos si el NIF ya existe
    cursor.execute("SELECT COUNT(*) FROM alumnos WHERE nif = ?", (nif,))
    if cursor.fetchone()[0] > 0:
        conn.close()
        return False  # ya existe, no insertamos
    cursor.execute("""
        INSERT INTO alumnos (nif, nombre, apellidos, localidad, codigo_postal, telefono, email, sexo, edad, estudios, estado_laboral)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (nif, nombre, apellidos, localidad, codigo_postal, telefono, email, sexo, edad, estudios, estado_laboral))
    conn.commit()
    conn.close()
    return True

#Obtener todos los alumnos
def obtener_alumnos():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM alumnos ORDER BY apellidos, nombre")
    alumnos = cursor.fetchall()
    conn.close()
    return alumnos

#Eliminar alumno por NIF
def eliminar_alumno(nif_alumno):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM alumnos WHERE nif = ?", (nif_alumno,))
    conn. commit()
    conn.close()
    print(f"🗑️ Alumno con NIF {nif_alumno} eliminado.")

#Actualizar alumno
def actualizar_alumno(nif_alumno, campo, nuevo_valor):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(f"UPDATE alumnos SET {campo} = ? WHERE nif = ?", (nuevo_valor, nif_alumno))
    conn.commit()
    conn.close()
    print(f"✏️ Alumno {nif_alumno} actualizado: {campo} = {nuevo_valor}")

#Obtener datos
def obtener_datos_alumno(nif):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT nombre, apellidos, localidad, codigo_postal, telefono, email, sexo, edad, estudios, estado_laboral
        FROM alumnos
        WHERE nif = ?
    """, (nif,))
    datos = cursor.fetchone()
    conn.close()
    return datos