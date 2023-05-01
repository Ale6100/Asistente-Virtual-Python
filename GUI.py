import tkinter as tk
from tkinter import messagebox
import pkg_resources
import webbrowser
import scripts.direcciones_ as direcciones_
import subprocess
import threading

ventana_abierta = True

def leer_salida():
    while True:
        global proceso
        output = proceso.stdout.readline()
        if output == '' and proceso.poll() is not None:
            break
        if output:
            msg = output.strip()
            print(msg)
            
            if ventana_abierta is not True: break
            
            if "Detenido" in msg:
                start_button.config(state=tk.NORMAL)
                stop_button.config(state=tk.DISABLED)
                label.config(text='Presiona en "iniciar"')
            elif "Escuchando..." in msg:
                label.config(text='Escuchando...')
            elif 'Procesando...' in msg:
                label.config(text='Espere...')
            elif 'Internet no detectado. Reintentando...' in msg:
                label.config(text='Internet no detectado. Reintentando...')

def iniciar():
    label.config(text='Iniciando. Espere...')
    start_button.config(state=tk.DISABLED)
    stop_button.config(state=tk.NORMAL)
    global proceso
    proceso = subprocess.Popen(['pythonw', 'asistente_virtual.py', 'iniciado'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1, universal_newlines=True)
    thread = threading.Thread(target=leer_salida)
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
root.iconbitmap(pkg_resources.resource_filename(__name__, 'complementos/icon.ico'))

def cerrar():
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
