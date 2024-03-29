""" 
En el desarrollo de este programa, utilicé la librería face-recognition 
junto con métodos de Numpy para implementar un sistema de vigilancia y 
asistencia que permite detectar rostros a través de una cámara en 
tiempo real y registrar una asistencia en una base de datos MySQL. Esta 
tecnología permite llevar a cabo diversas funciones, como el reconocimiento 
facial en eventos, la gestión de asistentes o la optimización de procesos 
de identificación para una empresa. Los datos de asistencia se almacenan de 
manera segura y eficiente en una base de datos MySQL, lo que permite un 
acceso rápido y confiable a la información de asistencia para su posterior 
análisis y generación de informes.
"""


from cv2 import cv2
import face_recognition as fr
import os
import numpy
from datetime import datetime
import mysql.connector

# Database connection configuration
db_config = {
    'host': 'localhost',
    'user': 'your_username',
    'password': 'your_password',
    'database': 'your_database'
}

# Create a database connection
db_connection = mysql.connector.connect(**db_config)
db_cursor = db_connection.cursor()

# Create the 'attendance' table in the database (if it doesn't exist)
db_cursor.execute("CREATE TABLE IF NOT EXISTS attendance (id INT AUTO_INCREMENT PRIMARY KEY, employee_name VARCHAR(255), entry_time DATETIME)")

# Remaining code...

# crear base de datos
ruta = 'Empleados'
mis_imagenes = []
nombres_empleados = []
lista_empleados = os.listdir(ruta)

for nombre in lista_empleados:
    imagen_actual = cv2.imread(f'{ruta}/{nombre}')
    mis_imagenes.append(imagen_actual)
    nombres_empleados.append(os.path.splitext(nombre)[0])

print(nombres_empleados)

# codificar imagenes
def codificar(imagenes):
    # crear una lista nueva
    lista_codificada = []

    # pasar todas las imagenes a rgb
    for imagen in imagenes:
        imagen = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)

        # codificar
        codificado = fr.face_encodings(imagen)[0]

        # agregar a la lista
        lista_codificada.append(codificado)

    # devolver lista codificada
    return lista_codificada

# registrar los ingresos
def registrar_ingresos(persona):
    ahora = datetime.now()
    string_ahora = ahora.strftime('%H:%M:%S')

    # Insert the attendance record into the database
    insert_query = "INSERT INTO attendance (employee_name, entry_time) VALUES (%s, %s)"
    insert_values = (persona, string_ahora)
    db_cursor.execute(insert_query, insert_values)
    db_connection.commit()

lista_empleados_codificada = codificar(mis_imagenes)

# tomar una imagen de camara web
captura = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# leer imagen de la camara
exito, imagen = captura.read()

if not exito:
    print("No se ha podido tomar la captura")
else:
    # reconocer cara en captura
    cara_captura = fr.face_locations(imagen)

    # codificar cara capturada
    cara_captura_codificada = fr.face_encodings(imagen, cara_captura)

    # buscar coincidencias
    for caracodif, caraubic in zip(cara_captura_codificada, cara_captura):
        coincidencias = fr.compare_faces(lista_empleados_codificada, caracodif)
        distancias = fr.face_distance(lista_empleados_codificada, caracodif)

        print(distancias)

        indice_coincidencia = numpy.argmin(distancias)

        # mostrar coincidencias si las hay
        if distancias[indice_coincidencia] > 0.6:
            print("No coincide con ninguno de nuestros empleados")
        else:
            # buscar el nombre del empleado encontrado
            nombre = nombres_empleados[indice_coincidencia]

            y1, x2, y2, x1 = caraubic
            cv2.rectangle(imagen, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(imagen, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(imagen, nombre, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 2555, 255), 2)

            registrar_ingresos(nombre)

            # mostrar la imagen obtenida
            cv2.imshow('Imagen web', imagen)

            # mantener ventana abierta
            cv2.waitKey(0)

# Close the database connection when done
db_cursor.close()
db_connection.close()

