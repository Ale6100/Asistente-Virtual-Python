import speech_recognition as sr #Para que reconozca la voz
import pyttsx3                  #Para que el programa hable
import wikipedia                #Importa los datos de wikipedia
import pyautogui
from googletrans import Translator 
import pyjokes                  #Para contar chistes
from pygame import mixer
from datetime import datetime   #Importa la hora
import webbrowser               #Acceso a páginas web          
import time
from bs4 import BeautifulSoup
import requests                 #Va a una página web a buscar información en formato html
import random
import subprocess as sub

'''
Todos los pedidos deben iniciar con el nombre del asistente (actualmente se llama "Okey")

Algunas palabras clave: (la mayoría tiene alguna variante. Por ejemplo en vez de decir "abre" se puede decir "abrís")
    "cancela"                      Ejemplo: "Okey, abre whatsapp, no mejor no, cencela"      (cancela el pedido siempre y cuando la palabra "cancela" esté al final)
    "en n minutos"                 Ejemplo: "Okey, videos de gatos en YouTube en 2 minutos"  (elimina "Okey, ... en n minutos") y programa la ejecución de otro pedido para dentro de n minutos (n debe ser un numero). Sólo se puede programar un pedido a la vez
    "en YouTube"                   Ejemplo: "Okey, videos de gatos en YouTube"               (elimina "Okey, ... en YouTube" de la búsqueda en YouTube) 
    "buscador"                     Ejemplo: "Okey, buscador Netflix"       .                 (elimina "Okey, buscador" del pedido). Busca en el buscador de windows
    "busca"                        Ejemplo: "Okey, busca: definción de oso"                  (elimina "Okey, busca" de la búsqueda)
    "decime la definición de"      Ejemplo: "Okey, decime la definición de Argentina"        (elimina "Okey, decime la definición de" de la búsqueda). Usa Wikipedia
    "ubicación"                    Ejemplo: "Okey, ubicación de Tres Arroyos y San martín"   (elimina "Okey, ubicación de" de la búsqueda)
    "traduce"                      Ejemplo: "Okey, traduce perro"                            (elimina "Okey, traduce" de la traducción). Traduce del español al inglés
    "escribir"                     Ejemplo: "Okey, escribir"                                 (elimina "Okey, escribir" del pedido)
    "tecla"                        Ejemplo: "Okey, tecla p"                                  (elimina "Okey, tecla" del pedido)
    "repetí"                       Ejemplo: "Okey, repetí: hola cómo estás"                  (elimina "Okey, repetí" del pedido)
    "que pensas de"                Ejemplo: "Okey, qué pensás de Alexa?"                     
    "estás ahí"                    Ejemplo: "Okey, ¿estás ahí?"
    "hora"                         Ejemplo: "Okey, qué hora es?"
    "fecha"                        Ejemplo: "Okey, decime la fecha"
    "gracias"                      Ejemplo: "Okey, muchas gracias"
    "atajo n"                      Ejemplo: "Okey, atajo n"                                  (donde n es un número del 1 al 9) Llamo "atajo" a los iconos que estan en la barra de tareas al lado del botón de windows                                          
-   "abre"                         Ejemplo: "Okey, abre WhatsApp"                            (sólo funciona en programas preseleccionados)              
-   "reproducir canciones"         Ejemplo: "Okey, reproducir canciones"                                                                                               #CORREGIR ERROR
    "cerrar"                       Ejemplo: "Okey, cerrar página"
    "silenciar"                    Ejemplo: "Okey, silenciar"                                
    "minimiza todo"                Ejemplo: "Okey, minimizá todo"                            
    "minimiza"                     Ejemplo: "Okey, minimizá la ventana"
    "dolar"                        Ejemplo: "Okey, dolar hoy"
    "clima"                        Ejemplo: "Okey, decime el clima"                                                                                                     
    "covid"                        Ejemplo: "Okey, situación actual del covid"
    "volumen ... X%"               Ejemplo: "Okey, volumen al X%"                            (sólo pone valores pares de volumen)                           
    "borra todo"                   Ejemplo: "Okey, borrá todo"                               (borra 100 carácteres)
    "hola"                         Ejemplo: "Okey, hola"
    "chiste"                       Ejemplo: "Okey, decime un chiste"
    "basta"                        Ejemplo: "Okey, basta"                                    (cierra el .exe o python)
-   "actualizar asistente virtual" Ejemplo: "Okey, actualizar asistente virtual"             (actualiza el .exe del asistente)              
    "cómo te llamás?"              Ejemplo: "Okey, ¿cómo te llamás?"                         
    "captura de pantalla"          Ejemplo: "Okey, sacá una captura de pantalla"             (guarda la captura en imágenes/capturas de pantalla)
    "qué podes hacer"              Ejemplo: "Okey, que podés hacer?"
    "nota" (agregá, leé o borrá)   Ejemplo: "Okey, agregar nota"                             (Escribe, lee, o borra notas en un block de notas. Se puede abrir este block diciendo "Okey, abrir notas")
    "cronómetro"                   Ejemolo: "Okey, inicia el cronómetro"
    "alarma... n minutos"          Ejemplo: "Okey, activá la alarma en 2 minutos"            (Programa la alarma para dentro de 2 minutos)
    "nivel de humor"               Ejemplo: "Okey, cuál es tu nivel de humor"
    "humor... X%"                  Ejemplo: "Okey, humor al 20%"                             (ajusta el nivel de humor del asistente, por defecto es 5%)
    "ayuda"                        Ejemplo: "Okey, necesito ayuda"                           (abre un block de notas con este texto)
-   "rutina"                       Ejemplo: "Okey, rutina estudiar"
    "cambia tu nombre"             Ejemplo: "Okey, cambia tu nombre"                         (te dice que no puede xd)

Aclaración: las palabras clave que inician con guión sólo funcionan en mi computadora

Los siguientes códigos pueden hacer que el programa no funcionar bien y se reinicie:
    "buscador", "...en WhatsApp" y "actualizar asistente virtual" (la máquina puede ser más lenta de lo previsto)
    "decime la definición de"                                     (la definición buscada puede no existir o esté mal detectada)
    "abre" y "reproducir canciones"                               (algunos archivos solo están en mi computadora)
    "dolar / clima / covid"                                       (la página donde se extrae la información pudo haber cambiado)
'''
usuario = 'Ricardo'                         #Nombre de usuario en la PC actual
name = 'okay'                               #Le definimos un nombre al asistente, o simplemente una palabra clave que hace que se active

engine = pyttsx3.init()
voices = engine.getProperty('voices')       #Tomamos a la variable "engine" y obtenems las propiedades de "voices". Hacemos esto para obtener todas las voces del reproductor

for i in range(len(voices)):                #Recorre la lista de voces instaladas en windows hasta encontrar alguna en español. Luego la usa
    if 'ES' in voices[i].id: 
        engine.setProperty('voice', voices[i].id)
        break
    else:
        engine.setProperty('voice', voices[0].id) #Si no encuentra ninguna, usa la primer voz de la lista

engine.setProperty('rate', 160)             #velocidad del asistente
############### Código antiguo, pero lo dejo por si sirve
#engine.setProperty('voice', voices[0].id)  #Cambiar el número para poner otra voz
#for i in voices:                           #Para ver las voces disponibles
#    print(i)
###############
k                 = [0]   #A esta lista se le agrega un elemento cada vez que comenzamos a grabar
mixer_stop_       = [999] #Coloco un número muy grande apropósito para asegurarme que no sea superado por len(k)
cronometro_       = []
tiempo_del_pedido = [1e10] #Originalmente (antes de que se programe un pedido) este número lo defino así pero cambia cuando programo un pedido. Coloco este número grande sabiendo que time.time() arroja resultados más chicos que 1e10
guarda_tarea      = []    #Acá va a estar el pedido programado. Originalmente no hay ninguno.
fin_tiempo_pedido = [0]   #Acá van a estar los minutos que va tardar en ejecutarse cada pedido programado. 
nivel_humor       = [5]   #Humor inicial, por defecto es 5

def reconocer_voz_y_pasarlo_a_texto(i = 0):
    try:
        with sr.Microphone() as source:                                    #Le pedimos que tome al micrófono como fuente para escuchar
            listener = sr.Recognizer()                                     #Esto hace que se reconozca la voz    
            listener.adjust_for_ambient_noise(source, duration = 1)        #Reduce el ruido ambiental. duration son los segundos que tarda en ajustar el ruido ambiental            
            ########## Chequeos necesarios para que algunos pedidos funcionen bien                                   
            k.append(0)                                                    #Se suma un elemento cada vez que comienza a grabar
            if (len(k) - mixer_stop_[-1]) > 20: mixer.music.stop()         #Apaga todos los archivos de audio después de 20 grabaciones (sólo influye en los archivos abiertos por el asistente)
            if chequear_temporizador(fin_tiempo_pedido[-1]) == True: return None #Chequea si llegó el momento de acatar el pedido que le dijimos que haga en X minutos (con las palabras clave '... en X minutos'). Si el pedido programado se ejecutó, entonces la función devuelve None                   
            ##########
            print(f'\n{len(k)-1}) Escuchando...')                          #Imprime esto para que sepamos que está escuchando (aunque realmente todavía no está escuchando)
            voice = listener.listen(source, 10)  #Acá comienza a escuchar. Tiene una tolerancia de 10 segundos de no escuchar nada, creo. Sirve para tratar de evitar que la grabación se trabe por estar encendida tanto tiempo
            print('Procesando...')
            rec = listener.recognize_google(voice, language = 'es-AR').lower() #Acá se almacena lo que se grabó. Le pido que reconozca mi voz con google en el idioma español argentino. El lower cambia mayúsculas por minúsculas. Da error cuando Python no escucha nada             
    except sr.RequestError:
        if i < 3:                                                          #Si hay un fallo de conexión, intenta tres veces arrancar el programa. Si a la número tres no vuelve la conexión, se cierra. (Hay 10 segundos entre cada intento)
            print('Fallo de conexión, reintentando...')
            time.sleep(10)
            rec = reconocer_voz_y_pasarlo_a_texto(i = i + 1)
        else: print_and_talk('Fallo de conexión a internet. Cerrando')
    except:
        print('No se escuchó nada. Reintentando..')
        rec = reconocer_voz_y_pasarlo_a_texto()
    return rec

def listen():
    rec = reconocer_voz_y_pasarlo_a_texto()
    if rec == None: return None                             #Si rec es None (es decir, si recién se activó un pedido programado), entonces listen también devuelve None
    else:  
        if name not in rec: rec = listen()                  #Si el nombre del asistente no está en rec, vuelve a iniciar la definición   
        return rec
    
def run():
    rec = listen()                                          #Definimos como "rec" a lo que nos retorne la función "listen()"
    if rec == None: return None                             #Si recién se activó un pedido programado, entonces devuelve None y vuelve al while original
    else:
        posicion_name = rec.find(name)                      #Busca la posición donde inicia el nombre del asistente
        rec = rec[posicion_name : len(rec)]                 #Recorta la grabación hasta el momento donde se dice el nombre
        print(f'Dijiste: {rec}')                            #Te muestra lo que quedó de la grabación
        rec = rec.replace(name + ' ', '').replace(name, '') #Pedimos que reemplace el nombre del asistente por un espacio vacío       
        pedidos(rec)

def pedidos(rec):
    try:
        reintentos = 2                            #Esto indica la cantidad de reintentos que se harán en algunos códigos específicos
        rec = rec.replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u') #Quita las tildes
        direccion = {'zoom' : 'C:/Users/' + usuario + '/AppData/Roaming/Zoom/bin/Zoom.exe', 'whatsapp' : 'C:/Users/' + usuario + '/AppData/Local/WhatsApp/WhatsApp.exe', 'steam' : 'C:/Program Files (x86)/Steam/Steam.exe', 'canciones' : 'C:/Users/' + usuario + '/Music/Canciones/canciones.xspf', 'estudio' : 'C:/Users/' + usuario + '/Desktop/Estudio', 'word' : 'C:/Program Files/Microsoft Office/root/Office16/WINWORD.exe', 'excel' : 'C:/Program Files/Microsoft Office/root/Office16/EXCEL.exe', 'facebook' : 'https://www.facebook.com/', 'youtube' : 'https://www.youtube.com/', 'twitch' : 'https://www.twitch.tv/', 'codigos' : 'https://colab.research.google.com/drive/1e9pqVIkt6J1LK7uxsK_IE-i5rx4NJiME?usp=sharing', 'asistente' : 'https://colab.research.google.com/drive/1mSVIXH-x9u0ABlPbS6XIHsLdIpm3_k02', 'google' : 'https://www.google.com.ar/', 'simulador de plazo fijo' : 'Archivos_complementarios/Simulador_de_plazo_fijo.exe', 'notas' : 'Archivos_complementarios/Notas asistente virtual.txt', 'computadora' : 'https://computacion.mercadolibre.com.ar/pc-escritorio/pc/intel-core-i7/mas-de-481-gb/mas-de-16-GB-ram/nuevo/cpu_NoIndex_True#applied_filter_id%3DHDD_SIZE%26applied_filter_name%3DDisco+duro%26applied_filter_order%3D5%26applied_value_id%3D481-*%26applied_value_name%3D481-*%26applied_value_order%3D5%26applied_value_results%3DUNKNOWN_RESULTS%26is_custom%3Dtrue'}
        if 'cancela' == rec[-7:] or 'cancelar' == rec[-8:]: #Cancela el pedido actual siempre y cuando digamos "cancelar" al final
            print_and_talk('Ok, cancelo el pedido')
            run()
        
        elif 'minutos' == rec[-7:] or 'minuto' == rec[-6:]: #programa un pedido para dentro de X minutos
            rec = rec.replace(' minutos', '').replace(' minuto', '').replace('un', '1') #Quita la palabra "minutos". Por lo tanto, "abre whatsapp en 2 minutos" queda en "abre whatsapp en 2"
            rec_split = rec.split()               #Separa la cadena de texto en palabras, convirtiendola en una lista
            tiempo_limite = rec_split[-1]         #Copia la última palabra (que debería ser un número)
            rec = ' '.join(rec_split[:-2])        #Toma todas las palabras menos las dos últimas y las junta de nuevo en una cadena de texto (en nuestro ejemplo, sería 'abre whatsapp')
            pedido_programado(rec, tiempo_limite) #En "tiempo_limite" minutos, se ejecutará la acción "rec"
            
        elif 'en youtube' == rec[-10:]:
            pedido_youtube = rec.replace('en youtube', '')
            webbrowser.open('https://www.youtube.com/results?search_query=' + pedido_youtube)
            print_and_talk('Hecho')
    
        elif 'buscador' == rec[:8] or 'busca door' == rec[:8]:        #Busca el pedido en el buscador de windows
            rec = rec.replace('buscador', '').replace('busca door', '')
            buscador(rec)
    
        elif 'buscar' == rec[:6] or 'buscas' == rec[:6] or 'me buscas' == rec[:9] or 'busca' == rec[:5]:
            pedido_buscador = rec.replace('buscar', '').replace('me buscas', '').replace('buscas', '').replace('busca', '')
            webbrowser.open('https://www.google.com.ar/search?q=' + pedido_buscador) #Busca en google lo que esté dentro de "rec"
            print_and_talk('Estos son los resultados')            
    
        elif 'decime la definicion de' == rec[:23] or 'definicion de' == rec[:13] or 'define' == rec[:6] or 'definicion' == rec[:10]:                            
            definicion_wikipedia(rec)
        
        elif 'decime la ubicacion del' == rec[:23] or 'dame la ubicacion de la' == rec[:23]  or 'dame la ubicacion del' == rec[:21] or 'decime la ubicacion de la' == rec[:25] or 'ubicacion del' == rec[:13] or 'donde esta el' == rec[:13] or 'donde esta la' == rec[:13]  or 'ubicacion de' == rec[:12] or 'donde esta' == rec[:10]:
            pedido_maps = rec.replace('decime la ubicacion del', '').replace('dame la ubicacion del', '').replace('decime la ubicacion de la', '').replace('dame la ubicacion de la', '').replace('ubicacion del', '').replace('ubicacion de', '').replace('donde esta el', '').replace('donde esta la', '').replace('donde esta', '')
            webbrowser.open('https://www.google.com.ar/maps/search/' + pedido_maps) #Busca en google maps lo que esté dentro de "rec"
            print_and_talk('Hecho')                        
       
        elif 'traduce' == rec[:7] or 'traducime' == rec[:9] or 'me traducis' == rec[:11] or 'traducis' == rec[:8] or 'traducir' == rec[:8] or 'traduccion de' == rec[:13] or 'traduccion' == rec[:10]:
            pedido_traductor = rec.replace('traduceme', '').replace('traduce', '').replace('traducirme', '').replace('traducime', '').replace('me traducis', '').replace('traducis', '').replace('traducir', '').replace('traduccion de', '').replace('traduccion', '')
            traduccion = Translator().translate(pedido_traductor, src = 'es', dest = 'en' ).text #Traduce del español al inglés
            print_and_talk(pedido_traductor + ' en inglés se dice ' + traduccion)
    
        elif 'escrib' == rec[:6] and 'nota' not in rec:
            pedido_escritura = rec.replace('escribir ', '').replace('escribis ', '').replace('escribi ', '').replace('escribes ', '').replace('escribe ', '')
            pyautogui.typewrite(pedido_escritura)         #Escribe todo lo que le pediste (hay que decirlo rápido y claro)
            print_and_talk('Hecho')  
        
        elif 'tecla' == rec[:5] and 'teclado' != rec[:7]: #Aprieta la tecla pedida
            rec = rec.replace('tecla ', '')
            apretar_tecla(rec)
    
        elif 'repeti' == rec[:6] or 'repite' == rec[:6] or 'deci' == rec[:4]:
            rec = rec.replace('repeti ', '').replace('repite ', '')
            print_and_talk(rec)                           #Repite todo lo que le dijiste (hay que decirlo rápido y claro)
            
        elif 'que pensas de' == rec[:13] or 'que piensas de' == rec[:14]:
            if ('alexa' in rec or 'siri' in rec or 'google' in rec or 'asistente' in rec):
                print_and_talk('Yo soy mejor')
            else: print_and_talk('No lo conozco, pero seguro soy mejor')
        
        elif pedidos_genericos(rec, direccion, reintentos) == True: None #Si se recibe un "pedido genérico" (cualquier pedido que esté dentro de esa función), esto devuelve None
            
        elif len(rec) == 0: print_and_talk('Que pasa')    #Si detecta sólo el nombre, dice "qué pasa"
            
        else: print_and_talk('No te entendí')             #Si detecta algo pero no lo entiende o se pide algo que no está programado, dice "No te entendí"
    except: print_and_talk('Error desconocido')           #Si hay un error no previsto, dice "Error desconocido" y vuelve al while

#############################################################################

def pedidos_genericos(rec, direccion, reintentos):        #Los "pedidos genéricos" son aquellos que son activados por una o varias palabras sin importar las otras cosas que digas. Se diferencian con los pedidos de arriba porque ya no deben ser pedidos exactos yendo directo al grano
    res = True
    if 'estas ahi' in rec or 'estas por ahi' in rec:
        if humor_activado() == True: mixer_('Ahre que no mori', volumen = 0.4)
        else: print_and_talk('Estoy aquí')
        
    elif 'hora' in rec:
        hora = datetime.now().strftime('%H:%M %p')  #Hora actual
        print_and_talk(f'Son las {hora}')
        
    elif 'fecha' in rec:
        fecha = datetime.now().strftime('%d/%m/%Y') #Fecha actual
        print_and_talk(f'Hoy es {fecha}') 
        
    elif 'gracias' in rec: print_and_talk('De nada')
    
    elif 'atajo' in rec: atajos(rec, reintentos)      #Abre atajos del 1 al 9

    elif 'abri' in rec or 'abras' in rec or 'abre' in rec: abrir(rec, direccion, reintentos) #Abre archivos que estén en la biblioteca "direccion"
                          
    elif 'reproducir las canciones' in rec or 'reproduce canciones' in rec or 'reproducir canciones' in rec or 'reproduci cancion' in rec or 'poner las canciones' in rec or 'pones canciones' in rec or 'pone las canciones' in rec or 'pon las canciones' in rec:
        webbrowser.open_new(direccion['canciones'])
        pyautogui.press('volumedown', 50), pyautogui.press('volumeup', 10)
        print_and_talk('Reproduciendo canciones')
        
    elif 'cerrar' in rec or 'cierra' in rec:                         
        pyautogui.hotkey('alt', 'F4')
        print_and_talk('Hecho') 

    elif 'mute' in rec or 'silenci' in rec:
        pyautogui.hotkey('volumemute')
        print_and_talk('Hecho')

    elif 'minimizar todo' in rec or 'minimizar toda' in rec or 'minimizar los' in rec or 'minimizar las' in rec or 'minimiza todo' in rec or 'minimiza toda' in rec or 'minimiza los' in rec or 'minimiza las' in rec or 'minimizame todo' in rec or 'minimizame toda' in rec or 'minimizame los' in rec or 'minimizame las' in rec:
        pyautogui.hotkey('win', 'd')
        print_and_talk('Hecho')

    elif 'minimizar' in rec or 'minimiza' in rec:
        pyautogui.hotkey('ALT', 'space', 'N')
        print_and_talk('Hecho')
    
    elif 'dolar' in rec or 'clima' in rec or 'temperatura' in rec or 'covid' in rec or 'coronavirus' in rec: beautifulsoup(rec)
            
    elif 'volumen' in rec: volumen_al(rec)          #Cambia el volumen al X%

    elif 'borrar todo' in rec or 'borra todo' in rec or 'borras todo' in rec: 
        pyautogui.press('backspace', 100)           #Borra 100 carácteres
        print_and_talk('Borrando 100 caracteres')
    
    elif 'hola' in rec:
        if humor_activado() == True: mixer_varias_opciones(['waza', 'hello m f']) 
        else: print_and_talk('Hola')

    elif 'chiste' in rec:
        chiste = pyjokes.get_joke('es')
        print_and_talk(chiste)

    elif 'basta' in rec or 'apagate' in rec: basta()                    #Agrega un elemento "True" a la lista "basta" y detiene la grabación

    elif 'actualizar asistente' in rec or 'actualizarte' in rec or 'actualizate' in rec or 'actualices' in rec: #Para que el ".exe" del asistente se actualice
        webbrowser.open_new('C:/Users/' + usuario + '/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Anaconda3 (64-bit)/Anaconda Prompt (anaconda3)'), print_and_talk('Actualizando asistente')
        pyautogui.typewrite('cd C:\\Users\\' + usuario + '\\Desktop\\Estudio\\Python\\Asistente_virtual'), time.sleep(1)
        pyautogui.hotkey('enter'), time.sleep(2)
        pyautogui.typewrite('pyinstaller --windowed --add-data "Archivos_complementarios;Archivos_complementarios" --icon=./z_robot.ico Asistente_virtual.py'), time.sleep(1)
        pyautogui.hotkey('enter'), basta() #--windowed: No se habre la consola cuando abrimos el .exe. --onefile: Crea el .exe y sus dependencias en un sólo archivo. --add-data "X;X": Guarda la carpeta X en una nueva carpeta X. --icon=./X.ico: Hace el .exe con el icono X.        
    
    elif 'como te llamas' in rec or 'cual es tu nombre' in rec:
        if humor_activado() == True: mixer_varias_opciones(['buena preg', 'excel preg', 'vale millones', 'ehh', 'tu dime', 'uvuewe'])  
        else: print_and_talk(f'Me llamo {name}')
        
    elif 'captura de pantalla' in rec or 'que estoy viendo' in rec:
        pyautogui.hotkey('win', 'printscreen')      #Saca una captura de pantalla y la guarda en "imágenes/capturas de pantalla"
        print_and_talk('Captura guardada')
    
    elif 'nota' in rec: nota(rec)
        
    elif 'cronometro' in rec: cronometro(rec)
    
    elif 'alarma' in rec: mixer_(rec)

    elif 'humor actual' in rec or 'nivel de humor' in rec: print_and_talk(f'Nivel de humor al {nivel_humor[-1]}%. Si querés modificarlo debés decir "humor al n%"')
    
    elif 'humor' in rec or 'amor' in rec: cambiar_humor(rec)
    
    elif 'ayuda' in rec or 'no entiendo' in rec or 'que puedes hacer' in rec or 'que cosas puedes hacer' in rec or 'que cosas podes hacer' in rec or 'que podes hacer' in rec:
        sub.Popen('Archivos_complementarios/Palabras clave.txt', shell = True)
        print_and_talk('Abriendo block de ayuda')
    
    elif 'rutina' in rec: rutinas(rec, reintentos)     
    
    elif 'cambia tu nombre' in rec or 'cambiar tu nombre' in rec: print_and_talk('No puedo cambiar mi nombre')
    
    else: res = False
    return res

###################################################################

######## DEFINICIONES QUE DEPENDERÁN DE OTRAS QUE ESTÁN MÁS ABAJO 
def print_and_talk(text): #Esta función hace que el reproductor lea el texto en el paréntesis, pero primero lo imprime                        
    print(text)
    engine.say(text)  
    engine.runAndWait()

def respuesta_positiva(rec, reintentos, j = 0): #Hice esto pero jamás lo usé
    rec = reconocer_voz_y_pasarlo_a_texto()
    if 'si' in rec: res = True
    elif 'no' in rec: res = False
    else:
        if j < reintentos:
            print_and_talk('Responde con sí o con no')
            rec = reconocer_voz_y_pasarlo_a_texto()
            respuesta_positiva(rec, reintentos, j = j + 1)
        else:
            print_and_talk('Error, tu respuesta debía contenter sí o no')
            if humor_activado() == True: mixer_varias_opciones(['Ah re bolu', 'Tonto 1', 'Tonto 2'])  
            res = None
    return res

def pedido_programado(rec, tiempo_limite):
    guarda_tarea.append(rec)                          #Guarda el pedido programado
    tiempo_del_pedido.append(time.time())             #Guarda el tiempo actual
    fin_tiempo_pedido.append(float(tiempo_limite)*60) #Guarda la cantidad de minutos que tienen que pasar para que el pedido se active
    print_and_talk('Ok, lo recordaré')
def chequear_temporizador(T):                         #T es la cantidad de minutos que tienen que pasar para que el pedido se active
    if (time.time() - tiempo_del_pedido[-1]) > T:     #Chequea si la diferencia de tiempo entre ahora y el momento en el que se hizo el pedido, es mayor a T (es decir, si ya se superó el tiempo T)
        rec = guarda_tarea[-1]                        #Si pasó el tiempo pedido, agarra el pedido programado y lo ejecuta en "ordenes"
        pedidos(rec)
        guarda_tarea.clear()                          #Reinicia las variables originales, para poder hacer un nuevo pedido de ser necesario
        tiempo_del_pedido.clear(), tiempo_del_pedido.append(1e10)
        fin_tiempo_pedido.clear(), fin_tiempo_pedido.append(0)        
        res = True
    else: res = False
    return res

def mixer_(rec, cantidad = 1, volumen = 0.5):        #Reproduce sonidos pedidos en formato mp3 que estén en "direccion_m"
    direccion_m = {'alarma' : "Alarma", 'hasta la proxima' : 'Hasta la proxima', 'no mori' : 'Ahre que no mori', 're bolu' : 'Ahre bolu', 'waza' : 'Wazaa', 'hello m f' : 'Hello m f', 'buena preg' : 'Es una muy buena pregunta', 'excel preg' : 'Esa es una excelente pregunta', 'vale millones' : 'Esta informacion vale millones', 'ehh' : 'MARADONA EEEE EEEHH', 'tu dime' : 'No lo sé tú dime', 'uvuewe' : 'Uvuewewe', 'Tonto 1' : 'Tonto 1', 'Tonto 2' : 'Tonto 2', 'casi' : 'Casi la cag'}
    try:     
        for i in direccion_m:
            if i in rec:
                mixer.init()
                mixer.music.load(f'Archivos_complementarios/{direccion_m[i]}.mp3')
                mixer.music.set_volume(volumen)
                mixer.music.play(cantidad)           #mixer.music.play(1) suena n veces
                mixer_stop_.append(len(k))
                break
    except: print_and_talk('Error, el archivo de sonido no está o no funciona')
def mixer_varias_opciones(opciones):
    mixer_(random.choice(opciones), volumen = 0.4)

def humor_activado():                                #Agarra un número al azar y evalúa si se activa un comentario "gracioso" en algunos pedidos xd
    res = False 
    if 100*random.random() < nivel_humor[-1]: res = True #random.random() es un número aleatorio entre 0 y 1
    return res
########

def buscador(rec):
    pyautogui.hotkey('win', 's'), time.sleep(2)
    pyautogui.typewrite(rec), print_and_talk(f'Abriendo {rec}')
    pyautogui.hotkey('enter')

def definicion_wikipedia(rec):
    try:              
        pedido_wikipedia = rec.replace('decime la definicion de', '').replace('definicion de', '').replace('define', '').replace('definicion', '')
        wikipedia.set_lang('es')                      #wikipedia en español
        info = wikipedia.summary(pedido_wikipedia, 1) #Busca lo que esté dentro de "rec" (el 1 hace referencia al párrafo 1)
        print_and_talk(info)
    except: print_and_talk('La definición pedida no existe o no se entendió el pedido')

def atajos(rec, reintentos, j = 0):
    numeros, palabras, contador = '123456789', ['uno', 'dos', 'tres', 'cuatro', 'cinco', 'seis', 'siete', 'ocho', 'nueve'], 0
    for i in range(9):
        if numeros[i] in rec or palabras[i] in rec:
            print_and_talk(f'Abriendo atajo {numeros[i]}')
            pyautogui.hotkey('win', numeros[i])
            if (humor_activado() == True) and (j == reintentos): mixer_('casi', volumen = 0.9)
            break
        contador = contador + 1    
    if contador == 9:
        if j < reintentos:
            print_and_talk('No te entendí, ¿cuál atajo querés?')
            rec = reconocer_voz_y_pasarlo_a_texto()
            atajos(rec, reintentos, j = j + 1)
        else:
            print_and_talk('Los atajos son números del 1 al 9')
            if humor_activado() == True: mixer_varias_opciones(['Ah re bolu', 'Tonto 1', 'Tonto 2'])  
        
def abrir(rec, direccion, reintentos, j = 0):
    contador = 0
    for i in direccion:        
        if i in rec:
            if (i == 'notas') or (i == 'simulador de plazo fijo'):
                sub.Popen(direccion[i], shell = True)
            else:
                webbrowser.open_new(direccion[i])
            print_and_talk(f'Abriendo {i}')
            if (humor_activado() == True) and (j == reintentos): mixer_('casi', volumen = 0.9)
            break
        contador = contador + 1
    if ('basta' in rec or 'nada' in rec): print_and_talk('Ok, no hago nada')
    elif contador == len(direccion):
        if j < reintentos:
            print_and_talk('No te entendí, ¿qué querés abrir?')
            rec = reconocer_voz_y_pasarlo_a_texto()
            abrir(rec, direccion, reintentos, j = j + 1)
        else: print_and_talk('No encontré el programa')

def beautifulsoup(rec):
    try:    
        if 'dolar' in rec:
            page = requests.get('https://www.dolarhoy.com/')
            soup = BeautifulSoup(page.content, 'html.parser')
            content_compra, content_venta = soup.find_all('div', class_ = 'compra'), soup.find_all('div', class_ = 'venta')
            precio_compra, precio_venta = content_compra[2].find_all('div')[1].text, content_venta[2].find_all('div')[1].text
            print_and_talk('El dólar oficial es de ' + precio_compra + ' para la compra y ' + precio_venta + ' para la venta')
            
        elif ('clima' in rec or 'temperatura' in rec):
            page = requests.get('https://weather.com/es-AR/tiempo/hoy/l/-34.61,-58.45?par=google')
            soup = BeautifulSoup(page.content, 'html.parser')
            temperatura = soup.find_all('span', class_ = 'CurrentConditions--tempValue--3a50n')[0].text
            print_and_talk('La temperatura actual es de ' + temperatura)
                
        elif ('covid' in rec or 'coronavirus' in rec):
            page = requests.get('https://www.worldometers.info/coronavirus/country/argentina/')
            soup = BeautifulSoup(page.content, 'html.parser')
            content_situacion = soup.find_all('div', class_ = 'maincounter-number')
            infectados, muertos, recuperados = content_situacion[0].text, content_situacion[1].text, content_situacion[2].text
            print_and_talk('Actualmente en Argentina hay ' + infectados.replace('\n', '').replace(',', '.').replace(' ', '') + ' casos, ' + muertos.replace('\n', '').replace(',', '.').replace(' ', '') + ' fallecidos, y ' + recuperados.replace('\n', '').replace(',', '.').replace(' ', '') + ' recuperados.')
    except: print_and_talk('Información no encontrada')

def volumen_al(rec):
    rec = rec.replace('%', '')
    for i in range(100, -1, -1):
        if str(i) in rec:
            pyautogui.press('volumedown', 50), pyautogui.press('volumeup', round(i/2))
            print_and_talk(f'Volumen al {2*round(i/2)} por ciento') #Lo hago así sabiendo que el resultado siempre será par, ya que los botones mueven el valor de volumen de a pares
            break

def apretar_tecla(rec):
    teclas, contador = {'arriba' : "up", 'abajo' : "down", 'derecha' : 'right', 'izquierda' : 'left', 'espacio' : 'space', 'borrar' : 'backspace', 'enter' : 'enter', 'tab' : 'tab'}, 0
    for i in teclas:
        if rec == i:
            pyautogui.press(teclas[rec])
            print_and_talk('Hecho')
            break
        contador = contador + 1
    if contador == len(teclas):
        pyautogui.press(rec)
        print_and_talk('Hecho')
        
def basta():
    try:
        if humor_activado() == True:
            mixer_('hasta la proxima', volumen = 0.2)
            time.sleep(3)
            try: mixer.music.stop()
            except: None
        else: print_and_talk('Cerrando')
    except: print_and_talk('Cerrando')
    finally: basta_.append(True)
        
def nota(rec):
    try:
        if ('agreg' in rec or 'escrib' in rec):
            print_and_talk('¿Qué querés que anote?')
            rec = reconocer_voz_y_pasarlo_a_texto()
            notas = open('Archivos_complementarios/Notas asistente virtual.txt', 'a')
            notas.write(f'\n\n{rec}') #Agrega una nota
            notas.close()
            print_and_talk('Nota escrita')
        elif ('lee' in rec or 'lea' in rec or 'peleas' in rec or 'ver' in rec):
            notas = open('Archivos_complementarios/Notas asistente virtual.txt', 'r')
            texto = notas.read()    #Lee las notas
            notas.close()
            if len(texto) == 0: print_and_talk('No hay notas escritas')
            else: print_and_talk(texto)
        elif ('borra' in rec or 'elimina' in rec or 'borres' in rec):
            notas = open('Archivos_complementarios/Notas asistente virtual.txt', 'w')
            notas.write('')         #Borra todas las notas
            notas.close()
            print_and_talk('Notas borradas')
        elif ('basta' in rec or 'nada' in rec): print_and_talk('Ok, no hago nada')
        else:
            print_and_talk('¿Querés que agregue una nota, que lea o que borre?') #Si no te entiende o no le respondés, te pregunta esto (decir "basta" si se repite en bucle)
            rec = reconocer_voz_y_pasarlo_a_texto()
            nota(rec)
    except: print_and_talk('Archivo de notas roto')

def cronometro(rec):
    try:   
        if ('inicia' in rec or 'comenza' in rec or 'comienza' in rec):
            print_and_talk('Iniciando cronómetro')
            cronometro_.append(time.time())        #Anota el tiempo actual
        elif ('detene' in rec or 'para' in rec): #Cuando se detiene averigua cuanto tiempo pasó
            tiempo_pasado = round(time.time() - cronometro_[-1], 2)
            print_and_talk(f'Pasaron {tiempo_pasado} segundos, {round(tiempo_pasado/60, 2)} minutos') 
            cronometro_.clear()
        elif 'nada' in rec or 'basta' in rec: basta()
        else:
            print_and_talk('Querés iniciar o detener el cronómetro?')
            rec = reconocer_voz_y_pasarlo_a_texto()
            cronometro(rec)
    except:
        print_and_talk('Error, primero tenés que iniciar el cronómetro') #Da error si le pedis que se detenga sin antes haberle pedido que se inicie
        if humor_activado() == True: mixer_varias_opciones(['Ah re bolu', 'Tonto 1', 'Tonto 2'])           

def cambiar_humor(rec):
    rec, contador = rec.replace('%', ''), 0
    for i in range(100, -1, -1):
        if str(i) in rec:
            if i == 100:
                frases = ['Formateo programado para las 22 horas', 'Autodestrucción en t menos 10 segundos', 'Humor al 100%']
                print_and_talk(random.choice(frases))
            else:
                print_and_talk(f'Humor al {i}%')
            nivel_humor.append(i)
            break
        contador = contador + 1
    if contador == 101: print_and_talk('El nivel de humor se pide en términos porcentuales, del 0 al 100')

def rutinas(rec, reintentos, j = 0):
    if 'estudiar' in rec or 'estudio' in rec:
        webbrowser.open_new('C:/Users/' + usuario + '/Desktop/Estudio/Materias/Matemática 1/Resumen de Matematica1.docx')
        webbrowser.open_new('C:/Users/' + usuario + '/Desktop/Estudio/Materias/Matemática 1/Demostraciones de Matemática 1.docx')
        webbrowser.open_new('C:/Users/' + usuario + '/Desktop/Estudio/Materias/Matemática 1/Apuntes de la teórica (Prof. Páblo De Nápoli) - Verano 2017.pdf')
        webbrowser.open_new('C:/Users/' + usuario + '/Desktop/Estudio/Materias/Matemática 1/Teoremas.pdf')
        webbrowser.open_new('C:/Users/' + usuario + '/Desktop/Estudio/Materias/Matemática 1/Apuntes para el Final - Federico Yulita.pdf')
        webbrowser.open_new('C:/Users/' + usuario + '/Desktop/Estudio/Materias/Matemática 1/mas en palabras.pdf')
        webbrowser.open_new('C:/Users/' + usuario + '/Desktop/Estudio/Materias/Matemática 1/Teoremas Analisis Lartu.net.pdf')
        webbrowser.open_new('C:/Users/' + usuario + '/Desktop/Estudio/Materias/Matemática 1/Resumen de Matematica 1 - Julian Sackmann.pdf')
        webbrowser.open_new('C:/Users/' + usuario + '/Desktop/Estudio/Materias/Matemática 1/CalculoyAnalisis_Larotonda.pdf')
        pyautogui.press('volumedown', 50), pyautogui.press('volumeup', 10)
        nivel_humor.append(100), print_and_talk('Hecho')
    elif 'nada' in rec or 'basta' in rec:
        print_and_talk('Ok, no hago nada')
    elif j < reintentos:
        print_and_talk('No te entendí, ¿qué rutina querés iniciar?')
        rec = reconocer_voz_y_pasarlo_a_texto()
        rutinas(rec, reintentos, j = j + 1)
    else:
        print_and_talk('No encontré la rutina')
    
############################################################################# 

basta_ = []
def iniciar_asistente(): #Nos aseguramos de que el asistente no deje de estar activo una vez que lo iniciamos, siempre y cuando la lista "basta_" esté vacía   
    while len(basta_) == 0: run() 

if __name__ == '__main__': #Si este archivo de python se ejecuta acá (es decir, si no lo estamos ejecutando desde otro script), entonces iniciamos el asistente
    iniciar_asistente()
