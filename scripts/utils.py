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

asistente_virtual_name = importlib.util.resolve_name('asistente_virtual', package=None)
direcciones = direcciones_.direcciones

def eliminar_frases_introductorias(rec: str, array: list) -> str:
    frases_a_borrar = [ f'{frase} ' for frase in array ] # Agrega un espacio en cada frase
    frases_a_borrar_ordenadas = sorted(frases_a_borrar, key=lambda x: len(x), reverse=True) # Reordena según la longitud de caracteres, de mayor a menor
    frases_a_borrar_exp_reg = '|'.join(frases_a_borrar_ordenadas)  
    
    while re.match(fr'^({frases_a_borrar_exp_reg})', rec):
        for frase in frases_a_borrar_ordenadas:
            if rec[:len(frase)] == frase:
                rec = rec[len(frase):]
                break        
    return rec

def eliminar_frases_finales(rec: str) -> str:
    frases_a_borrar = ['por favor', 'gracias', 'muchas gracias', 'muchisimas gracias']
    frases_a_borrar_ordenadas = sorted(frases_a_borrar, key=lambda x: len(x), reverse=True)
    frases_a_borrar_exp_reg = '|'.join(frases_a_borrar_ordenadas)
    while re.search(fr'{frases_a_borrar_exp_reg}$', rec):
        for frase in frases_a_borrar_ordenadas:
            if rec[-len(frase):] == frase:
                rec = rec[:-len(frase)-1]
                break
    return rec

def buscar(rec: str) -> bool:
    if "en " not in rec: return False
    frases_a_buscar = ['buscame', 'buscar', 'buscas', 'busca', 'buscarias', 'buscador']
    frases_a_buscar_ordenadas = sorted(frases_a_buscar, key=lambda x: len(x), reverse=True)
    
    rec = rec # Defino un rec local para no modificar al original por si esta función llega a retornar False
    
    if any(word in rec for word in frases_a_buscar_ordenadas): # En caso de que el usuario diga alguna de las palabras de "frases_a_buscar", elimina de rec todo lo que haya dicho antes de eso
        for frase in frases_a_buscar_ordenadas:
            if frase in rec:
                posicion_inicio_frase = rec.find(f'{frase}') # Busca la posición donde inicia el nombre del asistente
                rec = rec[posicion_inicio_frase:]
                break
    
    rec = eliminar_frases_introductorias(rec, ['buscame', 'buscar', 'buscas', 'busca', 'a', 'al', 'buscarias', 'buscador'])
    #! okay puedes buscar netflix en windows por favor sí dale haceme ese favor
    
    if "en windows" in rec:
        indexPalClave = rec.find(f'en windows')
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
    for palClave in array_palClave: # Elimina todas las "palClave" al final del pedido y "en" (a esta altura, si rec="Buscar oso en google", ahora rec="oso")
        if f'en {palClave.lower()}' in rec:
            sitio = palClave
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
    
    numeros, palabras, contador = '123456789', ['uno', 'dos', 'tres', 'cuatro', 'cinco', 'seis', 'siete', 'ocho', 'nueve'], 0
    for i in range(9):
        if numeros[i] in rec or palabras[i] in rec:
            print_and_talk(f'Abriendo atajo {numeros[i]}')
            pyautogui.hotkey('win', numeros[i])
            break
        contador += 1    
    if contador == 9:
        print_and_talk('Los atajos son números del 1 al 9')

def abrir(rec: str, print_and_talk):
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
                if "http" in direcciones[dir]['url']:
                    webbrowser.open(f'{direcciones[dir]["url"]}')
                elif direcciones[dir]['url'].startswith('C:'):
                    os.startfile(f'{direcciones[dir]["url"]}')
                    
                    if sitio in ['canciones', 'musica']:
                        pyautogui.press('volumedown', 50)
                        pyautogui.press('volumeup', 10)
                    
                else:
                    os.startfile(pkg_resources.resource_filename(asistente_virtual_name, f'/{direcciones[dir]["url"]}'))
                return print_and_talk("Hecho") 
    print_and_talk("El sitio no está registrado o no se entendió el pedido") 


def volumen_al(rec, print_and_talk):
    rec = rec.replace('%', '')
    for i in range(100, -1, -1):
        if str(i) in rec:
            pyautogui.press('volumedown', 50)
            pyautogui.press('volumeup', round(i/2))
            print_and_talk(f'Volumen al {2*round(i/2)} por ciento') # Lo hago así sabiendo que el resultado siempre será par, ya que los botones mueven el valor de volumen de a pares
            break

def cronometro(rec: str, cronometro: int, print_and_talk):
    if 'inicia' in rec or 'comenza' in rec or 'comienza' in rec:
        print_and_talk('Iniciando cronómetro')
        cronometro = time.time() # Registra el tiempo actual
    else: # Cuando se detiene averigua cuánto tiempo pasó
        if cronometro == 0:
            print_and_talk('No puedes detener un cronómetro que no ha sido iniciado')
        else:
            tiempo_pasado = round(time.time() - cronometro)
            
            horas_sr = tiempo_pasado/60/60
            horas = int(np.floor(horas_sr))

            minutos_sr = (horas_sr - horas)*60
            minutos = int(np.floor(minutos_sr))

            segundos_sr = (minutos_sr - minutos)*60
            segundos = int(np.round(segundos_sr))

            horas_ = f'{horas}' if horas > 9 else f'0{horas}'
            minutos_ = f'{minutos}' if minutos > 9 else f'0{minutos}'
            segundos_ = f'{segundos}' if segundos > 9 else f'0{segundos}'
            print_and_talk(f'Pasaron {horas_}:{minutos_}:{segundos_}')
            cronometro = 0
    return cronometro
    