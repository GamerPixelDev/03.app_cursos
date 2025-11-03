import sqlite3
import os

#=== Ruta de la base de datos ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)
DATA_DIR = os.path.join(ROOT_DIR, "data")
DB_PATH = os.path.join(DATA_DIR, "database.db")
#Crear la carpeta data si no existe
if not os.path.exists("data"):
    os.makedirs("data")
#=== Conexión a la base de datos ===
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()
#=== Creación de tablas ===
cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT UNIQUE,
        contraseña TEXT,
        rol TEXT
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS alumnos (
        nif TEXT PRIMARY KEY,
        nombre TEXT,
        apellidos TEXT,
        localidad TEXT,
        codigo_postal TEXT,
        telefono TEXT,
        email TEXT UNIQUE,
        sexo TEXT,
        edad INTEGER,
        estudios TEXT,
        estado_laboral TEXT
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS cursos (
        codigo_curso TEXT PRIMARY KEY,
        nombre TEXT,
        fecha_inicio TEXT,
        fecha_fin TEXT,
        lugar TEXT,
        modalidad TEXT,
        horas INTEGER,
        responsable TEXT
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS matriculas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nif_alumno TEXT,
        codigo_curso TEXT,
        fecha_matricula TEXT,
        FOREIGN KEY (nif_alumno) REFERENCES alumnos(nif),
        FOREIGN KEY (codigo_curso) REFERENCES cursos(codigo_curso)
    )
''')
#=== Confirmar cambios y cerrar conexión ===
conn.commit()
conn.close()
print("Base de datos creada o verificada correctamente.")