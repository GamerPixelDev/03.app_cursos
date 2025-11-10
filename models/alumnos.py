#=== Todo el código comentado pertenece a la versión SQLite ===
#import sqlite3
#import os
from models.db_connection import get_connection
from models.utils_db import manejar_error_db

#=== RUTA BASE DE DATOS ===#
#BASE_DIR = os.path.dirname(os.path.abspath(__file__))
#ROOT_DIR = os.path.dirname(BASE_DIR)
#DB_PATH = os.path.join(ROOT_DIR, "data", "database.db")

#def get_connection():
#    Establece y devuelve una conexión a la base de datos SQLite.
#    conn = sqlite3.connect(DB_PATH)
#    return conn


#=== Crear alumno ===#
def crear_alumno(nif, nombre, apellidos, localidad, codigo_postal, telefono, email, sexo, edad, estudios, estado_laboral):
    #Inserta un nuevo alumno en la base de datos PostgreSQL.
    #Comprueba antes si el NIF ya existe para evitar duplicados.
    #Devuelve True si se inserta correctamente o False si ya existía.
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        # Comprobamos si el NIF ya existe (NIF es clave primaria o única)
        cursor.execute("SELECT COUNT(*) FROM alumnos WHERE nif = %s", (nif,))
        if cursor.fetchone()[0] > 0:
            print(f"⚠️  El alumno con NIF {nif} ya existe.")
            return False  # Ya existe, no insertamos
        # Insertamos nuevo alumno
        cursor.execute("""
            INSERT INTO alumnos (nif, nombre, apellidos, localidad, codigo_postal, telefono, email, sexo, edad, estudios, estado_laboral)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (nif, nombre, apellidos, localidad, codigo_postal, telefono, email, sexo, edad, estudios, estado_laboral))
        conn.commit()
        print(f"✅ Alumno {nombre} {apellidos} añadido correctamente.")
        return True
    except Exception as e:
        manejar_error_db(e, "crear alumno")
        return False
    finally:
        if 'conn' in locals() and conn:
            conn.close()

#=== Obtener todos los alumnos ===#
def obtener_alumnos():
    #Recupera todos los registros de alumnos ordenados por apellidos y nombre.
    #Devuelve una lista de tuplas con los datos.
    conn = None
    alumnos = []
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM alumnos ORDER BY apellidos, nombre")
        alumnos = cursor.fetchall()
        print(f"📋 {len(alumnos)} alumnos recuperados.")
    except Exception as e:
        manejar_error_db(e, "obtener alumnos")
        alumnos = []
    finally:
        if 'conn' in locals() and conn:
            conn.close()
        return alumnos

#=== Eliminar alumno por NIF ===#
def eliminar_alumno(nif_alumno):
    #Elimina un alumno de la base de datos según su NIF.
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM alumnos WHERE nif = %s", (nif_alumno,))
        conn.commit()
        print(f"🗑️ Alumno con NIF {nif_alumno} eliminado.")
    except Exception as e:
        manejar_error_db(e, "eliminar alumno")
    finally:
        if 'conn' in locals() and conn:
            conn.close()

#=== Actualizar alumno ===#
def actualizar_alumno(nif_alumno, campo, nuevo_valor):
    #Actualiza un campo específico del alumno identificado por su NIF.
    #El campo debe ser una columna válida del esquema 'alumnos'.
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        # ⚠️ Ojo: aquí no se usa placeholder en el nombre del campo porque no lo permite PostgreSQL,
        # por eso hay que garantizar que 'campo' venga de una lista controlada (no de input directo).
        cursor.execute(f"UPDATE alumnos SET {campo} = %s WHERE nif = %s", (nuevo_valor, nif_alumno))
        conn.commit()
        print(f"✏️ Alumno {nif_alumno} actualizado: {campo} = {nuevo_valor}")
    except Exception as e:
        manejar_error_db(e, "actualizar alumno")
    finally:
        if 'conn' in locals() and conn:
            conn.close()

#=== Obtener datos de un alumno ===#
def obtener_datos_alumno(nif):
    #Devuelve los datos detallados de un alumno según su NIF.
    #Si no existe, devuelve None.
    conn = None
    datos = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT nombre, apellidos, localidad, codigo_postal, telefono, email, sexo, edad, estudios, estado_laboral
            FROM alumnos
            WHERE nif = %s
        """, (nif,))
        datos = cursor.fetchone()
        if datos:
            print(f"👤 Datos obtenidos para NIF {nif}.")
        else:
            print(f"⚠️ No se encontró el alumno con NIF {nif}.")
    except Exception as e:
        manejar_error_db(e, "obtener datos de un alumno")
        datos = None
    finally:
        if 'conn' in locals() and conn:
            conn.close()
        return datos