import os
from openpyxl import load_workbook
from models import alumnos, cursos, matriculas

def importar_alumnos_desde_excel(ruta):
    wb = load_workbook(ruta)
    ws = wb.active
    filas = list(ws.iter_rows(values_only=True))
    encabezado = filas[0]
    datos = filas[1:]
    for fila in datos:
        nif, nombre, apellidos, localidad, cod_postal, correo, telefono, sexo, edad, estudios, estado_lab = fila
        alumnos.insertar_alumno(
            nif, nombre, apellidos, localidad, cod_postal, correo, telefono, sexo, edad, estudios, estado_lab
        )

def importar_cursos_desde_excel(ruta):
    wb = load_workbook(ruta)
    ws = wb.active
    filas = list(ws.iter_rows(values_only=True))
    encabezado = filas[0]
    datos = filas[1:]
    for fila in datos:
        codigo, nombre, fecha_inicio, fecha_fin, lugar, modalidad, horas, responsable = fila
        cursos.insertar_curso(codigo, nombre, fecha_inicio, fecha_fin, lugar, modalidad, horas, responsable)

def importar_matriculas_desde_excel(ruta):
    wb = load_workbook(ruta)
    ws = wb.active
    filas = list(ws.iter_rows(values_only=True))
    encabezado = filas[0]
    datos = filas[1:]
    for fila in datos:
        nif_alumno, codigo_curso = fila[:2]
        matriculas.guardar_matricula(nif_alumno, codigo_curso)
