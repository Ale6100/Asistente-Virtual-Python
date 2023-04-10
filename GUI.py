import tkinter as tk
from asistente_virtual import iniciar
import threading
from queue import Queue
import pkg_resources
import webbrowser
import scripts.direcciones_ as direcciones_

def update_gui(q):
    while True:
        msg = q.get()
        
        print(msg)

        if msg == "Detenido":
            start_button.config(state=tk.NORMAL)
            stop_button.config(state=tk.DISABLED)
            label.config(text='Presiona en "iniciar"')
        elif msg == "Encendido":
            start_button.config(state=tk.DISABLED)
            stop_button.config(state=tk.NORMAL)
        elif msg == "Escuchando...":
            label.config(text=f'{msg}')
        elif msg == 'Espere...':
            label.config(text=f'{msg}')

def start_():
    global stop_event
    stop_event = threading.Event()
    q = Queue()
    t = threading.Thread(target=iniciar, args=(q, stop_event))
    t.start()

    t_gui = threading.Thread(target=update_gui, args=(q,))
    t_gui.start()

def stop_():
    global stop_event
    stop_event.set()

root = tk.Tk()
root.title("Asistente Virtual")
root.geometry("275x100")
root.iconbitmap(pkg_resources.resource_filename(__name__, 'complementos/z_robot.ico'))

start_button = tk.Button(root, text="Iniciar Asistente", command=start_)
start_button.pack()

stop_button = tk.Button(root, text="Detener Asistente", command=stop_, state=tk.DISABLED)
stop_button.pack()

open_button = tk.Button(root, text="Ayuda", command=lambda: webbrowser.open(f'{direcciones_.direcciones["ayuda"]["url"]}'))
open_button.pack()

label = tk.Label(root, text='Presiona en "iniciar"')
label.pack()

root.mainloop()
