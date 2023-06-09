import re
import webbrowser
import scripts.direcciones_ as direcciones_
import pyautogui
import time
import os
import pkg_resources
import importlib.util
import time
import numpy as np
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
from pygame import mixer
import random

asistente_virtual_name = importlib.util.resolve_name('asistente_virtual', package=None)
direcciones = direcciones_.direcciones
dir_mixer = direcciones_.dir_mixer

def eliminar_frases_introductorias(rec: str, array: list) -> str:
    frases_a_borrar = [ f'{frase} ' for frase in array ] # Agrega un espacio en cada frase
    frases_a_borrar_ordenadas = sorted(frases_a_borrar, key=lambda x: len(x), reverse=True) # Reordena según la longitud de caracteres, de mayor a menor
    
    continuar = True
    while continuar: # Se asegura de que las frases de "frases_a_borrar" se eliminen de rec, siempre y cuando se ubiquen al principio
        for frase in frases_a_borrar_ordenadas:
            if rec.startswith(frase):
                rec = rec[len(frase):]
                break
        else: # El else se ejecuta si el for no se interrumpió
            continuar = False
    return rec

def eliminar_frases_finales(rec: str) -> str: # Análogo a eliminar_frases_introductorias
    frases_a_borrar = ['por favor', 'gracias', 'muchas gracias', 'muchisimas gracias']
    frases_a_borrar_ordenadas = sorted(frases_a_borrar, key=lambda x: len(x), reverse=True)
    continuar = True
    while continuar:
        for frase in frases_a_borrar_ordenadas:
            if rec.endswith(frase):
                rec = rec[:-len(frase)-1]
                break
        else:
            continuar = False
    return rec

def buscar(rec: str) -> bool:
    if "en " not in rec: return False
    frases_a_buscar = ['buscame', 'buscar', 'buscas', 'busca', 'buscarias']
    frases_a_buscar_ordenadas = sorted(frases_a_buscar, key=lambda x: len(x), reverse=True)
    
    rec = rec # Defino un rec local para no modificar al original por si esta función llega a retornar False
    
    if any(word in rec for word in frases_a_buscar_ordenadas): # En caso de que el usuario diga alguna de las palabras de "frases_a_buscar", elimina de rec todo lo que haya dicho antes de eso
        for frase in frases_a_buscar_ordenadas:
            if frase in rec:
                posicion_inicio_frase = rec.find(f'{frase}') # Busca la posición donde inicia el nombre del asistente
                rec = rec[posicion_inicio_frase:]
                break
    
    rec = eliminar_frases_introductorias(rec, ['buscame', 'buscar', 'buscas', 'busca', 'a', 'al', 'buscarias'])
    
    if 'en windows' in rec or 'en el buscador de windows' in rec: # En caso de que la búsqueda sea en el buscador de windows
        if "en windows" in rec:
            indexPalClave = rec.find(f'en windows')
        else:
            indexPalClave = rec.find(f'en el buscador de windows')
        rec = rec[:indexPalClave-1]
        pyautogui.hotkey('win', 's')
        time.sleep(2)
        pyautogui.typewrite(rec)
        time.sleep(1)
        pyautogui.hotkey('enter')
        return True 
    
    array_palClave = []
    for dir in direcciones: # Crea un array con todas las palabras clave del diccionario "direcciones"
        if 'palClave' in direcciones[dir] and 'buscador' in direcciones[dir]:
            array_palClave.extend(direcciones[dir]['palClave'])

    sitio = ""
    for palClave in array_palClave: # Elimina todas las "palClave" al final del pedido y "en" (después del for, si rec="Buscar oso en google", ahora rec="oso")
        if f'en {palClave.lower()}' in rec:
            sitio = palClave # Si alguna palabra clave fue encontrada, la toma
            indexPalClave = rec.find(f'en {palClave.lower()}')
            rec = rec[:indexPalClave-1]
            break
    
    if sitio == "": return False # Si ningún sitio fue solicitado en el pedido, se da por hecho que el usuario no quiere buscar nada y termina la función

    for dir in direcciones: # Crea un array con todas las palabras clave del diccionario "direcciones"
        if 'buscador' in direcciones[dir]:
            if sitio in direcciones[dir]['palClave']:
                webbrowser.open(f'{direcciones[dir]["buscador"]}{rec}')
    return True

def apretar_tecla(rec: str, print_and_talk):
    rec_array = rec.split()
    indexTecla = rec_array.index('tecla')
    rec = rec_array[indexTecla+1]
    
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
    frase_a_repetir = eliminar_frases_introductorias(rec, ['repeti', 'repite', 'deci', 'repetis'])
    if frase_a_repetir == rec: return False
    print_and_talk(rec)
    return True

def atajos(rec: str, print_and_talk):
    rec_array = rec.split()
    indexTecla = rec_array.index('atajo')
    rec = rec_array[indexTecla+1]
    
    numeros, palabras, contador = '123456789', ['uno', 'dos', 'tres', 'cuatro', 'cinco', 'seis', 'siete', 'ocho', 'nueve'], 0 # Tuve que hacer esto ya que el asistente a veces reconoce los números como palabras (en vez de "3" puede registrar "tres" por ejemplo)
    for i in range(9):
        if numeros[i] in rec or palabras[i] in rec:
            print_and_talk(f'Abriendo atajo {numeros[i]}')
            pyautogui.hotkey('win', numeros[i])
            break
        contador += 1    
    if contador == 9:
        print_and_talk('Los atajos son números del 1 al 9')

def abrir(rec: str, print_and_talk, humor):
    array_palClave = []
    for dir in direcciones: # Crea un array con todas las palabras clave del diccionario "direcciones"
        if 'palClave' in direcciones[dir] and 'url' in direcciones[dir]:
            array_palClave.extend(direcciones[dir]['palClave'])    

    sitio = ""
    for palClave in array_palClave: # Elimina todas las "palClave" al final del pedido y "en" (a esta altura, si rec="Buscar oso en google", ahora rec="oso")
        if palClave.lower() in rec:
            sitio = palClave
            break
        
    if sitio == "": return print_and_talk("El sitio no está registrado o no se entendió el pedido") 
    for dir in direcciones: # Crea un array con todas las palabras clave del diccionario "direcciones"
        if 'url' in direcciones[dir]:
            if sitio in direcciones[dir]['palClave']:
                if "http" in direcciones[dir]['url']: # Si se intenta abrir un sitio web                        
                    webbrowser.open(f'{direcciones[dir]["url"]}')
                    if dir == 'codigofuente' and deHumor(humor): mixer_varias_opciones(['buen_servicio', 'es_bellisimo'], print_and_talk)
                    if dir == 'ayuda' and deHumor(humor): mixer_varias_opciones(['buen_servicio'], print_and_talk)
                    
                elif direcciones[dir]['url'].startswith('C:'): # Si se intenta abrir un archivo local
                    if os.path.exists(f'{direcciones[dir]["url"]}'): os.startfile(f'{direcciones[dir]["url"]}')
                    
                    if sitio in ['canciones', 'musica']: # Si el archivo local es el archivo de audio reservado de música
                        if os.path.exists(f'{direcciones[dir]["url"]}'):
                            pyautogui.press('volumedown', 50), pyautogui.press('volumeup', 10)
                        else:
                            return print_and_talk(f'Error: debes colocar un archivo de audio para que yo pueda reproducirlo. Consulta el block de ayuda para más información')
 
                else: # Si el archivo local es interno del asistente
                    os.startfile(pkg_resources.resource_filename(asistente_virtual_name, f'/{direcciones[dir]["url"]}'))
                return print_and_talk("Hecho")
    print_and_talk("El sitio no está registrado o no se entendió el pedido") 


def volumen_al(rec, print_and_talk):
    numero = obtener_numero(rec)
    if numero < 0 or numero > 100:
        print_and_talk('El volumen solicitado debe ser un número entero entre 0 y 100')
    else:
        pyautogui.press('volumedown', 50)
        pyautogui.press('volumeup', round(numero/2))
        print_and_talk(f'Volumen al {2*round(numero/2)} por ciento') # Lo hago así sabiendo que el resultado siempre será par, ya que los botones mueven el valor de volumen de a pares

def cronometro(rec: str, cronometro: int, print_and_talk, humor:int):
    if 'inicia' in rec or 'comenza' in rec or 'comienza' in rec:
        print_and_talk('Iniciando cronómetro')
        cronometro = time.time() # Registra el tiempo actual
    else: # Cuando se detiene averigua cuánto tiempo pasó
        if cronometro == 0:
            print_and_talk('No puedes detener un cronómetro que no ha sido iniciado')
            if deHumor(humor): mixer_varias_opciones(['Ah_re_bolu', 'Estup', 'Imbec'], print_and_talk)            
        else:
            tiempo_pasado = round(time.time() - cronometro) # Tiempo pasado en segundos
            
            horas_sr = tiempo_pasado/60/60
            horas = int(np.floor(horas_sr)) # Horas pasadas

            minutos_sr = (horas_sr - horas)*60
            minutos = int(np.floor(minutos_sr))

            segundos_sr = (minutos_sr - minutos)*60
            segundos = int(np.round(segundos_sr))

            horas_ = f'{horas}' if horas > 9 else f'0{horas}' # Agregamos ceros de ser necesario, ya que se necesita un formato xx:xx:xx
            minutos_ = f'{minutos}' if minutos > 9 else f'0{minutos}'
            segundos_ = f'{segundos}' if segundos > 9 else f'0{segundos}'
            print_and_talk(f'Pasaron {horas_}:{minutos_}:{segundos_}')
            cronometro = 0
    return cronometro

def mixer_(rec, print_and_talk, cantidad = 1):        #Reproduce sonidos pedidos en formato mp3 que estén en "direccion_m"
    try:
        for i in dir_mixer:
            if i in rec:
                mixer.init()
                mixer.music.load(pkg_resources.resource_filename(asistente_virtual_name, f"/complementos/audio/{dir_mixer[i]['nombre']}.mp3"))
                mixer.music.set_volume(dir_mixer[i]['volumen'])
                mixer.music.play(cantidad) # mixer.music.play(n) suena n veces
                break
    except Exception as e:
        print_and_talk('Error, el archivo de sonido no está o no funciona')

def mixer_varias_opciones(opciones, print_and_talk):
    mixer_(random.choice(opciones), print_and_talk)

def deHumor(humor): # Agarra un número al azar y evalúa si se activa un comentario "gracioso" en algunos pedidos
    if 100*random.random() < humor: return True
    return False

def obtener_numero(rec: str):
    split = rec.split()
    numero = int([i for i in split if '%' in i][0][:-1].replace('.', ',').split(',')[0]) # Obtiene el número entero n de la cadena "bla bla bla n% bla bla"
    return numero
