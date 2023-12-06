import webbrowser
from scripts.addresses import addresses, dir_mixer
import pyautogui
import time
import numpy as np
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
from pygame import mixer
import random
import scripts.filter_phrases as filterPhrases

def delete_introductory_phrases(rec: str, delete_phrases: list[str]) -> str:
    delete_phrases_orderer = sorted(delete_phrases, key=lambda x: len(x), reverse=True) # Reordena según la longitud de caracteres, de mayor a menor

    for phrase in delete_phrases_orderer: # Se elimina de rec la primera frase encontrada de la lista
        if rec.startswith(phrase + ' '):
            rec = rec[len(phrase + ' '):]
            break
    return rec

def delete_end_phrases(rec: str) -> str: # Análogo a delete_introductory_phrases, pero con las frases finales
    delete_phrases_orderer = sorted(filterPhrases.final_phrases, key=lambda x: len(x), reverse=True)
    for frase in delete_phrases_orderer:
        if rec.endswith(frase):
            rec = rec[:-len(frase)-1]
            break
    return rec

def search(rec: str) -> bool:
    if "en " not in rec: return False
    rec = delete_until_you_find_some_phrase(rec, ['buscame', 'buscar', 'buscas', 'busca', 'buscarias', 'busques']) # Además de ejecutar la funcion, defino un rec local para no modificar al original por si esta función llega a retornar False
    rec = delete_introductory_phrases(rec, filterPhrases.search_phrases)

    if 'en windows' in rec or 'en el buscador de windows' in rec: # En caso de que la búsqueda sea en el buscador de windows. No la recomiendo
        if "en windows" in rec:
            indexPalClave = rec.find(f'en windows')
        else:
            indexPalClave = rec.find(f'en el buscador de windows')
        rec = rec[:indexPalClave-1] # Recorta la grabación hasta el momento donde se la frase de "en windows" o "en el buscador de windows"
        pyautogui.hotkey('win', 's') # Abre el buscador de windows, busca lo que pediste y presiona "enter"
        time.sleep(5)
        pyautogui.typewrite(rec)
        time.sleep(5)
        pyautogui.hotkey('enter')
        return True

    array_sitios: list[str] = []
    for dir in addresses: # Crea un array con todos los sitios del diccionario "addresses", siempre y cuando se pueda buscar en ellos
        if 'sitios' in addresses[dir] and 'buscador' in addresses[dir]:
            array_sitios.extend(addresses[dir]['sitios'])

    sitio = ""
    busqueda = ""
    for sitios in array_sitios: # Elimina todas las "sitios" al final del pedido y "en" (después del for, si rec="Buscar oso en google", ahora rec="oso")
        if f'en {sitios.lower()}' in rec:
            sitio = sitios # Si algún sitio fue encontrado, lo toma
            indexPalClave = rec.find(f'en {sitios.lower()}')
            busqueda = rec[:indexPalClave-1]
            break

    if sitio == "": return False # Si ningún sitio fue solicitado en el pedido, se da por hecho que el usuario no quiere buscar nada y termina la función

    for dir in addresses: # Busca en el sitio solicitado la búsqueda solicitado
        if 'buscador' in addresses[dir]:
            if sitio in addresses[dir]['sitios']:
                webbrowser.open(f'{addresses[dir]["buscador"]}{busqueda}')
    return True

def key_press(rec: str, print_and_talk):
    rec_array = rec.split()
    indexTecla = rec_array.index('tecla')
    rec = rec_array[indexTecla+1] # Array rec a partir desde el momento que se dijo la palabra tecla

    teclas, contador = {'arriba' : "up", 'abajo' : "down", 'derecha' : 'right', 'izquierda' : 'left', 'espacio' : 'space', 'borrar' : 'backspace', 'enter' : 'enter', 'tab' : 'tab'}, 0
    for i in teclas:
        if rec == i:
            pyautogui.press(teclas[rec])
            print_and_talk('Hecho')
            break
        contador += 1
    if contador == len(teclas):
        pyautogui.press(rec)
        print_and_talk('Hecho')

def repetir(rec: str, print_and_talk) -> bool:
    frase_a_repetir = delete_introductory_phrases(rec, ['repeti', 'repite', 'deci', 'repetis'])
    if frase_a_repetir == rec: return False
    print_and_talk(rec)
    return True

def shortcut(rec: str, print_and_talk):
    rec_array = rec.split()
    indexTecla = rec_array.index('atajo')
    rec = rec_array[indexTecla+1] # Array rec a partir desde el momento que se dijo la palabra atajo

    numeros, palabras = '123456789', ['uno', 'dos', 'tres', 'cuatro', 'cinco', 'seis', 'siete', 'ocho', 'nueve'] # Tuve que hacer esto ya que el asistente a veces reconoce los números como palabras (en vez de "3" puede registrar "tres" por ejemplo)
    for i, (numero, palabra) in enumerate(zip(numeros, palabras)):
        if numero in rec or palabra in rec:
            print_and_talk(f'Abriendo atajo {numero}')
            pyautogui.hotkey('win', numero)
            break
    else:
        print_and_talk('Los atajos son números del 1 al 9')

def open_(rec: str, print_and_talk, humor: int | float):
    array_sitios: list[str] = []
    for dir in addresses: # Crea un array con todos los sitios del diccionario "addresses"
        if 'sitios' in addresses[dir] and 'url' in addresses[dir]:
            array_sitios.extend(addresses[dir]['sitios'])

    sitio = ""
    for sitios in array_sitios: # Busca en el sitio solicitado en el pedido
        if sitios.lower() in rec:
            sitio = sitios
            break

    if sitio == "": return print_and_talk("El sitio no está registrado o no se entendió el pedido")

    for dir in addresses:
        if 'url' in addresses[dir]:
            if sitio in addresses[dir]['sitios']: # Si el sitio está dentro de los preconfigurados
                if "http" in addresses[dir]['url']: # Si se intenta abrir un sitio web
                    webbrowser.open(addresses[dir]["url"])
                    if dir == 'sourcecode' and check_humor(humor): play_random_sound(['buen_servicio', 'es_bellisimo'], print_and_talk)

                elif addresses[dir]['url'].startswith('C:'): # Si se intenta abrir un archivo local
                    if os.path.exists(addresses[dir]["url"]):
                        os.startfile(addresses[dir]["url"])

                    if sitio in addresses['canciones']['sitios']: # Si además el archivo local es el archivo de audio reservado de música
                        if os.path.exists(addresses[dir]["url"]):
                            p_ = pyautogui.press('volumedown', 50), pyautogui.press('volumeup', 10)
                        else:
                            p_ = pyautogui.press('volumedown', 50), pyautogui.press('volumeup', 10)
                            webbrowser.open(addresses["sourcecode"]["url"])
                            return print_and_talk('Error: debes colocar un archivo de audio para que yo pueda reproducirlo. Consulta el block de ayuda para más información')

                else: # Si el archivo local es interno del asistente (aunque actualmente no hay ninguno)
                    os.startfile(f'/{addresses[dir]["url"]}')
                return print_and_talk("Hecho")
    print_and_talk("El sitio no está registrado o no se entendió el pedido") 

def change_volume(rec: str, print_and_talk):
    numero = get_percentage(rec)
    if numero < 0 or numero > 100:
        print_and_talk('El volumen solicitado debe ser un número entero entre 0 y 100')
    else:
        half_volume = round(numero/2)
        pyautogui.press('volumedown', 50)
        pyautogui.press('volumeup', half_volume)
        print_and_talk(f'Volumen al {2*half_volume} por ciento') # Lo hago así sabiendo que el resultado siempre será par, ya que los botones mueven el valor de volumen de a dos unidades

def chronometer(rec: str, chronometer: float | int, print_and_talk, humor: int | float, config):
    if any(keyword in rec for keyword in ['inicia', 'comenza', 'comienza']):
        print_and_talk('Iniciando cronómetro')
        chronometer = change_value(config, 'chronometer', time.time()) # Registra el tiempo actual
    else: # Cuando se detiene averigua cuánto tiempo pasó
        if chronometer == 0:
            print_and_talk('No puedes detener un cronómetro que no ha sido iniciado')
            if check_humor(humor): play_random_sound(['Ah_re_bolu', 'Estup', 'Imbec'], print_and_talk)
        else:
            tiempo_pasado = round(time.time() - chronometer) # Tiempo pasado en segundos

            dias_sr = tiempo_pasado/60/60/24 # el _sr significa que es el valor real
            dias = int(np.floor(dias_sr))

            horas_sr = (dias_sr - dias)*24
            horas = int(np.floor(horas_sr)) # Horas pasadas

            minutos_sr = (horas_sr - horas)*60
            minutos = int(np.floor(minutos_sr))

            segundos_sr = (minutos_sr - minutos)*60
            segundos = int(np.round(segundos_sr))

            string_res = 'Pasaron '
            if dias != 0:
                string_res += f'{dias} días '

            if horas != 0:
                string_res += f'{horas} horas '

            if minutos != 0:
                string_res += f'{minutos} minutos '

            if segundos != 0:
                if horas != 0 or minutos != 0 or dias != 0:
                    string_res += f'y {segundos} segundos'
                else:
                    string_res += f'{segundos} segundos'
            print_and_talk(string_res)
            chronometer = change_value(config, 'chronometer', 0)
    return chronometer

def play_sound(rec: str, print_and_talk, cantidad = 1): # Reproduce sonidos pedidos en formato mp3 que estén en "direccion_m"
    try:
        for i in dir_mixer:
            if i in rec:
                mixer.init()
                mixer.music.load(f"./complementos/audio/{dir_mixer[i]['nombre']}.mp3")
                mixer.music.set_volume(dir_mixer[i]['volumen'])
                mixer.music.play(cantidad) # mixer.music.play(n) suena n veces
                break
    except Exception as e:
        print_and_talk('Error, el archivo de sonido no está o no funciona')

def play_random_sound(opciones: list[str], print_and_talk):
    play_sound(random.choice(opciones), print_and_talk)

def check_humor(humor: int | float): # Agarra un número al azar y evalúa si se activa un comentario "gracioso" en algunos pedidos
    return 100 * random.random() < humor

def get_percentage(rec: str): # Obtiene el número entero n de la cadena "bla bla bla n% bla bla"
    numero = rec.split('%')[0].split(' ')[-1]
    numero_entero = numero.replace('.', ',').split(',')[0]
    return int(numero_entero)

def delete_until_you_find_some_phrase(rec: str, frases: list[str]): # En caso de que el usuario diga alguna de las palabras de "frases", elimina de rec todo lo que haya dicho antes de eso
    frases_buscar_ordenadas = sorted(frases, key=lambda x: len(x), reverse=True)

    for frase in frases_buscar_ordenadas:
        if frase in rec:
            rec = rec[rec.find(frase):]
            break
    return rec

def change_value(config, clave: str, valor: int | float): # Modifica el valor de un dato en config.ini
    config.set('Assistant', clave, str(valor))
    with open('config.ini', 'w') as f:
        config.write(f)
    return valor
