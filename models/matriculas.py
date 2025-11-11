#=== Versión adaptada a PostgreSQL ===
from models.db_connection import get_connection
from models.utils_db import manejar_error_db
from datetime import datetime

#=== Crear matrícula ===#
def crear_matricula(nif_alumno, codigo_curso, fecha_matricula=None):
    #Inserta una nueva matrícula en la base de datos.
    #Si no se especifica fecha, se usa la fecha actual.
    #Devuelve True si se crea correctamente o False si ya existía.
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        # Si no se indica fecha, se asigna la fecha actual
        if fecha_matricula is None:
            fecha_matricula = datetime.now().strftime("%Y-%m-%d")
        # Comprobamos si el alumno ya está matriculado en ese curso
        cursor.execute("""
            SELECT COUNT(*) FROM matriculas
            WHERE nif_alumno = %s AND codigo_curso = %s
        """, (nif_alumno, codigo_curso))
        if cursor.fetchone()[0] > 0:
            print(f"⚠️  El alumno {nif_alumno} ya está matriculado en el curso {codigo_curso}.")
            return False
        # Insertamos la nueva matrícula
        cursor.execute("""
            INSERT INTO matriculas (nif_alumno, codigo_curso, fecha_matricula)
            VALUES (%s, %s, %s)
        """, (nif_alumno, codigo_curso, fecha_matricula))
        conn.commit()
        print(f"✅ Matrícula creada para alumno {nif_alumno} en el curso {codigo_curso}.")
        return True
    except Exception as e:
        manejar_error_db(e, "crear matrícula")
        return False
    finally:
        if 'conn' in locals() and conn:
            conn.close()

#=== Obtener todas las matrículas (con JOINs) ===#
def obtener_matriculas():
    #Recupera todas las matrículas junto con los nombres de alumnos y cursos.
    #Usa JOINs para mostrar información combinada.
    conn = None
    datos = []
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                a.nif,
                a.nombre || ' ' || a.apellidos AS alumno,
                c.codigo_curso,
                c.nombre AS curso,
                m.fecha_matricula
            FROM matriculas m
            JOIN alumnos a ON m.nif_alumno = a.nif
            JOIN cursos c ON m.codigo_curso = c.codigo_curso
            ORDER BY m.fecha_matricula DESC
        """)
        datos = cursor.fetchall()
        print(f"📋 {len(datos)} matrículas obtenidas.")
    except Exception as e:
        manejar_error_db(e, "obtener matrículas")
        datos = []
    finally:
        if 'conn' in locals() and conn:
            conn.close()
        return datos

#=== Eliminar matrícula ===#
def eliminar_matricula(id_matricula):
    #Elimina una matrícula específica según su ID.
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM matriculas WHERE id = %s", (id_matricula,))
        conn.commit()
        print(f"🗑️ Matrícula con ID {id_matricula} eliminada correctamente.")
    except Exception as e:
        manejar_error_db(e, "eliminar matrícula")
    finally:
        if 'conn' in locals() and conn:
            conn.close()

#=== Buscar cursos por alumno ===#
def obtener_cursos_por_alumno(nif_alumno):
    #Devuelve los cursos en los que un alumno está matriculado,
    #junto con su estado (Finalizado, Abierto o En curso),
    #calculado en función de las fechas de inicio y fin.
    conn = None
    datos = []
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                c.codigo_curso,
                c.nombre,
                c.fecha_inicio,
                c.fecha_fin,
                CASE 
                    WHEN c.fecha_fin < CURRENT_DATE THEN 'Finalizado'
                    WHEN c.fecha_inicio > CURRENT_DATE THEN 'Abierto'
                    ELSE 'En curso'
                END AS estado
            FROM matriculas m
            JOIN cursos c ON m.codigo_curso = c.codigo_curso
            WHERE m.nif_alumno = %s
            ORDER BY c.fecha_inicio DESC
        """, (nif_alumno,))
        datos = cursor.fetchall()
        print(f"🎓 {len(datos)} cursos encontrados para el alumno {nif_alumno}.")
    except Exception as e:
        manejar_error_db(e, "obtener cursos por alumno")
        datos = []
    finally:
        if 'conn' in locals() and conn:
            conn.close()
        return datos

#=== Buscar alumnos por curso ===#
def obtener_alumnos_por_curso(codigo_curso):
    #Devuelve los alumnos matriculados en un curso,
    #mostrando su información básica y el estado del curso.
    conn = None
    datos = []
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                a.nif,
                a.nombre || ' ' || a.apellidos AS alumno,
                a.telefono,
                a.email,
                CASE 
                    WHEN c.fecha_fin < CURRENT_DATE THEN 'Finalizado'
                    WHEN c.fecha_inicio > CURRENT_DATE THEN 'Pendiente'
                    ELSE 'En curso'
                END AS estado_curso
            FROM matriculas m
            JOIN alumnos a ON m.nif_alumno = a.nif
            JOIN cursos c ON m.codigo_curso = c.codigo_curso
            WHERE m.codigo_curso = %s
            ORDER BY a.apellidos, a.nombre
        """, (codigo_curso,))
        datos = cursor.fetchall()
        print(f"👥 {len(datos)} alumnos encontrados para el curso {codigo_curso}.")
    except Exception as e:
        manejar_error_db(e, "obtener alumnos por curso")
        datos = []
    finally:
        if 'conn' in locals() and conn:
            conn.close()
        return datos
    
def actualizar_fecha_matricula(nif_alumno, codigo_curso, nueva_fecha):
    """Actualiza la fecha de matrícula de un alumno en un curso."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE matriculas
            SET fecha_matricula = %s
            WHERE nif_alumno = %s AND codigo_curso = %s
        """, (nueva_fecha, nif_alumno, codigo_curso))
        conn.commit()
    except Exception as e:
        manejar_error_db(e, "actualizar fecha de matrícula")
    finally:
        conn.close()