import configparser
import os
import threading
import time
from datetime import datetime
import random
import webbrowser
from multiprocessing import Queue
from threading import Event

import pyautogui
import pyttsx3 # Conversión de texto a voz
import speech_recognition as sr # Reconocimiento de voz

import scripts.utils as utils
from scripts.addresses import addresses

class AssistantApp:
    RECOGNITION_ERROR = '--error--'
    config = configparser.ConfigParser()
    MESSAGE_DONTKNOW = 'No te entendi'

    def __init__(self, q: Queue, stop_event: Event, modo_discreto: int, api_key: str):
        self.q = q
        self.stop_event = stop_event
        self.modo_discreto = modo_discreto
        self.config.read('config.ini')
        self.name = self.config.get('Assistant', 'name', fallback='okay') # Le definimos un nombre al asistente, o simplemente una palabra clave que hace que se active
        self.humor = self.config.getint('Assistant', 'humor', fallback=5) # Porcentaje de humor al n%. Significa que va a poner un audio "gracioso" el n% de las veces en los pedidos que tengan humor configurado
        self.chronometer = self.config.getfloat('Assistant', 'chronometer', fallback=0)
        self.informal_chat = self.config.getint('Assistant', 'informal_chat', fallback=0)
        self.api_key = api_key
        self.user = os.environ.get('USERNAME') or os.environ.get('USER') # El usuario de tu PC actual
        self.continue_ = True
        self.attempts = 0
        self.configaudio()
        self.chat = utils.restart_ia(self.informal_chat, self.print_and_talk, self.api_key, self.stop)
        self.print_('Encendido')
        self.start()
        self.print_('Detenido')

    #! Configuración de audio
    def configaudio(self):
        self.engine = pyttsx3.init() # Inicializamos el motor de voz
        self.engine.setProperty('rate', 145) # Velocidad del asistente al hablar
        self.engine.setProperty('volume', 1.0) # Volumen del asistente

        voices = self.engine.getProperty('voices')  # Accedemos al objeto "voices". Hacemos esto para obtener todas las voces del motor
        selected_volume = next((v for v in voices if 'ES' in v.id), None) or next((v for v in voices if 'EN' in v.id), voices[0].id)  # Analiza las voces instaladas del sistema y trata de colocar español (de preferencia) o inglés
        self.engine.setProperty('voice', selected_volume)

    #! Configuramos los mensajes en la consola y la salida de audio
    def print_(self, text: str):
        print(text)
        self.q.put(text)

    def print_and_talk(self, text: str): # El asistente imprime el texto pasado como argumento y lo reproduce
        self.print_(text)
        if not self.modo_discreto: self.engine.say(text)
        if self.engine._inLoop: self.engine.endLoop() # Si el motor de voz está en un loop, lo detenemos para evitar errores
        self.engine.runAndWait()

    #! Configuramos el detenimiento del asistente
    def stop(self):
        if utils.check_humor(self.humor):
            utils.play_sound('Hasta_la_proxima', self.print_and_talk)
            time.sleep(3) # Hago que espere estos segundos para darle tiempo a que el audio termine
        else:
            self.print_and_talk('Deteniendo')
        self.continue_ = False

    #! Lógica y reconocimiento de los pedidos
    def run(self):
        rec = self.listen() # Retorna el pedido de un usuario
        if rec == self.RECOGNITION_ERROR: return None # No trata de ejecutar ningún pedido si hubo algún error
        index_first_name = rec.find(self.name) # Busca la posición donde inicia el nombre del asistente
        index_second_name = rec.find(self.name, index_first_name + len(self.name)) # Busca la posición donde termina la segunda vez que se dijo el nombre del asistente (en caso de que lo haya dicho dos veces)
        if index_second_name != -1: # Si el usuario dijo dos veces el nombre del asistente, entonces mejor, ya que podrá entender mejor el pedido. 
            rec = rec[index_first_name+len(self.name) : index_second_name].strip() # Se quedará únicamente con lo que dijo en medio
        else:
            rec = rec[index_first_name+len(self.name):].strip() # Recorta la grabación hasta el momento donde se dice el nombre
        self.request(rec) # Ejecuta el pedido

    def listen(self): # Se repite el while hasta que detecte que se llamó al asistente por su nombre o hasta que de error
        while True:
            if self.stop_event.is_set():
                self.stop()
                return self.RECOGNITION_ERROR
            rec = self.recognise_speech_and_pass_it_to_text()
            if self.name in rec or rec == self.RECOGNITION_ERROR: return rec

    def recognise_speech_and_pass_it_to_text(self, connection_failures = 0):
        self.attempts += 1
        if (not self.informal_chat) and (self.attempts % 100 == 0): self.chat = utils.restart_ia(self.informal_chat, self.print_and_talk, self.api_key) # Reinicia la IA cada 100 escuchas, siempre y cuando estemos en un chat formal
        try:
            with sr.Microphone() as source: # Abrimos el micrófono como fuente de entrada de audio
                listener = sr.Recognizer()
                listener.adjust_for_ambient_noise(source, duration = 1) # Ajusta el nivel de ruido ambiental. Duration son los segundos que tarda en ajustar el ruido ambiental
                self.print_(f'\n{self.attempts}) Escuchando...')
                # Acá comienza a escuchar, tiene una tolerancia máxima de 10 segundos de no escuchar nada. Sirve para tratar de evitar que la grabación se trabe por estar encendida mucho tiempo.
                # El phrase_time_limit es el tiempo máximo que dura cada frase, pero lo pongo más que nada para que no se quede colgado luego de suspender la máquina, ya que internamente cree que el usuario sigue hablando
                voice = listener.listen(source, timeout=10, phrase_time_limit=60)
                self.print_('Procesando...')
                return str(sr.Recognizer().recognize_google(voice, language='es', show_all=False, pfilter=0)).lower() # Acá se almacena lo que se grabó. Usa el servicio de Google para reconocer el habla en español y lo convierte a minúsculas. Da error cuando no escucha nada
        except sr.RequestError:
            N = 3 # Cantidad de veces que va a intentar reconectarse a internet en caso de que falle
            if connection_failures < N:
                self.print_('Internet no detectado. Reintentando...')
                time.sleep(5)
                return self.recognise_speech_and_pass_it_to_text(connection_failures+1)
            else:
                self.print_and_talk('Fallo de conexión a internet')
                self.stop()
        except sr.UnknownValueError:
            self.print_('No se escuchó nada. Reintentando...')
        except sr.WaitTimeoutError:
            self.print_("Tiempo de espera agotado. Reintentando...")
        except Exception as e:
            self.print_and_talk('Error desconocido en el reconocimiento')
            self.print_(f'Error:\n{e}')
        return self.RECOGNITION_ERROR

    def request(self, rec: str):
        print(f'rec: {rec}')
        try:
            if len(rec) == 0: return self.print_and_talk('¿Qué pasa?') # Si el pedido incluía sólo el nombre
            if rec == 'gracias' or rec == 'muchas gracias': return self.print_and_talk('De nada')
            if rec == 'hola' or rec == 'buenas' or rec == 'buenos días' or rec == 'buenas tardes':
                if utils.check_humor(self.humor): return utils.play_random_sound(['wazaa', 'hello_m_f'], self.print_and_talk)
                return self.print_and_talk('hola')

            if any(word == rec.split(' ')[-1] for word in ['basta', 'apaga', 'apagues']): return self.stop() # Apaga al asistente. La palabra "basta" debe decirse al final (o alguna variante similar)

            if self.informal_chat: # Si estamos en un chat informal, ignoramos los pedidos
                return self.print_and_talk(utils.process_with_natural_language_informal_talk(rec, self.chat, self.api_key))

            response_ia = utils.process_with_natural_language(rec, self.chat, self.api_key)

            if response_ia["action"] == "none": # Esto no debería suceder nunca. Si sucede, es porque se está inventando cosas
                self.chat = utils.restart_ia(self.informal_chat, self.print_and_talk, self.api_key)
                self.print_and_talk(self.MESSAGE_DONTKNOW)

            elif self.order_without_ia(rec): None

            elif response_ia["action"] != "order_not_in_list": # Si la IA detecta que el pedido está dentro de los pre-configurados para ella
                self.order_with_ia(response_ia)

            else: # Si detecta algo pero no lo entiende o se pide algo que no está programado:
                if 100 * random.random() < 20: # Una de cada cinco veces te da una respuesta más larga
                    self.print_and_talk('No te entendí. Es posible que el pedido no esté preconfigurado')
                else:
                    self.print_and_talk(self.MESSAGE_DONTKNOW)
        except Exception as e:
            self.print_and_talk('Error desconocido') # Si hay un error no previsto, dice "Error desconocido", muestra el error y vuelve al while original
            self.print_(f'Error:\n{e}')

    def order_without_ia(self, rec: str):
        rec = rec.lower().replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u').replace('Á', 'A').replace('É', 'E').replace('Í', 'I').replace('Ó', 'O').replace('Ú', 'U')

        if any(word == rec.split(' ')[-1] for word in ['cancela', 'cancelar', 'cancelas', 'cancelalo', 'olvidalo', 'cancelarlo']): # Cancela el pedido que estás solicitando. La palabra "cancelar" debe decirse al final (o alguna variante similar)
            self.print_and_talk('Ok, cancelo el pedido')

        elif any(word in rec for word in ['cierr', 'cerra']) and any(word in rec for word in ['ventana', 'programa', 'archivo']):
            pyautogui.hotkey('alt', 'F4')
            self.print_and_talk('Hecho')

        elif "tecla " in rec and len(rec.split())-1 >= rec.split().index('tecla')+1: # Si dice la palabra "tecla" en cualquier momento excepto en la palabra final, presiona la tecla pedida luego de esa palabra. Ej: "Presiona la tecla p por favor"
            utils.key_press(rec, self.print_and_talk)

        elif 'alarma' == rec.split()[-1]: utils.play_sound(rec, self.print_and_talk) # Si "alarma" se dice al final
        else: return False
        return True

    def order_with_ia(self, response_ia: dict[str, str]):
        action = response_ia["action"]

        if action == "search":
            site = response_ia["site"].lower()
            query = response_ia["query"]

            if "windows" in site:
                pyautogui.hotkey('win', 's') # Abre el buscador de windows, busca lo que pediste y presiona "enter"
                time.sleep(5)
                pyautogui.typewrite(query)
                time.sleep(5)
                pyautogui.hotkey('enter')
                self.print_and_talk("Hecho")
            else:
                for dir in addresses: # Busca en el sitio solicitado la búsqueda solicitada
                    if 'buscador' in addresses[dir]:
                        if site in [dir.lower() for dir in addresses[dir]['sitios']]:
                            webbrowser.open(f'{addresses[dir]["buscador"]}{query}')
                            self.print_and_talk("Buscando")
                            break
                else:
                    self.print_and_talk('El sitio no está preconfigurado')

        elif action == "program_order":
            minutes_string = response_ia["minutes"]

            if isinstance(minutes_string, str) and (',' in minutes_string):
                minutes_string = minutes_string.split(',')[0]

            threading.Timer(int(float(minutes_string))*60, lambda: self.request(response_ia["order"])).start() # Ejecuta el pedido en la cantidad de minutos que hayamos especificado
            self.print_and_talk('Ok, lo recordaré')

        elif action == "time": # Hora actual
            hora = datetime.now().strftime('%H:%M %p')
            self.print_and_talk(f'Son las {hora}')

        elif action == "date": # Fecha actual
            fecha = datetime.now().strftime('%d/%m/%Y')
            self.print_and_talk(f'Hoy es {fecha}')

        elif action == "atajo":
            self.print_and_talk(f'Abriendo atajo {response_ia["number"]}')
            pyautogui.hotkey('win', response_ia["number"])

        elif action == "open":
            sitio = response_ia["name"].lower()
            for dir in addresses:
                if 'url' in addresses[dir]:
                    if sitio in [site.lower() for site in addresses[dir]['sitios']]: # Si el sitio está dentro de los preconfigurados
                        if "http" in addresses[dir]['url']: # Si se intenta abrir un sitio web
                            webbrowser.open(addresses[dir]["url"])
                            self.print_and_talk("Hecho")
                            break

                        elif addresses[dir]['url'].startswith('C:'): # Si se intenta abrir un archivo local (aunque por ahora no le doy uso)
                            if os.path.exists(addresses[dir]["url"]):
                                os.startfile(addresses[dir]["url"])
                                break
            else:
                self.print_and_talk('El sitio no está preconfigurado')

        elif action == "play_music":
            if os.path.exists(addresses["canciones"]["url"]):
                os.startfile(addresses["canciones"]["url"])
                pyautogui.press('volumedown', 50), pyautogui.press('volumeup', 10) # Para que ponga el volumen al 20%
                self.print_and_talk('Reproduciendo música')
            else:
                webbrowser.open(addresses["sourcecode"]["url"])
                self.print_and_talk('Error: debes colocar un archivo de audio para que yo pueda reproducirlo. Consulta el block de ayuda para más información')

        elif action == "switch_mute":
            pyautogui.hotkey('volumemute')
            self.print_and_talk('Hecho')

        elif action == "minimize":
            with pyautogui.hold('down'):
                pyautogui.press(['alt', 'space'])
            time.sleep(0.2)
            pyautogui.press('n')
            self.print_and_talk('Hecho')

        elif action == "minimize_all":
            pyautogui.hotkey('win', 'd')
            self.print_and_talk('Hecho')

        elif action == "set_volume":
            number_string = response_ia["number"]

            if isinstance(number_string, str) and (',' in number_string):
                number_string = number_string.split(',')[0]

            numero = int(float(number_string))

            if numero < 0 or numero > 100:
                self.print_and_talk('El volumen solicitado debe ser un número entero entre 0 y 100')
            else:
                half_volume = round(numero/2)
                pyautogui.press('volumedown', 50)
                pyautogui.press('volumeup', half_volume)
                self.print_and_talk(f'Volumen al {2*half_volume} por ciento') # Lo hago así sabiendo que el resultado siempre será par, ya que los botones mueven el valor de volumen de a dos unidades

        elif action == "tell_joke": self.print_and_talk(response_ia["joke"])

        elif action == "ask_name":
            if utils.check_humor(self.humor): utils.play_random_sound(['Excel_preg', 'Marad_ee', 'No_lo_se_tu_dime', 'muy_buena_preg', 'info_vale_millones', 'Uvuewewe'], self.print_and_talk)
            else: self.print_and_talk(f'Me llamo {self.name}')

        elif action == "screenshot":
            screenshot = pyautogui.screenshot()
            carpeta_contenedora = 'screenshots'
            if not os.path.exists(carpeta_contenedora): os.makedirs(carpeta_contenedora)
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S").replace(' ', '_').replace(':', '_')
            screenshot.save(f'{carpeta_contenedora}/{now}_screenshot.png')
            self.print_and_talk('Captura guardada')

        elif action == "chronometer":
            state = response_ia["state"]
            self.chronometer = utils.chronometer(state, self.chronometer, self.print_and_talk, self.humor, self.config)

        elif action == "check_level_humor": self.print_and_talk(f'Nivel de humor al {self.humor}%. Si querés modificarlo consulta las notas de ayuda')

        elif action == "set_level_humor":
            humor_nuevo_string = response_ia["level"]

            if isinstance(humor_nuevo_string, str) and (',' in humor_nuevo_string):
                humor_nuevo_string = humor_nuevo_string.split(',')[0]

            humor_nuevo = int(float(humor_nuevo_string))

            if humor_nuevo == 100:
                frases = ['Formateo programado para las 22 horas', 'Autodestrucción en t menos 10 segundos', 'Humor al 100%']
                self.print_and_talk(random.choice(frases))
                self.humor = utils.change_value(self.config, 'humor', humor_nuevo)
            elif humor_nuevo >= 0 and humor_nuevo < 100:
                self.print_and_talk(f'Humor al {humor_nuevo}%')
                self.humor = utils.change_value(self.config, 'humor', humor_nuevo)
            else:
                self.print_and_talk('El nivel de humor se pide en términos porcentuales del 0 al 100')
                if utils.check_humor(self.humor): utils.play_random_sound(['Ah_re_bolu', 'Estup', 'Imbec'], self.print_and_talk)

        elif action == "need_help":
            webbrowser.open(addresses["sourcecode"]["url"])
            self.print_and_talk('Proporcionando ayuda')
            if utils.check_humor(self.humor): utils.play_random_sound(['buen_servicio'], self.print_and_talk)

        elif action == "send_source_code":
            webbrowser.open(addresses["sourcecode"]["url"])
            self.print_and_talk('Abriendo código fuente')
            if utils.check_humor(self.humor): utils.play_random_sound(['buen_servicio', 'es_bellisimo'], self.print_and_talk)

        elif action == "ask_weather":
            webbrowser.open(f'{addresses["google"]["buscador"]}{response_ia["query"]}')
            self.print_and_talk('Hecho')
            if utils.check_humor(self.humor): utils.play_random_sound(['buen_servicio'], self.print_and_talk)

        elif action == "multiple_orders":
            orders_string = response_ia["orders"]

            if isinstance(orders_string, str) and (';' in orders_string):
                list_orders = orders_string.split(';')
                for _, order in enumerate(list_orders):
                    self.request(order)
            else:
                self.chat = utils.restart_ia(self.informal_chat, self.print_and_talk, self.api_key)
                self.print_and_talk(self.MESSAGE_DONTKNOW)

        elif action == "response":
            self.print_and_talk(response_ia["text"])

        else: # No debería llegar nunca acá. Si eso sucede, es porque se está inventando cosas
            self.chat = utils.restart_ia(self.informal_chat, self.print_and_talk, self.api_key)
            self.print_and_talk(self.MESSAGE_DONTKNOW)

    #! Ciclo para hacer que el asistente inicie y no termine nunca a menos que se lo pidamos específicamente
    def start(self):
        while self.continue_:
            self.run()
        self.engine.stop()
