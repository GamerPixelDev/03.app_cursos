import sqlite3
import os

#=== RUTA BASE DE DATOS ===#
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)
DB_PATH = os.path.join(ROOT_DIR, "data", "database.db")

def get_connection():
    """Establece y devuelve una conexión a la base de datos SQLite."""
    conn = sqlite3.connect(DB_PATH)
    return conn

#Crear alumno
def crear_alumno(nif, nombre, apellidos, localidad, codigo_postal, email, telefono, sexo, edad, estudios, estado_laboral):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO alumnos (nif, nombre, apellidos, localidad, codigo_postal, email, telefono, sexo, edad, estudios, estado_laboral)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (nif, nombre, apellidos, localidad, codigo_postal, email, telefono, sexo, edad, estudios, estado_laboral))
        conn.commit()
        print(f"✅ Alumno '{nombre} {apellidos}' añadido correctamente.")
    except sqlite3.IntegrityError:
        print(f"⚠️ El NIF '{nif}' ya existe.")
    finally:
        conn.close()

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