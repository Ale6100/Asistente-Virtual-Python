import pyttsx3 # Conversión de texto a voz
import speech_recognition as sr # Reconocimiento de voz
import threading
import scripts.utils as utils
import pyautogui
from datetime import datetime   #Importa la hora
import os
import pkg_resources
import shutil
import scripts.direcciones_ as direcciones_
import webbrowser
import pyjokes

#! Variables iniciales
usuario = os.environ.get('USERNAME') or os.environ.get('USER') # El usuario de tu PC actual
name = 'okay' # Le definimos un nombre al asistente, o simplemente una palabra clave que hace que se active
intentos = 0
continuar = True
cronometro = 0

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
def print_and_talk(text: str): # El reproductor lee el texto pasado como argumento pero primero lo imprime                        
    print(text)
    engine.say(text)
    if engine._inLoop: # Para que no entre en un loop y de error al llamar al runAndWait
        engine.endLoop()
    engine.runAndWait()

#! Configuramos el detenimiento del asistente
def detener():
    print_and_talk('Deteniendo')
    global continuar
    continuar = False
    
#! Configuramos el conteo de instancias
def otro_intento():
    global intentos
    intentos += 1 

#! Iniciamos al asistente
def run(q=None):
    rec = listen(q) # Retorna el pedido de un usuario
    if rec == f'-{name}-error-': return None # No trata de ejecutar ningún pedido si falló la conexión con internet
    posicion_inicio_name = rec.find(f'{name}') # Busca la posición donde inicia el nombre del asistente
    rec = rec[posicion_inicio_name :] # Recorta la grabación hasta el momento donde se dice el nombre
    print(f'Dijiste: {rec}') # Te muestra lo que quedó de la grabación
    rec = rec[len(name)+1 :] # Recorta el nombre del asistente
    pedidos(rec)

def listen(q=None) -> str: # Se llama a sí misma hasta que detecte que se llamó al asistente por su nombre
    rec = reconocer_voz_y_pasarlo_a_texto(q)
    if name not in rec: rec = listen()
    return rec

def reconocer_voz_y_pasarlo_a_texto(q=None) -> str: # Se llama a si misma hasta que reconozca algúna voz
    otro_intento()
    try:
        with sr.Microphone() as source: # Abrimos el micrófono como fuente de entrada de audio
            listener = sr.Recognizer()
            listener.adjust_for_ambient_noise(source, duration = 1) # Ajusta el nivel de ruido ambiental. Duration son los segundos que tarda en ajustar el ruido ambiental            
            print(f'\n{intentos}) Escuchando...')
            if q != None: q.put("Escuchando...")
            voice = listener.listen(source, timeout=10) # Acá comienza a escuchar. Tiene una tolerancia máxima de 10 segundos de no escuchar nada. Sirve para tratar de evitar que la grabación se trabe por estar encendida mucho tiempo
            print('Procesando...')
            if q != None: q.put("Espere...")
            return listener.recognize_google(voice, language = 'es-AR', show_all=False).lower() # Acá se almacena lo que se grabó. Usa el servicio de Google para reconocer el habla en español argentino y lo convierte a minúsculas. Da error cuando no escucha nada             
    except sr.RequestError: # Si hay un fallo de conexión, intenta tres veces arrancar el programa. Si a la número tres no vuelve la conexión, se cierra. (Hay 10 segundos entre cada intento)
        print_and_talk('Fallo de conexión a internet')
        detener()
    except sr.UnknownValueError:
        print('No se escuchó nada. Reintentando...')
    except sr.WaitTimeoutError:
        print("Tiempo de espera agotado. Reintentando...")
    except Exception as e:
        print_and_talk(f'Error desconocido en el reconocimiento:\n{e}')
    return f'-{name}-error-'

#! Lógica y reconocimiento de los pedidos
def pedidos(rec: str) -> str:
    try:
        if len(rec) == 0: return print_and_talk('¿Qué pasa?') # Si el pedido incluía sólo el nombre
        if rec == 'gracias' or rec == 'muchas gracias': return print_and_talk('De nada')
        if rec == 'hola': return print_and_talk('hola')
        
        rec = rec.replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u').replace('Á', 'A').replace('É', 'E').replace('Í', 'I').replace('Ó', 'O').replace('Ú', 'U') # Quito todas las tildes
        rec = utils.eliminar_frases_introductorias(rec, ['necesito', 'podrias', 'seria bueno', 'por favor', 'quiero', 'gustaria', 'serias tan amable de', 'interesaria', 'seria de gran ayuda si', 'harias un gran favor si pudieras', 'que', 'podes', 'puedes', 'estaria bueno', 'sos capaz de', "me", "che"])
        rec = utils.eliminar_frases_finales(rec)
        
        if pedidoPreciso(rec): None # Considero dos tipos de pedidos distintos. Si hacemos un "pedido preciso", esta función ejecuta el pedido solicitado y devuelve True
        
        elif pedidoGenerico(rec): None
    
        else: print_and_talk('No te entendí') # Si detecta algo pero no lo entiende o se pide algo que no está programado, dice "No te entendí"
    except Exception as e:
        print_and_talk(f'Error desconocido:\n{e}') # Si hay un error no previsto, dice "Error desconocido", muestra el error y vuelve al while

def pedidoPreciso(rec: str) -> bool: # Denomino "pedido preciso" a todos aquellos pedidos que necesitan ser solicitados de manera específica, no de cualquier forma
    if False: pass
    
    elif any(word == rec.split(' ')[-1] for word in ['cancela', 'cancelar', 'cancelas', 'cancelalo', 'olvidalo']): # Cancela el pedido actual siempre y cuando digamos "cancelar" como última palabra (o alguna variante similar)
        print_and_talk('Ok, cancelo el pedido')
    
    elif any(word == rec.split(' ')[-1] for word in ['minuto', 'minutos']) and (rec.split(' ')[-3] == 'en'): # Programa un pedido para dentro de X minutos
        rec_array = rec.split(' ')
        
        if rec_array[-2] == 'un': # Cambio 'un' por '1' en el pedido, ya que yo necesito que sea un número
            rec_array[-2] = '1'
            
        numero = rec_array[-2]
        if numero.isdigit(): # Me aseguro de que el usuario haya especificado un número de minutos. Si no fue así, ignora el pedido y vuelve a empezar
            rec = ' '.join(rec.split(' ')[:-3]) # Quito "en X minutos" y solicito un pedido para después
            threading.Timer(int(numero)*60, lambda: pedidos(rec)).start()
            print_and_talk('Ok, lo recordaré')
    
    elif utils.buscar(rec): print_and_talk('Hecho')
        
    elif any(rec.startswith(word) for word in ['escribir ', 'escribis ', 'escribi ', 'escribes ', 'escribe ']):  # Escribe todo lo que le pediste
        pedido_escritura = utils.eliminar_frases_introductorias(rec, ['escribir', 'escribis', 'escribi', 'escribes', 'escribe'])
        pyautogui.typewrite(pedido_escritura)
        print_and_talk('Hecho')
        
    elif any(rec.startswith(word) for word in ['repeti ', 'repite ', 'deci ', 'repetis ', 'repetir ', 'repitas ']):  # Repite todo lo que le pediste
        pedido_repetir = utils.eliminar_frases_introductorias(rec, ['repeti', 'repite', 'deci', 'repetis', 'repetir', 'repitas'])
        print_and_talk(pedido_repetir)
    
    else: return False
    return True

def pedidoGenerico(rec: str) -> bool:
    if False: pass
    
    elif any(word in rec for word in ['estas ahi', 'estas por ahi', 'seguis ahi', 'me estas escuchando']): print_and_talk('Estoy aquí')    
    
    elif ' hora' in rec or rec.startswith('hora'): # Hora actual
        hora = datetime.now().strftime('%H:%M %p')
        print_and_talk(f'Son las {hora}')
        
    elif 'fecha' in rec:
        fecha = datetime.now().strftime('%d/%m/%Y') # Fecha actual
        print_and_talk(f'Hoy es {fecha}')
    
    elif "atajo " in rec and len(rec.split())-1 >= rec.split().index('atajo')+1:
        utils.atajos(rec, print_and_talk)
    
    elif any(word in rec for word in ['abri', 'abras', 'abre', 'ir a']): utils.abrir(rec, print_and_talk) #Abre archivos que estén en la biblioteca "direccion"
    
    elif any(word in rec for word in ['reprod', 'pone']) and any(word in rec for word in ['cancion', 'musica']):
        if os.path.exists(f'{direcciones_.direcciones["canciones"]["url"]}'):
            os.startfile(f'{direcciones_.direcciones["canciones"]["url"]}')
            pyautogui.press('volumedown', 50), pyautogui.press('volumeup', 10)
            print_and_talk('Reproduciendo música')
        else:
            print_and_talk(f'Error: debes colocar un archivo de audio para que yo pueda reproducirlo. Consulta el block de ayuda para más información, o sino puedes decir "{name} ayuda"')
    
    elif any(word in rec for word in ['cerrar', 'cierra']):                         
        pyautogui.hotkey('alt', 'F4')
        print_and_talk('Hecho')
        
    elif any(word in rec for word in ['mute', 'silenci']):
        pyautogui.hotkey('volumemute')
        print_and_talk('Hecho')
        
    elif 'minimiza' in rec and any(word in rec for word in ['todo', 'toda', 'los', 'las']): # Minimiza todas los programas
        pyautogui.hotkey('win', 'd')
        print_and_talk('Hecho')
        
    elif 'minimiza' in rec: # Minimiza el programa actual
        pyautogui.hotkey('alt', 'space', hold='down')
        pyautogui.press('n')
        print_and_talk('Hecho')
        
    elif 'volumen' in rec and '%' in rec: utils.volumen_al(rec, print_and_talk) # Cambia el volumen al X%
    
    elif 'chiste' in rec: print_and_talk(pyjokes.get_joke('es', category='all'))    
    
    elif any(word in rec for word in ['basta', 'apaga', 'apagues']): detener() # Apaga al asistente
    
    elif any(word in rec for word in ['como te llamas', 'cual es tu nombre']): print_and_talk(f'Me llamo {name}')    
    
    elif "tecla " in rec and len(rec.split())-1 >= rec.split().index('tecla')+1: # Si dice la palabra "tecla" en cualquier momento excepto en la palabra final, presiona la tecla pedida
        utils.apretar_tecla(rec, print_and_talk)    
    
    elif any(word in rec for word in ['captura de pantalla', 'estoy viendo', 'capturar pantalla', 'capturar pantalla', 'captura la pantalla', 'screenshot']): # Saca una captura de pantalla
        screenshot = pyautogui.screenshot()
        now = f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'.replace(' ', '_').replace(':', '_')
        screenshot.save(f'{now}_screenshot.png')
        print_and_talk('Captura guardada')
        
    elif 'cronometro' in rec and (any(word in rec for word in ['inicia', 'comenza', 'comienza']) or any(word in rec for word in ['detene', 'para', 'deten'])):
        global cronometro
        cronometro = utils.cronometro(rec, cronometro, print_and_talk)
        
    elif any(word in rec for word in ['ayuda', 'no entiendo', 'cosas puedes hacer', 'cosas podes hacer']):
        webbrowser.open(f'{direcciones_.direcciones["ayuda"]["url"]}')
        print_and_talk('Abriendo block de ayuda')
        
    elif 'ver codigo fuente' in rec:
        webbrowser.open(f'{direcciones_.direcciones["codigofuente"]["url"]}')
        print_and_talk('Abriendo código fuente')
    
    elif any(word in rec for word in ['actualizar asistente', 'actualizarte', 'actualizate', 'actualices']): #Para que el ".exe" del asistente se actualice
        if usuario == 'Ricardo': # Si alguien más aparte de mí accede a este if no hay problema, pero con esto trato de reducir esa posibilidad
            nombreAsistente = 'Asistente_virtual'
            print_and_talk('Actualizando asistente')
            os.chdir(f'{os.getcwd()}')
            os.system(f'pyinstaller --noconfirm --windowed --onefile --name "{nombreAsistente}" --add-binary "complementos/*;complementos" --add-data "scripts;scripts" --add-data "Asistente_virtual.py;Asistente_virtual.py" --icon=./complementos/z_robot.ico GUI.py')
            os.remove(f'{os.getcwd()}/{nombreAsistente}.spec')
            shutil.rmtree(f'{os.getcwd()}/build')
        else:
            None
    else: return False
    return True

#! Ciclo para hacer que el asistente no termine nunca a menos que se lo pidamos específicamente
def iniciar(q=None, stop_event=None): # Nos aseguramos de que el asistente no deje de estar activo una vez que lo iniciamos
    global continuar
    continuar = True
    
    if __name__ == '__main__':
        while continuar: # Si ejecutamos este script desde acá, no queremos usar los parámetros de la función
            run()
    else: # Si ejecutamos este código dede tkinter, necesitamos asegurarnos de no haber detenido el script desde el botón "Detener asistente"
        if continuar and not stop_event.is_set():
            q.put("Encendido") # Uso q.put para enviarle mensajes al tkinter
        
        while continuar and not stop_event.is_set():
            run(q)
            
        if stop_event.is_set():
            print_and_talk("Deteniendo")
            q.put("Detenido")
            
        if not continuar:
            q.put("Detenido")

    engine.stop()

if __name__ == '__main__': # Si este archivo de python se ejecuta acá (es decir, si no lo estamos ejecutando desde otro script), entonces iniciamos el asistente
    iniciar()
