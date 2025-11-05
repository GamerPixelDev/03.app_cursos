import os
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill
from models import alumnos, cursos, matriculas

# Carpeta de salida
EXPORT_DIR = os.path.join(os.path.dirname(__file__), "..", "exports")
os.makedirs(EXPORT_DIR, exist_ok=True)

def exportar_alumnos_excel():
    datos = alumnos.obtener_alumnos()
    wb = Workbook()
    ws = wb.active
    ws.title = "Alumnos"
    # Encabezados
    columnas = [
        "NIF", "Nombre", "Apellidos", "Localidad", "Código Postal",
        "Email", "Teléfono", "Sexo", "Edad", "Estudios", "Estado Laboral"
    ]
    ws.append(columnas)
    # Estilos de encabezado
    for col in ws[1]:
        col.font = Font(bold=True, color="FFFFFF")
        col.alignment = Alignment(horizontal="center")
    ws.row_dimensions[1].height = 20
    for i, cell in enumerate(ws[1], start=1):
        ws.cell(row=1, column=i).fill = PatternFill("solid", fgColor="3E64FF")
    # Datos
    for fila in datos:
        ws.append(fila)
    # Ajustar anchos de columna
    for col in ws.columns:
        max_len = max(len(str(cell.value or "")) for cell in col)
        ws.column_dimensions[col[0].column_letter].width = max_len + 2
    # Guardar archivo
    ruta = os.path.join(EXPORT_DIR, "alumnos.xlsx")
    wb.save(ruta)
    return ruta
