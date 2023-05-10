import pyttsx3 # Conversión de texto a voz
import speech_recognition as sr # Reconocimiento de voz
import threading
import scripts.utils as utils
import pyautogui
from datetime import datetime #Importa la hora
import os
import shutil
import scripts.direcciones_ as direcciones_
import webbrowser
import pyjokes
import time
import random
import sys

#! Variables iniciales
usuario = os.environ.get('USERNAME') or os.environ.get('USER') # El usuario de tu PC actual
name = 'okay' # Le definimos un nombre al asistente, o simplemente una palabra clave que hace que se active
intentos = 0
continuar = True
cronometro = 0
humor = 5 # Porcentaje de humor al n%. Significa que va a poner un audio "gracioso" el n% de las veces en los pedidos que tengan humor configurado

#! Configuración de audio
engine = pyttsx3.init() # Inicializamos el motor de voz

engine.setProperty('rate', 145) # Velocidad del asistente al hablar
engine.setProperty('volume', 1.0) # Volumen del asistente

voices = engine.getProperty('voices') # Accedemos al objeto "voices". Hacemos esto para obtener todas las voces del motor
if any('ES' in v.id for v in voices): # Analiza las voces instaladas del sistema y trata de colocar español (de preferencia) o inglés
    v_elegida = next((v for v in voices if 'ES' in v.id), None)
elif any('EN' in v.id for v in voices):
    v_elegida = next((v for v in voices if 'EN' in v.id), None)
else: # Si no hay voces en español ni en inglés, se selecciona la primera voz disponible en la lista
    v_elegida = voices[0].id
engine.setProperty('voice', v_elegida)

#! Configuramos los mensajes en la consola y la salida de audio
def print_(text):
    print(text)
    sys.stdout.flush() # Pongo esto para que se vacíe el búfer de salida estándar después de cada print para que los prints se envíen al proceso padre (correspondiente al GUI.py) en tiempo real

def print_and_talk(text: str): # El asistente imprime el texto pasado como argumento y lo reproduce
    print_(text)
    engine.say(text)
    if engine._inLoop: # Si el motor de voz está en un loop, lo detenemos para evitar errores
        engine.endLoop()
    engine.runAndWait()

#! Configuramos el detenimiento del asistente
def detener():
    if utils.deHumor(humor):
        utils.mixer_('Hasta_la_proxima', print_and_talk)
        time.sleep(3)
    else:
        print_and_talk('Deteniendo')
    global continuar
    continuar = False
    
#! Configuramos el conteo de instancias
def otro_intento():
    global intentos
    intentos += 1 

#! Iniciamos al asistente
def run():
    rec = listen() # Retorna el pedido de un usuario
    if rec == f'-{name}-error-': return None # No trata de ejecutar ningún pedido si hubo algún error
    posicion_inicio_name = rec.find(f'{name}') # Busca la posición donde inicia el nombre del asistente
    rec = rec[posicion_inicio_name :] # Recorta la grabación hasta el momento donde se dice el nombre
    print_(f'Dijiste: {rec}') # Te muestra lo que quedó de la grabación
    rec = rec[len(name)+1 :] # Recorta el nombre del asistente
    pedidos(rec)

def listen() -> str: # Se llama a sí misma hasta que detecte que se llamó al asistente por su nombre
    rec = reconocer_voz_y_pasarlo_a_texto()
    if name not in rec: rec = listen()
    return rec

def reconocer_voz_y_pasarlo_a_texto(fallos_conexion=0) -> str: # Definimos la función que reconocerá la voz y la convertirá en texto
    otro_intento()
    try:
        with sr.Microphone() as source: # Abrimos el micrófono como fuente de entrada de audio
            listener = sr.Recognizer()
            listener.adjust_for_ambient_noise(source, duration = 1) # Ajusta el nivel de ruido ambiental. Duration son los segundos que tarda en ajustar el ruido ambiental            
            print_(f'\n{intentos}) Escuchando...')
            voice = listener.listen(source, timeout=10) # Acá comienza a escuchar. Tiene una tolerancia máxima de 10 segundos de no escuchar nada. Sirve para tratar de evitar que la grabación se trabe por estar encendida mucho tiempo
            print_('Procesando...')
            return sr.Recognizer().recognize_google(voice, language = 'es', show_all=False).lower() # Acá se almacena lo que se grabó. Usa el servicio de Google para reconocer el habla en español argentino y lo convierte a minúsculas. Da error cuando no escucha nada             
    except sr.RequestError: # Si hay un fallo de conexión, intenta dos veces más arrancar el programa. Si a la número tres no vuelve la conexión, se cierra. (Hay 5 segundos entre cada intento)
        if fallos_conexion <= 1:
            print_('Internet no detectado. Reintentando...')
            time.sleep(5)
            return reconocer_voz_y_pasarlo_a_texto(fallos_conexion=fallos_conexion+1)
        else:
            print_and_talk('Fallo de conexión a internet')
            detener()
    except sr.UnknownValueError:
        print_('No se escuchó nada. Reintentando...')
    except sr.WaitTimeoutError:
        print_("Tiempo de espera agotado. Reintentando...")
    except Exception as e:
        print_and_talk(f'Error desconocido en el reconocimiento:\n{e}')
    return f'-{name}-error-'

#! Lógica y reconocimiento de los pedidos
def pedidos(rec: str) -> str:
    try:
        if len(rec) == 0: return print_and_talk('¿Qué pasa?') # Si el pedido incluía sólo el nombre
        if rec == 'gracias' or rec == 'muchas gracias': return print_and_talk('De nada')
        if rec == 'hola': 
            if utils.deHumor(humor): return utils.mixer_varias_opciones(['wazaa', 'hello_m_f'], print_and_talk)      
            return print_and_talk('hola')
        
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
    elif any(word == rec.split(' ')[-1] for word in ['cancela', 'cancelar', 'cancelas', 'cancelalo', 'olvidalo']): # Cancela el pedido que estás solicitando. La palabra "cancelar" debe decirse al final (o alguna variante similar)
        print_and_talk('Ok, cancelo el pedido')
    
    elif any(word == rec.split(' ')[-1] for word in ['minuto', 'minutos']) and (rec.split(' ')[-3] == 'en'): # Programa la ejecución de otro pedido para dentro de n minutos. "minutos" debe decirse al final, y "n" debe ser un número natural
        rec_array = rec.split(' ')
        
        if rec_array[-2] == 'un': # Cambio 'un' por '1' en el pedido, ya que yo necesito que sea un número
            rec_array[-2] = '1'
            
        numero = rec_array[-2]
        if numero.isdigit(): # Me aseguro de que el usuario haya especificado un número de minutos. Si no fue así, ignora el pedido y vuelve a empezar
            rec = ' '.join(rec.split(' ')[:-3]) # Quito "en X minutos" y solicito un pedido para después
            threading.Timer(int(numero)*60, lambda: pedidos(rec)).start() # Ejecuta el pedido en la cantidad de minutos que hayamos especificado
            print_and_talk('Ok, lo recordaré')
    
    elif utils.buscar(rec): print_and_talk('Hecho')
        
    elif any(rec.startswith(word) for word in ['escribir ', 'escribis ', 'escribi ', 'escribes ', 'escribe ']):  # Escribe todo lo que le pediste
        pedido_escritura = utils.eliminar_frases_introductorias(rec, ['escribir', 'escribis', 'escribi', 'escribes', 'escribe'])
        pyautogui.typewrite(pedido_escritura)
        print_and_talk('Hecho')
        
    elif any(rec.startswith(word) for word in ['repeti ', 'repite ', 'repetis ', 'repetir ', 'repitas ']):  # Repite todo lo que le pediste
        pedido_repetir = utils.eliminar_frases_introductorias(rec, ['repeti', 'repite', 'deci', 'repetis', 'repetir', 'repitas', 'decime'])
        print_and_talk(pedido_repetir)
    
    else: return False
    return True

def pedidoGenerico(rec: str) -> bool:
    global humor
    if False: pass
    elif any(word in rec for word in ['estas ahi', 'estas por ahi', 'seguis ahi', 'me estas escuchando']):
        if utils.deHumor(humor): utils.mixer_varias_opciones(['No_lo_se_tu_dime'], print_and_talk)
        else: print_and_talk('Estoy aquí')
    
    elif ' hora' in rec or rec.startswith('hora'): # Hora actual
        hora = datetime.now().strftime('%H:%M %p')
        print_and_talk(f'Son las {hora}')
        
    elif 'fecha' in rec or 'dia es hoy' in rec:
        fecha = datetime.now().strftime('%d/%m/%Y') # Fecha actual
        print_and_talk(f'Hoy es {fecha}')
    
    elif "atajo " in rec and len(rec.split())-1 >= rec.split().index('atajo')+1:
        utils.atajos(rec, print_and_talk)
    
    elif any(word in rec for word in ['abri', 'abras', 'abre', 'ir a']): utils.abrir(rec, print_and_talk, humor) # Abre archivos que estén en la biblioteca "direccion"
    
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
        time.sleep(0.1)
        pyautogui.press('n')
        print_and_talk('Hecho')
        
    elif 'volumen' in rec and '%' in rec: utils.volumen_al(rec, print_and_talk) # Cambia el volumen al X%
    
    elif 'chiste' in rec: print_and_talk(pyjokes.get_joke('es', category='all'))    
    
    elif any(word in rec for word in ['basta', 'apaga', 'apagues']): detener() # Apaga al asistente
    
    elif any(word in rec for word in ['como te llamas', 'cual es tu nombre']):
        if utils.deHumor(humor): utils.mixer_varias_opciones(['Excel_preg', 'Marad_ee', 'No_lo_se_tu_dime', 'muy_buena_preg', 'info_vale_millones', 'Uvuewewe'], print_and_talk)  
        else: print_and_talk(f'Me llamo {name}')    
    
    elif "tecla " in rec and len(rec.split())-1 >= rec.split().index('tecla')+1: # Si dice la palabra "tecla" en cualquier momento excepto en la palabra final, presiona la tecla pedida
        utils.apretar_tecla(rec, print_and_talk)    
    
    elif any(word in rec for word in ['captura de pantalla', 'estoy viendo', 'capturar pantalla', 'capturar pantalla', 'captura la pantalla', 'screenshot', 'capturame la pantalla']): # Saca una captura de pantalla
        screenshot = pyautogui.screenshot()
        now = f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'.replace(' ', '_').replace(':', '_')
        screenshot.save(f'capturas_de_pantalla/{now}_screenshot.png')
        print_and_talk('Captura guardada')
        
    elif 'cronometro' in rec and (any(word in rec for word in ['inicia', 'comenza', 'comienza']) or any(word in rec for word in ['para', 'deten'])):
        global cronometro
        cronometro = utils.cronometro(rec, cronometro, print_and_talk, humor)
        
    elif 'alarma' in rec: utils.mixer_(rec, print_and_talk)
    
    elif any(word in rec for word in ['humor actual', 'nivel de humor']) and ' al' not in rec: print_and_talk(f'Nivel de humor al {humor}%. Si querés modificarlo consulta las notas de ayudaS')        
        
    elif 'humor' in rec and '%' in rec:
        humor_nuevo = utils.obtener_numero(rec)
        if humor_nuevo == 100:
            frases = ['Formateo programado para las 22 horas', 'Autodestrucción en t menos 10 segundos', 'Humor al 100%']
            print_and_talk(random.choice(frases))
            humor = humor_nuevo
        elif humor_nuevo >= 0 and humor_nuevo < 100:
            print_and_talk(f'Humor al {humor_nuevo}%')
            humor = humor_nuevo
        else:
            print_and_talk('El nivel de humor se pide en términos porcentuales del 0 al 100')
            if utils.deHumor(humor): utils.mixer_varias_opciones(['Ah_re_bolu', 'Estup', 'Imbec'], print_and_talk)
            
    elif any(word in rec for word in ['ayuda', 'no entiendo', 'cosas puedes hacer', 'cosas podes hacer']):
        webbrowser.open(f'{direcciones_.direcciones["ayuda"]["url"]}')
        print_and_talk('Proporcionando ayuda')
        if utils.deHumor(humor): utils.mixer_varias_opciones(['buen_servicio'], print_and_talk)
        
    elif 'ver codigo fuente' in rec:
        webbrowser.open(f'{direcciones_.direcciones["codigofuente"]["url"]}')
        print_and_talk('Abriendo código fuente')
        if utils.deHumor(humor): utils.mixer_varias_opciones(['buen_servicio', 'es_bellisimo'], print_and_talk)
    
    elif any(word in rec for word in ['actualizar asistente', 'actualizarte', 'actualizate', 'actualices']): #Para que el ".exe" del asistente se actualice
        if usuario == 'Ricardo': # Si alguien más aparte de mí accede a este if no hay problema, pero con esto trato de reducir esa posibilidad (me llamo Alejandro pero mi computadora tiene este nombre de usuario)
            nombreAsistente = 'Asistente_virtual'
            print_and_talk('Actualizando asistente')
            os.chdir(f'{os.getcwd()}')
            os.system(f'pyinstaller --windowed --name "{nombreAsistente}" --add-binary "complementos/audio/*.mp3;complementos/audio" --add-data "complementos;complementos" --add-data "scripts;scripts" --icon=complementos/icon.ico --add-data "asistente_virtual.py;." GUI.py') # --onefile
            os.remove(f'{os.getcwd()}/{nombreAsistente}.spec')
            shutil.rmtree(f'{os.getcwd()}/build')
    else: return False
    return True

#! Ciclo para hacer que el asistente no termine nunca a menos que se lo pidamos específicamente
def iniciar(): # Nos aseguramos de que el asistente no deje de estar activo una vez que lo iniciamos
    global continuar
    continuar = True
    print_('Encendido')
    
    while continuar:
        run()

    engine.stop()
    print_('Detenido')

if __name__ == '__main__': # Si este archivo de python se ejecuta acá (es decir, si no lo estamos ejecutando desde otro script), entonces iniciamos el asistente
    iniciar()
