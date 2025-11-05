import os
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from models import alumnos

EXPORT_DIR = os.path.join(os.path.dirname(__file__), "..", "exports")
os.makedirs(EXPORT_DIR, exist_ok=True)

def exportar_alumnos_pdf():
    datos = alumnos.obtener_alumnos()
    if not datos:
        raise ValueError("No hay alumnos para exportar.")
    # Ruta de salida
    nombre_archivo = os.path.join(EXPORT_DIR, f"alumnos_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf")
    # Crear documento (horizontal para más columnas)
    doc = SimpleDocTemplate(nombre_archivo, pagesize=landscape(A4))
    elementos = []
    # --- Estilos y cabecera ---
    styles = getSampleStyleSheet()
    titulo = Paragraph("Listado de Alumnos", styles["Title"])
    fecha = Paragraph(datetime.now().strftime("Generado el %d/%m/%Y a las %H:%M"), styles["Normal"])
    elementos.append(titulo)
    elementos.append(fecha)
    elementos.append(Spacer(1, 12))
    # --- Logo (si existe) ---
    logo_path = os.path.join(os.path.dirname(__file__), "..", "icons", "logo.png")
    if os.path.exists(logo_path):
        elementos.insert(0, Image(logo_path, width=60, height=60))
    # --- Cabeceras de tabla ---
    columnas = [
        "NIF", "Nombre", "Apellidos", "Localidad", "Código Postal",
        "Email", "Teléfono", "Sexo", "Edad", "Estudios", "Estado Laboral"
    ]
    tabla_datos = [columnas] + [list(fila) for fila in datos]
    # --- Crear tabla ---
    tabla = Table(tabla_datos, repeatRows=1)
    tabla.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#3E64FF')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 10),
        ('BOTTOMPADDING', (0,0), (-1,0), 8),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.whitesmoke, colors.lightgrey])
    ]))
    elementos.append(tabla)
    elementos.append(Spacer(1, 12))
    # --- Pie de página ---
    footer = Paragraph("Gestor de Cursos - Junta de Extremadura", styles["Normal"])
    elementos.append(footer)
    # --- Construir PDF ---
    doc.build(elementos)
    return nombre_archivo
