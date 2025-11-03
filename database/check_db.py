import sqlite3
import os

#=== RUTA DE LA BASE DE DATOS ===
DB_PATH = os.path.join("data", "database.db")
#Conexión
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()
#Mostramos las tablas existentes
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("Tablas existentes en la base de datos:")
for table in tables:
    nombre_tabla = table[0]
    print(f"- {nombre_tabla}")
    #Para cada tabla, mostramos sus columnas
    cursor.execute(f"PRAGMA table_info({nombre_tabla});")
    columnas = cursor.fetchall()
    for col in columnas:
        print(f"    - {col[1]} ({col[2]})")
    print()  # Línea en blanco entre tablas
#Cerramos conexión
conn.close()