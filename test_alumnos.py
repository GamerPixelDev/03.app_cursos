from models.alumnos_model import crear_alumno, obtener_alumnos

crear_alumno("12345678A", "Carlos", "Pérez", "Badajoz", "06001", "carlos@example.com",
            "600123456", "M", 30, "Grado", "Empleado")

alumnos = obtener_alumnos()
for a in alumnos:
    print(a)
