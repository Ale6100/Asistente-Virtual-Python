import tkinter as tk
from tkinter import messagebox
import webbrowser
import subprocess
import threading
import scripts.direcciones_ as direcciones_
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

name = config.get('Assistant', 'name', fallback='okay')

ventana_abierta = True # Es True si la interfaz gráfica de Tkinter se encuentra abierta

def leer_salida(): # Lee la salidas (los prints en este caso) del subproceso correspondiente al asistente virtual y actualiza la interfaz gráfica según el valor de los prints
    while True:
        output = proceso.stdout.readline() # Lee la línea de la salida del subproceso
        if output == '' and proceso.poll() is not None: break # Sale del bucle si output es una cadena vacía y si el subproceso ya no se está ejecutando
        
        if output:
            msg = output.strip() # Elimina espacios al inicio y al final de la cadena
            if not ventana_abierta: break # Si la ventana está cerrada, sale del bucle
            
            if "Detenido" in msg: # Actualiza la interfaz gráfica según el valor de los prints
                toggle_botones('asistente_detenido')
                label_iniciar.config(text='Presiona en "iniciar"')
            elif "Escuchando..." in msg:
                label_iniciar.config(text='Escuchando...')
            elif 'Procesando...' in msg:
                label_iniciar.config(text='Espere...')
            elif 'Internet no detectado. Reintentando...' in msg:
                label_iniciar.config(text='Internet no detectado. Reintentando...')

def iniciar(): # Inicia el subproceso correspondiente al asistente virtual
    label_iniciar.config(text='Iniciando. Espere...')
    toggle_botones('asistente_iniciado')
    global proceso
    proceso = subprocess.Popen(['pythonw', 'asistente_virtual.py', 'iniciado'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1, universal_newlines=True) # Ejecuta el subproceso en segundo plano
    thread = threading.Thread(target=leer_salida) # Crea un hilo para leer la salida del subproceso
    thread.start()

def detener(): # Detiene el subproceso correspondiente al asistente virtual
    if 'proceso' in globals():
        global proceso
        if proceso:
            proceso.terminate()
            toggle_botones('asistente_detenido')
            label_iniciar.config(text='Presiona en "Iniciar asistente"')

def cambiar_valor(clave: str, valor: str | int | float):
    config.set('Assistant', clave, valor)
    with open('config.ini', 'w') as f:
        config.write(f)    

def guardar_nombre():
    new_name = new_name_entry.get()
    if new_name != '' and all(letter in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ' for letter in new_name):
        cambiar_valor('name', new_name)
        new_name_entry['text'] = ''
        label_error['text'] = ''
        intro_label['text'] = f'Tu asistente se llama "{new_name}". Pídele algo'
        new_name_entry.delete(0, tk.END)
        set_msg_temp('Nombre modificado')
    else:
        label_error['text'] = 'Coloca un nombre válido'
        
def guardar_humor():
    new_humor = new_humor_entry.get()
    if new_humor != '' and all(letter in '1234567890' for letter in new_humor):
        cambiar_valor('humor', new_humor)
        new_humor_entry['text'] = ''
        label_error['text'] = ''
        new_humor_entry.delete(0, tk.END)
        set_msg_temp('Nivel de humor modificado')
    elif any(caracter in new_humor for caracter in ['%', '.', ',']):
        label_error['text'] = 'Coloca un valor válido. Debe ser un número entero sin porcentaje'
    else:
        label_error['text'] = 'Coloca un valor válido'

def toggle_botones(estado): # Activa o desactiva los botones, dependiendo si el asistente está activo o no
    if estado == 'asistente_iniciado':
        start_button.config(state=tk.DISABLED)
        stop_button.config(state=tk.NORMAL)
        save_name_button.config(state=tk.DISABLED)
        save_humor_button.config(state=tk.DISABLED)
    elif estado == 'asistente_detenido':
        start_button.config(state=tk.NORMAL)
        stop_button.config(state=tk.DISABLED)
        save_name_button.config(state=tk.NORMAL)
        save_humor_button.config(state=tk.NORMAL)

def set_msg_temp(msg): # Coloca un mensaje temporal 
    label_msg_temp['text'] = msg
    
    def reset_value():
        label_msg_temp['text'] = ''
    
    threading.Timer(5, lambda: reset_value()).start()

# Interfaz
root = tk.Tk()
root.title("Asistente Virtual")
root.geometry()
root.iconbitmap('complementos/icon.ico') 

def cerrar(): # Configurar la acción al cerrar la ventana
    if messagebox.askokcancel("Cerrar", "¿Quieres cerrar el asistente?"):
        detener()
        root.destroy()
        global ventana_abierta
        ventana_abierta = False

root.protocol("WM_DELETE_WINDOW", cerrar)

intro_label = tk.Label(root, text=f'Tu asistente se llama "{name}". Pídele algo')
intro_label.grid(row = 0, column = 0, columnspan = 6)

start_button = tk.Button(root, text="Iniciar asistente", command=iniciar)
start_button.grid(row = 1, column = 0, columnspan = 3)

stop_button = tk.Button(root, text="Detener asistente", command=detener, state=tk.DISABLED)
stop_button.grid(row = 1, column = 3, columnspan = 3)

label_msg_temp = tk.Label(root, text='')
label_msg_temp.grid(row = 2, column = 0, columnspan = 6)

label_iniciar = tk.Label(root, text='Presiona en "iniciar asistente"')
label_iniciar.grid(row = 3, column = 0, columnspan = 6)

label_error = tk.Label(root, text='', foreground='red')
label_error.grid(row = 4, column = 0, columnspan = 6)

new_name_label = tk.Label(root, text='Cambiar nombre a:')
new_name_label.grid(row = 5, column = 0, columnspan = 2)

new_name_entry = tk.Entry(root)
new_name_entry.grid(row = 5, column = 2, columnspan = 2)

save_name_button = tk.Button(root, text="Guardar", command=guardar_nombre)
save_name_button.grid(row = 5, column = 4, columnspan = 2)

new_humor_label = tk.Label(root, text='Cambiar humor a:')
new_humor_label.grid(row = 6, column = 0, columnspan = 2)

new_humor_entry = tk.Entry(root)
new_humor_entry.grid(row = 6, column = 2, columnspan = 2)

save_humor_button = tk.Button(root, text="Guardar", command=guardar_humor)
save_humor_button.grid(row = 6, column = 4, columnspan = 2)

help_button = tk.Button(root, text="Ayuda", command=lambda: webbrowser.open(direcciones_.direcciones["codigofuente"]["url"]))
help_button.grid(row = 7, column = 0, columnspan = 6)

root.mainloop()
