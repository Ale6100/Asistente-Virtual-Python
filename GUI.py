import tkinter as tk
from tkinter import messagebox
import pkg_resources
import webbrowser
import scripts.direcciones_ as direcciones_
import subprocess
import threading

ventana_abierta = True # Es True si la interfaz gráfica de Tkinter se encuentra abierta

def leer_salida(): # Lee la salidas (los prints en este caso) del subproceso correspondiente al asistente virtual
    while True:
        global proceso
        output = proceso.stdout.readline() # Lee la línea de la salida del subproceso
        if output == '' and proceso.poll() is not None: break # Sale del bucle si output es una cadena vacía y si el subproceso ya no se está ejecutando
        
        if output:
            msg = output.strip() # Elimina espacios al inicio y al final de la cadena           
            if ventana_abierta is not True: break # Si la ventana está cerrada sale del bucle
            
            if "Detenido" in msg: # Actualiza la etiqueta según el valor de los prints
                start_button.config(state=tk.NORMAL)
                stop_button.config(state=tk.DISABLED)
                label.config(text='Presiona en "iniciar"')
            elif "Escuchando..." in msg:
                label.config(text='Escuchando...')
            elif 'Procesando...' in msg:
                label.config(text='Espere...')
            elif 'Internet no detectado. Reintentando...' in msg:
                label.config(text='Internet no detectado. Reintentando...')

def iniciar(): # Inicia el subproceso correspondiente al asistente virtual
    label.config(text='Iniciando. Espere...')
    start_button.config(state=tk.DISABLED)
    stop_button.config(state=tk.NORMAL)
    global proceso
    proceso = subprocess.Popen(['pythonw', 'asistente_virtual.py', 'iniciado'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1, universal_newlines=True) # Ejecuta el subproceso en segundo plano
    thread = threading.Thread(target=leer_salida) # Crea un hilo para leer la salida del subproceso
    thread.start()

def detener():
    if 'proceso' in globals():
        global proceso
        if proceso:
            proceso.terminate()
            start_button.config(state=tk.NORMAL)
            stop_button.config(state=tk.DISABLED)
            label.config(text='Presiona en "iniciar"')

root = tk.Tk()
root.title("Asistente Virtual")
root.geometry("275x100")
root.iconbitmap(pkg_resources.resource_filename(__name__, 'complementos/icon.ico')) # Estoy consciente de que no era necesario usar pkg_resources para esto, pero lo dejo ya que me sirve si el .exe del asistente es un archivo único (por ahora no lo es)

def cerrar(): # Configurar la acción al cerrar la ventana
    global ventana_abierta
    if messagebox.askokcancel("Cerrar", "¿Quieres cerrar el asistente?"):
        detener()
        root.destroy()
        ventana_abierta = False

root.protocol("WM_DELETE_WINDOW", cerrar)

start_button = tk.Button(root, text="Iniciar asistente", command=iniciar)
start_button.pack()

stop_button = tk.Button(root, text="Detener asistente", command=detener, state=tk.DISABLED)
stop_button.pack()

open_button = tk.Button(root, text="Ayuda", command=lambda: webbrowser.open(f'{direcciones_.direcciones["ayuda"]["url"]}'))
open_button.pack()

label = tk.Label(root, text='Presiona en "iniciar"')
label.pack()

root.mainloop()
