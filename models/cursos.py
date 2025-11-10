#=== Versión adaptada a PostgreSQL ===
from models.db_connection import get_connection
from models.utils_db import manejar_error_db

#=== Crear curso ===#
def crear_curso(codigo_curso, nombre, fecha_inicio, fecha_fin, lugar, modalidad, horas, responsable):
    #Inserta un nuevo curso en la base de datos PostgreSQL.
    #Comprueba si el código del curso ya existe antes de insertarlo.
    #Devuelve True si se crea correctamente o False si ya existía.
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        # Verificamos si el código ya está registrado
        cursor.execute("SELECT COUNT(*) FROM cursos WHERE codigo_curso = %s", (codigo_curso,))
        if cursor.fetchone()[0] > 0:
            print(f"⚠️  El curso con código {codigo_curso} ya existe.")
            return False
        # Insertamos el nuevo curso
        cursor.execute("""
            INSERT INTO cursos (codigo_curso, nombre, fecha_inicio, fecha_fin, lugar, modalidad, horas, responsable)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (codigo_curso, nombre, fecha_inicio, fecha_fin, lugar, modalidad, horas, responsable))
        conn.commit()
        print(f"✅ Curso '{nombre}' creado correctamente.")
        return True
    except Exception as e:
        manejar_error_db(e, "crear curso")
        return False
    finally:
        if 'conn' in locals() and conn:
            conn.close()

#=== Obtener todos los cursos ===#
def obtener_cursos():
    #Recupera todos los cursos ordenados por código descendente.
    #Devuelve una lista de tuplas con todos los registros.
    conn = None
    datos = []
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM cursos ORDER BY codigo_curso DESC")
        datos = cursor.fetchall()
        print(f"📋 {len(datos)} cursos recuperados.")
    except Exception as e:
        manejar_error_db(e, "obtener cursos")
        datos = []
    finally:
        if 'conn' in locals() and conn:
            conn.close()
        return datos

#=== Eliminar curso por código ===#
def eliminar_curso(codigo_curso):
    #Elimina un curso existente según su código único.
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM cursos WHERE codigo_curso = %s", (codigo_curso,))
        conn.commit()
        print(f"🗑️ Curso con código {codigo_curso} eliminado correctamente.")
    except Exception as e:
        manejar_error_db(e, "eliminar curso")
    finally:
        if 'conn' in locals() and conn:
            conn.close()

#=== Actualizar curso ===#
def actualizar_curso(codigo_curso, campo, nuevo_valor):
    #Actualiza un campo concreto del curso indicado por su código.
    #El nombre del campo debe ser una columna válida de la tabla 'cursos'.
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        # ⚠️ 'campo' no se pasa como parámetro porque PostgreSQL no permite
        # usar placeholders para nombres de columnas, por tanto debe validarse antes.
        cursor.execute(f"UPDATE cursos SET {campo} = %s WHERE codigo_curso = %s", (nuevo_valor, codigo_curso))
        conn.commit()
        print(f"✏️ Curso {codigo_curso} actualizado: {campo} = {nuevo_valor}")
    except Exception as e:
        manejar_error_db(e, "actualizar curso")
    finally:
        if 'conn' in locals() and conn:
            conn.close()

#=== Obtener datos de un curso ===#
def obtener_datos_curso(codigo_curso):
    #Recupera los datos detallados de un curso por su código.
    #Devuelve una tupla con la información o None si no existe.
    conn = None
    datos = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT nombre, fecha_inicio, fecha_fin, lugar, modalidad, horas, responsable
            FROM cursos
            WHERE codigo_curso = %s
        """, (codigo_curso,))
        datos = cursor.fetchone()
        if datos:
            print(f"📚 Datos obtenidos para el curso {codigo_curso}.")
        else:
            print(f"⚠️ No se encontró el curso con código {codigo_curso}.")
    except Exception as e:
        manejar_error_db(e, "obtener datos de un curso")
        datos = None
    finally:
        if 'conn' in locals() and conn:
            conn.close()
        return datos