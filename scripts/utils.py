from scripts.addresses import dir_mixer
import pyautogui
import time
import numpy as np
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
from pygame import mixer
import random
import json
from scripts.train_ai import safety_settings

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

def chronometer(state: str, chronometer: float | int, print_and_talk, humor: int | float, config):
    if state == "iniciar":
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

def change_value(config, clave: str, valor: int | float): # Modifica el valor de un dato en config.ini
    config.set('Assistant', clave, str(valor))
    with open('config.ini', 'w') as f:
        config.write(f)
    return valor

def process_with_natural_language(rec: str, chat):
    response_ia = chat.send_message(rec, safety_settings=safety_settings)
    try: # En caso de que la respuesta no sea un json, tal como lo especifiqué
        return json.loads(response_ia.text)
    except:
        return json.loads('{ "action": "none" }')

def process_with_natural_language_informal_talk(rec: str, chat):
    response_ia = chat.send_message(rec, safety_settings=safety_settings)
    return response_ia.text
