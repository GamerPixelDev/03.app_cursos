from pathlib import Path

from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm

from models import alumnos, cursos, matriculas
from models.export_paths import resolver_ruta_exportacion

# EXPORTAR ALUMNOS
def exportar_alumnos_pdf(*, usuario: str | None = None, ruta_destino: str | None = None):
    datos = alumnos.obtener_alumnos()
    if not datos:
        raise ValueError("No hay alumnos para exportar.")
    # Seleccionar ruta final
    carpeta = resolver_ruta_exportacion(usuario=usuario, ruta_destino=ruta_destino)
    nombre_archivo = carpeta / f"alumnos_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
    doc = SimpleDocTemplate(str(nombre_archivo), pagesize=landscape(A4),
                            leftMargin=25, rightMargin=25, topMargin=40, bottomMargin=30)
    elementos = []
    styles = getSampleStyleSheet()
    titulo = Paragraph("Listado de Alumnos", styles["Title"])
    fecha = Paragraph(datetime.now().strftime("Generado el %d/%m/%Y a las %H:%M"), styles["Normal"])
    elementos += [titulo, fecha, Spacer(1, 12)]
    # Logo
    logo_path = Path(__file__).resolve().parent.parent / "icons" / "logo.png"
    if logo_path.exists():
        elementos.insert(0, Image(str(logo_path), width=60, height=60))
    # Columnas
    columnas = ["NIF", "Nombre", "Apellidos", "Localidad", "CP",
                "Telf", "Email", "Sexo", "Edad", "Estudios", "Est Lab"]
    cell_style = ParagraphStyle('CellStyle', fontName='Helvetica', fontSize=8, leading=10, alignment=0)
    tabla_datos = [columnas]
    for fila in datos:
        tabla_datos.append([Paragraph(str(v) if v else "", cell_style) for v in fila])
    colWidths = [2*cm, 3*cm, 4*cm, 3*cm, 1.7*cm, 2*cm, 5*cm, 1*cm, 1*cm, 4*cm, 2*cm]
    tabla = Table(tabla_datos, colWidths=colWidths, repeatRows=1)
    tabla.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#3E64FF')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 10),
        ('FONTSIZE', (0,1), (-1,-1), 8),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.whitesmoke, colors.lightgrey])
    ]))
    elementos.append(tabla)
    elementos.append(Spacer(1, 12))
    elementos.append(Paragraph("Gestor de Cursos - Junta de Extremadura", styles["Normal"]))
    doc.build(elementos)
    return str(nombre_archivo)

# EXPORTAR CURSOS
def exportar_cursos_pdf(*, usuario: str | None = None, ruta_destino: str | None = None):
    datos = cursos.obtener_cursos()
    if not datos:
        raise ValueError("No hay cursos para exportar.")
    carpeta = resolver_ruta_exportacion(usuario=usuario, ruta_destino=ruta_destino)
    nombre_archivo = carpeta / f"cursos_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
    doc = SimpleDocTemplate(str(nombre_archivo), pagesize=landscape(A4),
                            leftMargin=25, rightMargin=25, topMargin=40, bottomMargin=30)
    elementos = []
    styles = getSampleStyleSheet()
    elementos += [
        Paragraph("Listado de Cursos", styles["Title"]),
        Paragraph(datetime.now().strftime("Generado el %d/%m/%Y a las %H:%M"), styles["Normal"]),
        Spacer(1, 12)
    ]
    logo_path = Path(__file__).resolve().parent.parent / "icons" / "logo.png"
    if logo_path.exists():
        elementos.insert(0, Image(str(logo_path), width=60, height=60))
    columnas = ["Código", "Nombre", "Fecha Inicio", "Fecha Fin", "Lugar",
                "Modalidad", "Horas", "Responsable"]
    cell_style = ParagraphStyle('CellStyle', fontName='Helvetica', fontSize=8, leading=10)
    tabla_datos = [columnas]
    for fila in datos:
        tabla_datos.append([Paragraph(str(v) if v else "", cell_style) for v in fila])
    colWidths = [2.5*cm, 5*cm, 3*cm, 3*cm, 4*cm, 3*cm, 2*cm, 4*cm]
    tabla = Table(tabla_datos, colWidths=colWidths, repeatRows=1)
    tabla.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#3E64FF')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.whitesmoke, colors.lightgrey])
    ]))
    elementos.append(tabla)
    elementos.append(Spacer(1, 12))
    elementos.append(Paragraph("Gestor de Cursos - Junta de Extremadura", styles["Normal"]))
    doc.build(elementos)
    return str(nombre_archivo)

# EXPORTAR MATRÍCULAS
def exportar_matriculas_pdf(*, usuario: str | None = None, ruta_destino: str | None = None):
    datos = matriculas.obtener_matriculas()
    if not datos:
        raise ValueError("No hay matrículas para exportar.")
    carpeta = resolver_ruta_exportacion(usuario=usuario, ruta_destino=ruta_destino)
    nombre_archivo = carpeta / f"matriculas_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
    doc = SimpleDocTemplate(str(nombre_archivo), pagesize=landscape(A4),
                            leftMargin=25, rightMargin=25, topMargin=40, bottomMargin=30)
    elementos = []
    styles = getSampleStyleSheet()
    elementos += [
        Paragraph("Listado de Matrículas", styles["Title"]),
        Paragraph(datetime.now().strftime("Generado el %d/%m/%Y a las %H:%M"), styles["Normal"]),
        Spacer(1, 12)
    ]
    columnas = ["NIF", "Nombre Alumno", "Código Curso", "Curso", "Fecha Insc."]
    cell_style = ParagraphStyle('CellStyle', fontName='Helvetica', fontSize=8, leading=10)
    tabla_datos = [columnas]
    for fila in datos:
        tabla_datos.append([Paragraph(str(v) if v else "", cell_style) for v in fila])
    colWidths = [2*cm, 3*cm, 4*cm, 5*cm, 3*cm]
    tabla = Table(tabla_datos, colWidths=colWidths, repeatRows=1)
    tabla.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#3E64FF')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.whitesmoke, colors.lightgrey])
    ]))
    elementos.append(tabla)
    elementos.append(Spacer(1, 12))
    elementos.append(Paragraph("Gestor de Cursos - Junta de Extremadura", styles["Normal"]))
    doc.build(elementos)
    return str(nombre_archivo)