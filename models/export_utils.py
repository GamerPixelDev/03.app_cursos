import os
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill
from models import alumnos, cursos, matriculas, usuarios

# Carpeta de salida por defecto
EXPORT_DIR_DEFAULT = os.path.join(os.path.dirname(__file__), "..", "exports")
os.makedirs(EXPORT_DIR_DEFAULT, exist_ok=True)

# FUNCIÓN AUXILIAR PARA ELEGIR RUTA REAL
def _resolver_ruta(ruta_usuario):
    """
    Si ruta_usuario existe → usarla.
    Si es None o no existe → usar ruta por defecto.
    """
    if ruta_usuario and os.path.isdir(ruta_usuario):
        return ruta_usuario
    return EXPORT_DIR_DEFAULT

# ALUMNOS
def exportar_alumnos_excel(ruta_destino=None):
    datos = alumnos.obtener_alumnos()
    carpeta = _resolver_ruta(ruta_destino)
    archivo = os.path.join(carpeta, "alumnos.xlsx")
    wb = Workbook()
    ws = wb.active
    ws.title = "Alumnos"
    columnas = [
        "NIF", "Nombre", "Apellidos", "Localidad", "Código Postal",
        "Teléfono", "Email", "Sexo", "Edad", "Estudios", "Estado Laboral"
    ]
    ws.append(columnas)
    # Estilo cabecera
    for col in ws[1]:
        col.font = Font(bold=True, color="FFFFFF")
        col.alignment = Alignment(horizontal="center")
        col.fill = PatternFill("solid", fgColor="3E64FF")
    # Datos
    for fila in datos:
        ws.append(fila)
    # Ajustar ancho columnas
    for col in ws.columns:
        max_len = max(len(str(cell.value or "")) for cell in col)
        ws.column_dimensions[col[0].column_letter].width = max_len + 2
    wb.save(archivo)
    return archivo

# CURSOS
def exportar_cursos_excel(ruta_destino=None):
    datos = cursos.obtener_cursos()
    if not datos:
        raise ValueError("No hay cursos para exportar.")
    carpeta = _resolver_ruta(ruta_destino)
    archivo = os.path.join(carpeta, "cursos.xlsx")
    wb = Workbook()
    ws = wb.active
    ws.title = "Cursos"
    columnas = [
        "Código", "Nombre", "Fecha Inicio", "Fecha Fin",
        "Lugar", "Modalidad", "Horas", "Responsable"
    ]
    ws.append(columnas)
    for col in ws[1]:
        col.font = Font(bold=True, color="FFFFFF")
        col.alignment = Alignment(horizontal="center")
        col.fill = PatternFill("solid", fgColor="3E64FF")
    for fila in datos:
        ws.append(fila)
    for col in ws.columns:
        max_len = max(len(str(cell.value or "")) for cell in col)
        ws.column_dimensions[col[0].column_letter].width = max_len + 2
    wb.save(archivo)
    return archivo

# MATRÍCULAS
def exportar_matriculas_excel(ruta_destino=None):
    datos = matriculas.obtener_matriculas()
    if not datos:
        raise ValueError("No hay matrículas para exportar.")
    carpeta = _resolver_ruta(ruta_destino)
    archivo = os.path.join(carpeta, "matriculas.xlsx")
    wb = Workbook()
    ws = wb.active
    ws.title = "Matrículas"
    columnas = [
        "NIF", "Nombre Alumno", "Código Curso", "Curso", "Fecha Insc."
    ]
    ws.append(columnas)
    for col in ws[1]:
        col.font = Font(bold=True, color="FFFFFF")
        col.alignment = Alignment(horizontal="center")
        col.fill = PatternFill("solid", fgColor="3E64FF")
    for fila in datos:
        ws.append(fila)
    for col in ws.columns:
        max_len = max(len(str(cell.value or "")) for cell in col)
        ws.column_dimensions[col[0].column_letter].width = max_len + 2
    wb.save(archivo)
    return archivo