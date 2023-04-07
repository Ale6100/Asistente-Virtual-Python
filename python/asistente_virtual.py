import pyttsx3 # Conversión de texto a voz
import speech_recognition as sr # Reconocimiento de voz
import sys # Interacción con el intérprete de Python, lo uso para mejorar la interacción con JavaScript
import threading
import utils

'''
Todos los pedidos deben iniciar con el nombre del asistente (actualmente se llama "Okey")

Algunas palabras clave: (la mayoría tiene alguna variante. Por ejemplo en vez de decir "abre" se puede decir "abrís")
    "cancelar"      Ejemplo: "Okey, basta en un minuto. No, cancelar"           | Cancela el pedido siempre y cuando la palabra "cancela" esté al final
    "en n minutos"  Ejemplo: "Okey, videos de gatos en YouTube en 2 minutos"    | Elimina "Okey, ... en n minutos" y programa la ejecución de otro pedido para dentro de n minutos (n debe ser un numero)
    "busacr X en Y" Ejemplo: "Okey, buscar oso en windows"                       | Elimina "Okey, buscar ... en Y" y busca en el sitio Y lo que le pediste

    "basta"         Ejemplo: "Okey, basta"                                      (apaga al asistente)
'''

#! Variables iniciales
name = 'okay' # Le definimos un nombre al asistente, o simplemente una palabra clave que hace que se active
intentos = 0
continuar = True

#! Configuración de audio
engine = pyttsx3.init()

engine.setProperty('rate', 150) # Velocidad del asistente al hablar
engine.setProperty('volume', 1.0) # Volumen del asistente

voices = engine.getProperty('voices') # Accedemos al objeto "voices". Hacemos esto para obtener todas las voces del reproductor
if any('ES' in v.id for v in voices): # Analiza las voces instaladas del sistema y trata de colocar español (de preferencia) o inglés
    v_elegida = next((v for v in voices if 'ES' in v.id), None)
elif any('EN' in v.id for v in voices):
    v_elegida = next((v for v in voices if 'EN' in v.id), None)
else:
    v_elegida = voices[0].id  # Si no encuentra ninguna, usa la primer voz de la lista
engine.setProperty('voice', v_elegida)

#! Configuramos los mensajes en la consola y la salida de audio
def print_(text: str):
    print(text)
    sys.stdout.flush() # Pongo esto para que se vacie el búfer de salida estándar después de cada print para que el evento message de JavaScript funcione en tiempo real

def print_and_talk(text: str): # El reproductor lee el texto pasado como argumento pero primero lo imprime                        
    print_(text)
    engine.say(text)  
    engine.runAndWait()

#! Configuramos el detenimiento del asistente
def detener():
    print_and_talk('Apagando')
    global continuar
    continuar = False
    
#! Configuramos el conteo de instancias
def otro_intento():
    global intentos
    intentos += 1 

#! Iniciamos al asistente
def run():
    rec = listen() # Retorna el pedido de un usuario
    if rec == f'-${name} no se pudo conectar a internet-': return None # No trata de ejecutar ningún pedido si falló la conexión con internet
    posicion_inicio_name = rec.find(f'{name}') # Busca la posición donde inicia el nombre del asistente
    rec = rec[posicion_inicio_name : len(rec)] # Recorta la grabación hasta el momento donde se dice el nombre
    print_(f'Dijiste: {rec}') # Te muestra lo que quedó de la grabación
    rec = rec[len(name)+1 : len(rec)] # Recorta el nombre del asistente
    pedidos(rec)

def listen() -> str: # Se llama a sí misma hasta que detecte que se llamó al asistente por su nombre
    rec = reconocer_voz_y_pasarlo_a_texto()
    if name not in rec: rec = listen()
    return rec

def reconocer_voz_y_pasarlo_a_texto() -> str: # Se llama a si misma hasta que reconozca algúna voz
    otro_intento()
    try:
        with sr.Microphone() as source: # Abrimos el micrófono como fuente de entrada de audio
            listener = sr.Recognizer()
            listener.adjust_for_ambient_noise(source, duration = 1) # Ajusta el nivel de ruido ambiental. Duration son los segundos que tarda en ajustar el ruido ambiental            
            print_(f'\n{intentos}) Escuchando...')
            voice = listener.listen(source, timeout=10) # Acá comienza a escuchar. Tiene una tolerancia máxima de 10 segundos de no escuchar nada. Sirve para tratar de evitar que la grabación se trabe por estar encendida mucho tiempo
            print_('Procesando...')
            return listener.recognize_google(voice, language = 'es-AR', show_all=False).lower() # Acá se almacena lo que se grabó. Usa el servicio de Google para reconocer el habla en español argentino y lo convierte a minúsculas. Da error cuando no escucha nada             
    except sr.RequestError: # Si hay un fallo de conexión, intenta tres veces arrancar el programa. Si a la número tres no vuelve la conexión, se cierra. (Hay 10 segundos entre cada intento)
        print_and_talk('Fallo de conexión a internet')
        detener()
        return f'-${name} no se pudo conectar a internet-'
    except sr.UnknownValueError:
        print_('No se escuchó nada. Reintentando...')
        return reconocer_voz_y_pasarlo_a_texto()
    except sr.WaitTimeoutError:
        print_("Tiempo de espera agotado. Reintentando...")
        return reconocer_voz_y_pasarlo_a_texto()
    except Exception as e:
        print_and_talk(f'Error desconocido en el reconocimiento:\n{e}')
        return reconocer_voz_y_pasarlo_a_texto()

#! Lógica y reconocimiento de los pedidos
def pedidos(rec: str) -> str:
    rec = rec.replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u').replace('Á', 'A').replace('É', 'E').replace('Í', 'I').replace('Ó', 'O').replace('Ú', 'U') # Quito todas las tildes
    rec = utils.eliminar_frases_introductorias(rec, ['necesito', 'podrias', 'seria bueno', 'por favor', 'quiero', 'gustaria', 'serias tan amable de', 'interesaria', 'seria de gran ayuda si', 'harias un gran favor si pudieras', 'que', 'podes', 'puedes', 'estaria bueno', 'sos capaz de', "me", "che"])
    rec = utils.eliminar_frases_finales(rec)

    try:
        if len(rec) == 0: print_and_talk('¿Qué pasa?') # Si el pedido incluía sólo el nombre
        
        elif pedidoPreciso(rec): None # Considero dos tipos de pedidos distintos. Si hacemos un "pedido preciso", esta función ejecuta el pedido solicitado y devuelve True
        
        elif pedidoGenerico(rec): None
    
        else: print_and_talk('No te entendí') # Si detecta algo pero no lo entiende o se pide algo que no está programado, dice "No te entendí"
    except Exception as e:
        print_and_talk(f'Error desconocido:\n{e}') # Si hay un error no previsto, dice "Error desconocido", muestra el error y vuelve al while

def pedidoPreciso(rec: str) -> bool: # Denomino "pedido preciso" a todos aquellos pedidos que necesitan ser solicitados de manera específica, no de cualquier forma
    if False: pass
    
    elif any(word == rec.split(' ')[-1] for word in ['cancela', 'cancelar', 'cancelas', 'cancelalo', 'olvidalo']): # Cancela el pedido actual siempre y cuando digamos "cancelar" como última palabra (o alguna variante similar)
        print_and_talk('Ok, cancelo el pedido')
    
    elif any(word == rec.split(' ')[-1] for word in ['minuto', 'minutos']): # Programa un pedido para dentro de X minutos
        rec_array = rec.split(' ')
        
        if rec_array[-2] == 'un': # Cambio 'un' por '1' en el pedido, ya que yo necesito que sea un número
            rec_array[-2] = '1'
            
        numero = rec_array[-2]
        rec = ' '.join(rec.split(' ')[:-3])
        threading.Timer(int(numero)*60, lambda: pedidos(rec)).start()
        print_and_talk('Ok, lo recordaré')
    
    elif utils.buscar(rec):
        print_and_talk('Hecho')
    
    else: return False
    return True

def pedidoGenerico(rec: str) -> bool:
    if False: pass
    elif any(word in rec for word in ['basta', 'apaga', 'apagues']): detener() # Apaga al asistente
    else: return False
    return True

#! Ciclo para hacer que el asistente no termine nunca a menos que se lo pidamos específicamente
def iniciar_asistente(): # Nos aseguramos de que el asistente no deje de estar activo una vez que lo iniciamos, siempre y cuando "continuar" sea True
    while continuar: # Oficialmente estará encendido siempre y cuando este while no termine
        run()
    engine.stop()

iniciar_asistente()
