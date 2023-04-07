import re
import webbrowser
import direcciones_
import pyautogui
import time
import wikipedia

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
    frases_a_borrar = [ f' {frase}' for frase in frases_a_borrar ]
    frases_a_borrar_ordenadas = sorted(frases_a_borrar, key=lambda x: len(x), reverse=True)
    frases_a_borrar_exp_reg = '|'.join(frases_a_borrar_ordenadas)
    
    while re.search(fr'{frases_a_borrar_exp_reg}$', rec):
        for frase in frases_a_borrar_ordenadas:
            if rec[-len(frase):] == frase:
                rec = rec[:-len(frase)]
                break
    return rec

def buscar(rec: str) -> bool:
    rec = eliminar_frases_introductorias(rec, ['buscame', 'buscar', 'buscas', 'busca', 'a', 'al', 'buscarias'])

    if "windows" == rec[-len("windows"):]:
        rec = rec[:-len("windows")-4]
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
        if palClave.lower() == rec[-len(palClave):]:
            sitio = palClave
            rec = rec[:-len(palClave)-4]
            break

    if sitio == "": return False # Si ningún sitio fue solicitado en el pedido, se da por hecho que el usuario no quiere buscar nada y termina la función
    
    for dir in direcciones: # Crea un array con todas las palabras clave del diccionario "direcciones"
        if 'buscador' in direcciones[dir]:
            if sitio in direcciones[dir]['palClave']:
                webbrowser.open(f'{direcciones[dir]["buscador"]}{rec}')
    return True
