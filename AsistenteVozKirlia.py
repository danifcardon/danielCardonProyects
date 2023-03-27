"""
Este programa es un asistente de voz llamado "Kirlia", 
realizado utilizando la librería “Speech Recognition” 
junto con numerosas librerías de información de Python, 
capaz de recibir información de la entrada del micrófono del usuario, 
procesarla y proporcionar la respuesta adecuada. 
Este programa ha sido diseñado teniendo en cuenta la eficiencia 
y la escalabilidad, lo que permite la incorporación de nuevas 
funcionalidades a la aplicación de manera ágil y sencilla. 
Además, gracias a su tecnología, este asistente de voz representa 
una herramienta eficaz para mejorar la interacción del usuario con 
la tecnología y optimizar el acceso a la información, especialmente 
para personas con discapacidades que pueden tener dificultades 
para utilizar dispositivos convencionales.

"""


import pyttsx3
import speech_recognition as sr
import pywhatkit
import yfinance as yf
import pyjokes
import webbrowser
import datetime
import wikipedia

#escuchar microfono y devolver audio como string
def transformar_audio_en_texto():

    #almacenar recognizer en variable
    r = sr.Recognizer()
    
    #configurar microfono
    with sr.Microphone() as origen:

        #tiempo de espera
        r.pause_threshold = 0.8

        #informar que comenzo la grabacion
        print("Iniciando grabacion...")

        #guardar la grabacion
        audio = r.listen(origen)

        try:
            #buscar en google
            pedido = r.recognize_google(audio, language='es-ar')

            #imprimir en pantalla lo escuchado
            print("Dijiste: " + pedido)

            #devolver pedido
            return pedido

        #en caso de que no comprenda el audio
        except sr.UnknownValueError:

            #prueba de que no comprendio
            print("No se reconozco el audio")
            
            #devolver error
            return "sigo escuchando"
        
        #en caso de no resolver el pedido
        except sr.RequestError:

            #prueba de que no comprendio
            print("No se reconozco el audio")

            #devolver error
            return "sigo escuchando"
        
        #error inesperado
        except:

            #prueba de que no comprendio
            print("No se reconozco el audio")

            #devolver error
            return "sigo escuchando"


#funcion para que el asistente pueda ser escuchado
def hablar(mensaje):

    #encender el motor de pyttsx3
    engine = pyttsx3.init()

    #pronunciar mensaje
    engine.say(mensaje)
    engine.runAndWait()


#informar el dia de la semana
def pedir_dia():

    #crear la variable con datos del dia
    dia = datetime.date.today()
    
    #crear variable para el dia de la semana
    dia_semana = dia.weekday()

    #diccionario con los dias de la semana
    calendario = {0: "Lunes", 1: "Martes", 2: "Miércoles", 3: "Jueves", 4: "Viernes", 5: "Sábado", 6: "Domingo"}

    #decir el dia de la semana
    hablar("Hoy es " + calendario[dia_semana])


#inforar la hora
def pedir_hora():

    #crear una variable con datos de la hora
    hora = datetime.datetime.now()
    hora = f"En este momento son las {hora.hour} con {hora.minute}"

    #decir la hora
    hablar(hora)


#funcion saludo inicial
def saludo_inicial():

    #crear variable con datos de la hora
    hora = datetime.datetime.now()
    if hora.hour < 6 or hora.hour > 20:
        momento = "Buenas noches"
    elif hora.hour >= 6 and hora.hour < 13:
        momento = "Buen día"
    else:
        momento = "Buenas tardes"
        

    #decir el saludo
    hablar(f"{momento}, soy Kirlia, tu asistente personal. Por favor dime en que te puedo ayudar.")


#funcion central del asistente
def main():

    #activar el saludo inicial
    saludo_inicial()
    
    #variable de corte
    comenzar = True

    #Loop central
    while comenzar:

        #activar el micro y guardar el pedido en un string
        pedido = transformar_audio_en_texto().lower()

        if "abrir youtube" in pedido:
            hablar("Con gusto, estoy abriendo youtube")
            webbrowser.open("https://www.youtube.com")
            continue

        elif "abrir google" in pedido:
            hablar("Con gusto, estoy abriendo google")
            webbrowser.open("https://www.google.com")
            continue

        elif "es hoy" in pedido:
            pedir_dia()
            continue

        elif "hora es" in pedido:
            pedir_hora()
            continue

        elif "busca en wikipedia" in pedido:
            hablar("Con gusto, estoy abriendo wikipedia para buscarlo")
            pedido = pedido.replace("busca en wikipedia", "")
            wikipedia.set_lang("es")
            resultado = wikipedia.summary(pedido, sentences=3)
            hablar(f"Wikipedia dice lo siguiente: ")
            hablar(resultado)
            continue

        elif "busca en internet" in pedido:
            hablar("Con gusto, estoy abriendo internet para buscarlo")
            pedido = pedido.replace("busca en internet", "")
            pywhatkit.search(pedido)
            hablar("Esto he encontrado en internet")
            continue

        elif "reproducir" in pedido:
            hablar("Buena eleccion, reproduccion en camino")
            pedido = pedido.replace("reproducir", "")
            pywhatkit.playonyt(pedido)
            continue

        elif "broma" in pedido:
            hablar(pyjokes.get_joke("es"))
            continue

        elif "precio de las acciones" in pedido:
            accion = pedido.split("de")[-1].strip()
            cartera = {"apple":"APPL", "amazon":"AMZN", "google":"GOOG", "microsoft":"MSFT"}
            
            try:
                accionbuscada = cartera[accion]
                accion_buscada = yf.Ticker(accionbuscada)
                precioactual = accion_buscada.info["regularMarketPrice"]
                hablar(f"El precio de la accion {accion} es de {precioactual}")
            except:
                hablar("Perdon, no la he encontrado.")

        elif "adiós" in pedido:
            hablar("Adios")
            break


main()
