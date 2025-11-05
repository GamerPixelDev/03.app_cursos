import os
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from models import alumnos, cursos, matriculas

EXPORT_DIR = os.path.join(os.path.dirname(__file__), "..", "exports")
os.makedirs(EXPORT_DIR, exist_ok=True)

def exportar_alumnos_pdf():
    datos = alumnos.obtener_alumnos()
    if not datos:
        raise ValueError("No hay alumnos para exportar.")
    # Ruta de salida
    nombre_archivo = os.path.join(EXPORT_DIR, f"alumnos_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf")
    # Crear documento (horizontal para más columnas)
    doc = SimpleDocTemplate(nombre_archivo, pagesize=landscape(A4), leftMargin=25, rightMargin=25, topMargin=40, bottomMargin=30)
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
        "Teléfono", "Email", "Sexo", "Edad", "Estudios", "Estado Laboral"
    ]
    # === estilo de texto para celdas ===
    cell_style = ParagraphStyle(
        'CellStyle',
        fontName='Helvetica',
        fontSize=8,
        leading=10,
        alignment=0,  # 0 = izquierda, 1 = centrado, 2 = derecha
    )
    # === encabezados de columnas ===
    columnas = [
        "NIF", "Nombre", "Apellidos", "Localidad", "CP",
        "Telf", "Email", "Sexo", "Edad", "Estudios", "Est Lab"
    ]
    # === construir datos con salto de línea automático ===
    tabla_datos = [columnas]
    for fila in datos:
        fila_modificada = [Paragraph(str(v) if v is not None else "", cell_style) for v in fila]
        tabla_datos.append(fila_modificada)
    # === anchos de columna equilibrados (en cm) ===
    colWidths = [
        2*cm,  # NIF
        3*cm,    # Nombre
        4*cm,    # Apellidos
        3*cm,    # Localidad
        1.7*cm,    # Código Postal
        2*cm,    # Teléfono
        5*cm,    # Email
        1*cm,    # Sexo
        1*cm,    # Edad
        4*cm,    # Estudios
        2*cm     # Estado Laboral
    ]
    # === crear tabla con cabecera repetida ===
    tabla = Table(tabla_datos, colWidths=colWidths, repeatRows=1)
    # === aplicar estilo visual ===
    tabla.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#3E64FF')),  # fondo azul cabecera
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 10),
        ('FONTSIZE', (0,1), (-1,-1), 8),
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

#=== EXPORTAR CURSOS ===
def exportar_cursos_pdf():
    datos = cursos.obtener_cursos()
    if not datos:
        raise ValueError("No hay cursos para exportar.")
    nombre_archivo = os.path.join(EXPORT_DIR, f"cursos_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf")
    doc = SimpleDocTemplate(
        nombre_archivo,
        pagesize=landscape(A4),
        leftMargin=25,
        rightMargin=25,
        topMargin=40,
        bottomMargin=30
    )
    elementos = []
    styles = getSampleStyleSheet()
    titulo = Paragraph("Listado de Cursos", styles["Title"])
    fecha = Paragraph(datetime.now().strftime("Generado el %d/%m/%Y a las %H:%M"), styles["Normal"])
    elementos.append(titulo)
    elementos.append(fecha)
    elementos.append(Spacer(1, 12))
    logo_path = os.path.join(os.path.dirname(__file__), "..", "icons", "logo.png")
    if os.path.exists(logo_path):
        elementos.insert(0, Image(logo_path, width=60, height=60))
    columnas = [
        "Código", "Nombre", "Fecha Inicio", "Fecha Fin", "Lugar",
        "Modalidad", "Horas", "Responsable"
    ]
    # Estilo de celdas multilínea
    cell_style = ParagraphStyle(
        'CellStyle',
        fontName='Helvetica',
        fontSize=8,
        leading=10,
        alignment=0
    )
    tabla_datos = [columnas]
    for fila in datos:
        fila_modificada = [Paragraph(str(v) if v is not None else "", cell_style) for v in fila]
        tabla_datos.append(fila_modificada)
    from reportlab.lib.units import cm
    colWidths = [
        2.5*cm,  # Código
        5*cm,    # Nombre
        3*cm,    # Fecha inicio
        3*cm,    # Fecha fin
        4*cm,    # Lugar
        3*cm,    # Modalidad
        2*cm,    # Horas
        4*cm     # Responsable
    ]
    tabla = Table(tabla_datos, colWidths=colWidths, repeatRows=1)
    tabla.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#3E64FF')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 10),
        ('FONTSIZE', (0,1), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,0), 8),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.whitesmoke, colors.lightgrey])
    ]))
    elementos.append(tabla)
    elementos.append(Spacer(1, 12))
    footer = Paragraph("Gestor de Cursos - Junta de Extremadura", styles["Normal"])
    elementos.append(footer)
    doc.build(elementos)
    return nombre_archivo

#=== EXPORTAR MATRÍCULAS ===
def exportar_matriculas_pdf():
    datos = matriculas.obtener_matriculas()
    if not datos:
        raise ValueError("No hay matrículas para exportar.")
    nombre_archivo = os.path.join(EXPORT_DIR, f"matriculas_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf")
    doc = SimpleDocTemplate(
        nombre_archivo,
        pagesize=landscape(A4),
        leftMargin=25,
        rightMargin=25,
        topMargin=40,
        bottomMargin=30
    )
    elementos = []
    styles = getSampleStyleSheet()
    titulo = Paragraph("Listado de Matrículas", styles["Title"])
    fecha = Paragraph(datetime.now().strftime("Generado el %d/%m/%Y a las %H:%M"), styles["Normal"])
    elementos.append(titulo)
    elementos.append(fecha)
    elementos.append(Spacer(1, 12))
    columnas = ["ID", "NIF Alumno", "Nombre Alumno", "Curso", "Código Curso", "Estado"]
    cell_style = ParagraphStyle('CellStyle', fontName='Helvetica', fontSize=8, leading=10, alignment=0)
    tabla_datos = [columnas]
    for fila in datos:
        fila_modificada = [Paragraph(str(v) if v is not None else "", cell_style) for v in fila]
        tabla_datos.append(fila_modificada)
    from reportlab.lib.units import cm
    colWidths = [2*cm, 3*cm, 4*cm, 5*cm, 3*cm, 3*cm]
    tabla = Table(tabla_datos, colWidths=colWidths, repeatRows=1)
    tabla.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#3E64FF')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 10),
        ('FONTSIZE', (0,1), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,0), 8),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.whitesmoke, colors.lightgrey])
    ]))
    elementos.append(tabla)
    elementos.append(Spacer(1, 12))
    footer = Paragraph("Gestor de Cursos - Junta de Extremadura", styles["Normal"])
    elementos.append(footer)
    doc.build(elementos)
    return nombre_archivo