import configparser
import tkinter as tk
from tkinter import messagebox
import threading
import webbrowser
import scripts.addresses as addresses
from multiprocessing import Queue
from scripts.asistente_virtual import AssistantApp
import os
import signal

class AssistantGui:
    CONFIG_FILE = 'config.ini'
    CONFIG_SECTION = 'Assistant'

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read(self.CONFIG_FILE)
        self.name = self.config.get(self.CONFIG_SECTION, 'name', fallback='okay')
        self.q = Queue()
        self.stop_event = None
        self.window_open = True
        self.informal_chat = self.config.getint(self.CONFIG_SECTION, 'informal_chat', fallback=0)
        self.create_gui()

    def create_gui(self):
        self.root = tk.Tk()
        self.root.title("Asistente Virtual")
        self.root.iconbitmap('complementos/icon.ico')

        self.root.protocol("WM_DELETE_WINDOW", self.close_window)

        self.intro_label = tk.Label(self.root, text=f'El asistente se llama "{self.name}". Modo informal' if self.informal_chat else f'Tu asistente se llama "{self.name}". Pídele algo')
        self.intro_label.grid(row = 0, column = 0, columnspan = 6, pady=5)
        self.intro_label.config(font=(None, 9, 'bold'))

        self.start_button = tk.Button(self.root, text="Iniciar asistente", command=self.start)
        self.start_button.grid(row= 1, column = 0, columnspan = 3)

        self.stop_button = tk.Button(self.root, text="Detener asistente", command=self.stop, state=tk.DISABLED)
        self.stop_button.grid(row= 1, column = 3, columnspan = 3)

        self.label_msg_temp = tk.Label(self.root, text='')
        self.label_msg_temp.grid(row= 2, column = 0, columnspan = 6)

        self.label_start = tk.Label(self.root, text='Presiona en "Iniciar asistente"')
        self.label_start.grid(row= 3, column = 0, columnspan = 6)

        self.label_error = tk.Label(self.root, text='', foreground='red')
        self.label_error.grid(row= 4, column = 0, columnspan = 6)

        self.new_name_label = tk.Label(self.root, text='Cambiar nombre a:')
        self.new_name_label.grid(row= 5, column = 0, columnspan = 2)

        self.new_name_entry = tk.Entry(self.root)
        self.new_name_entry.grid(row= 5, column = 2, columnspan = 2)

        self.save_name_button = tk.Button(self.root, text="Guardar", command=self.save_name)
        self.save_name_button.grid(row= 5, column = 4, columnspan = 2)

        self.new_humor_label = tk.Label(self.root, text='Cambiar humor a:')
        self.new_humor_label.grid(row= 6, column = 0, columnspan = 2)

        self.new_humor_entry = tk.Entry(self.root)
        self.new_humor_entry.grid(row= 6, column = 2, columnspan = 2)

        self.save_humor_button = tk.Button(self.root, text="Guardar", command=self.save_humor)
        self.save_humor_button.grid(row= 6, column = 4, columnspan = 2)

        self.change_informal_mode_button = tk.Button(self.root, text="Desactivar modo informal" if self.informal_chat else "Activar modo informal", command=self.change_informal_mode, bg='orange' if self.informal_chat else 'white')
        self.change_informal_mode_button.grid(row= 7, column = 1, columnspan = 3)

        self.help_button = tk.Button(self.root, text="Ayuda", command=lambda: webbrowser.open(addresses.addresses["sourcecode"]["url"]))
        self.help_button.grid(row= 7, column = 4, columnspan = 3)

        self.root.mainloop()

    def start(self): # Inicia los hilos correspondientes al asistente virtual y al lector de mensajes
        self.label_start.config(text='Iniciando. Espere...')
        self.toggle_buttons('asistente_iniciado')

        self.stop_event = threading.Event()

        threading.Thread(target=AssistantApp, args=(self.q, self.stop_event)).start() # En self.stop_event se almacena una señal que le dice a ambos hilos cuándo deben detenerse
        threading.Thread(target=self.read_output).start()

    def read_output(self): # Lee los mensajes enviados por el hilo correspondiente al asistente virtual y actualiza la interfaz gráfica según los valores
        while True: # Podría poner la condición "not self.stop_event.is_set()", pero como el cierre no es inmediato, cuando esa condición se cumple en realidad todavía puede haber algún último mensaje que falte enviar
            msg = self.q.get().strip()
            if not self.window_open: break # Recordemos que el código se para hasta que se recibe un mensaje desde el get(), por eso el condicional está acá y no en el del propio while

            if "Detenido" in msg:
                self.toggle_buttons('asistente_detenido')
                self.label_start.config(text='Presiona en "Iniciar asistente"')
                self.label_msg_temp['text'] = ''
                break
            elif "Escuchando..." in msg:
                self.label_start.config(text='Escuchando...')
            elif 'Procesando...' in msg:
                self.label_start.config(text='Espere...')
            elif 'Internet no detectado. Reintentando...' in msg:
                self.label_start.config(text='Internet no detectado. Reintentando...')

    def stop(self): # Envía una señal al hilo del asistente virtual para que se pare cuando pueda (no es automático ya que no se recomienda forzarlo)
        if self.stop_event is not None and not self.stop_event.is_set():
            self.stop_event.set()
            self.stop_button.config(state=tk.DISABLED)
            self.label_msg_temp['text'] = 'Escuchando por última vez y deteniendo...'

    def close_window(self): # Configurar la acción al cerrar la ventana
        if messagebox.askokcancel("Cerrar", "¿Quieres cerrar el asistente?"):
            self.stop()
            self.window_open = False
            self.root.destroy()
            os.kill(os.getpid(), signal.SIGTERM)

    #? ----- métodos auxiliares -----

    def change_value(self, clave: str, valor: str):
        self.config.set(self.CONFIG_SECTION, clave, valor)
        with open(self.CONFIG_FILE, 'w') as f:
            self.config.write(f)

    def save_name(self):
        new_name = self.new_name_entry.get()
        if new_name != '' and all(letter.isalpha() for letter in new_name):
            self.change_value('name', new_name)
            self.new_name_entry['text'] = ''
            self.label_error['text'] = ''
            self.intro_label['text'] = f'Tu asistente se llama "{new_name}". Pídele algo'
            self.new_name_entry.delete(0, tk.END)
            self.set_msg_temp('Nombre modificado')
        else:
            self.label_error['text'] = 'Coloca un nombre válido'

    def save_humor(self):
        new_humor = self.new_humor_entry.get().strip()
        if new_humor == '' or not new_humor.isnumeric():
            self.label_error['text'] = 'Coloca un valor válido'
        elif int(new_humor) < 0 or int(new_humor) > 100:
            self.label_error['text'] = 'El nivel de humor debe estar entre 0 y 100'
        else:
            self.change_value('humor', new_humor)
            self.new_humor_entry['text'] = ''
            self.label_error['text'] = ''
            self.new_humor_entry.delete(0, tk.END)
            self.set_msg_temp(f'Nivel de humor al {new_humor}%')

    def set_msg_temp(self, msg): # Coloca un mensaje temporal
        self.label_msg_temp['text'] = msg

        def reset_value():
            self.label_msg_temp['text'] = ''

        threading.Timer(5, lambda: reset_value()).start()

    def toggle_buttons(self, estado): # Activa o desactiva los botones, dependiendo si el asistente está activo o no
        if estado == 'asistente_iniciado':
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.save_name_button.config(state=tk.DISABLED)
            self.save_humor_button.config(state=tk.DISABLED)
            self.change_informal_mode_button.config(state=tk.DISABLED)
        elif estado == 'asistente_detenido':
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            self.save_name_button.config(state=tk.NORMAL)
            self.save_humor_button.config(state=tk.NORMAL)
            self.change_informal_mode_button.config(state=tk.NORMAL)

    def change_informal_mode(self):
        if self.informal_chat:
            self.informal_chat = 0
            self.intro_label['text'] = f'Tu asistente se llama "{self.name}". Pídele algo'
            self.change_informal_mode_button['text'] = 'Activar modo informal'
            self.change_informal_mode_button.config(bg='white')
        else:
            self.informal_chat = 1
            self.intro_label['text'] = f'Tu asistente se llama "{self.name}". Modo informal'
            self.change_informal_mode_button['text'] = 'Desactivar modo informal'
            self.change_informal_mode_button.config(bg='orange')

        self.change_value('informal_chat', str(self.informal_chat))

if __name__ == "__main__":
    app = AssistantGui()
