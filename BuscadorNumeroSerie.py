"""
Para este programa utilize la libreria de 
expresiones regulares junto con algunos metodos
de pathlib para crear un buscador de archivos
con similitudes brindadas por el usuario.
"""


import os
import datetime
import math
import timeit
import re
from pathlib import Path

ruta = ("E:\\DEV\\Proyecto numeros en serie\\Mi_Gran_Directorio")

coincidencias = 0
encontradosN = []
encontradosA = []

pattern = r'N\D{3}-\d{5}'

def buscarserie(archivo, patron):

    estearchivo = open(archivo, "r")
    texto = estearchivo.read()
    if re.search(patron, texto):
        return re.search(patron, texto)
    else:
        return ""

def crearlista():
    for carpeta, subcarpeta, archivos in os.walk(ruta):
        for a in archivos:
            resultado = buscarserie(Path(carpeta,a), pattern)
            if resultado!= "":
                encontradosN.append((resultado.group()))
                encontradosA.append(a.title())

def iniciar():

    start_time = timeit.default_timer()

    indice = 0

    print(f"Fecha de búsqueda: [{datetime.datetime.now().strftime('%d/%m/%y')}]")
    print (f"ARCHIVO		NRO. SERIE")
    print (f"-------		----------")

    for a in encontradosA:
        print(f'{a}\t{encontradosN[indice]}')
        indice += 1

    print(f"Números encontrados: {len(encontradosN)}")

    elapsed_time = timeit.default_timer() - start_time

    print(f"Duración de la búsqueda: {math.ceil(elapsed_time)}")

crearlista()

iniciar()