import configparser
import tkinter as tk
from tkinter import messagebox
import subprocess
import threading
import webbrowser
import scripts.direcciones_ as direcciones_

class AssistantGUI:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        self.name = self.config.get('Assistant', 'name', fallback='okay')
        self.ventana_abierta = True # Es True si la interfaz gráfica de Tkinter se encuentra abierta
        self.proceso = None
        self.create_gui()

    def create_gui(self):
        self.root = tk.Tk()
        self.root.title("Asistente Virtual")
        self.root.iconbitmap('complementos/icon.ico')

        self.root.protocol("WM_DELETE_WINDOW", self.cerrar)

        self.intro_label = tk.Label(self.root, text=f'Tu asistente se llama "{self.name}". Pídele algo')
        self.intro_label.grid(row = 0, column = 0, columnspan = 6)

        self.start_button = tk.Button(self.root, text="Iniciar asistente", command=self.iniciar)
        self.start_button.grid(row= 1, column = 0, columnspan = 3)

        self.stop_button = tk.Button(self.root, text="Detener asistente", command=self.detener, state=tk.DISABLED)
        self.stop_button.grid(row= 1, column = 3, columnspan = 3)

        self.label_msg_temp = tk.Label(self.root, text='')
        self.label_msg_temp.grid(row= 2, column = 0, columnspan = 6)

        self.label_iniciar = tk.Label(self.root, text='Presiona en "Iniciar asistente"')
        self.label_iniciar.grid(row= 3, column = 0, columnspan = 6)

        self.label_error = tk.Label(self.root, text='', foreground='red')
        self.label_error.grid(row= 4, column = 0, columnspan = 6)

        self.new_name_label = tk.Label(self.root, text='Cambiar nombre a:')
        self.new_name_label.grid(row= 5, column = 0, columnspan = 2)

        self.new_name_entry = tk.Entry(self.root)
        self.new_name_entry.grid(row= 5, column = 2, columnspan = 2)

        self.save_name_button = tk.Button(self.root, text="Guardar", command=self.guardar_nombre)
        self.save_name_button.grid(row= 5, column = 4, columnspan = 2)

        self.new_humor_label = tk.Label(self.root, text='Cambiar humor a:')
        self.new_humor_label.grid(row= 6, column = 0, columnspan = 2)

        self.new_humor_entry = tk.Entry(self.root)
        self.new_humor_entry.grid(row= 6, column = 2, columnspan = 2)

        self.save_humor_button = tk.Button(self.root, text="Guardar", command=self.guardar_humor)
        self.save_humor_button.grid(row= 6, column = 4, columnspan = 2)

        self.help_button = tk.Button(self.root, text="Ayuda", command=lambda: webbrowser.open(direcciones_.direcciones["codigofuente"]["url"]))
        self.help_button.grid(row= 7, column = 0, columnspan = 6)

        self.root.mainloop()

    def cerrar(self): # Configurar la acción al cerrar la ventana
        if messagebox.askokcancel("Cerrar", "¿Quieres cerrar el asistente?"):
            self.detener()
            self.root.destroy()
            self.ventana_abierta = False

    def leer_salida(self): # Lee la salidas (los prints en este caso) del subproceso correspondiente al asistente virtual y actualiza la interfaz gráfica según el valor de los prints
        while True:
            output = self.proceso.stdout.readline() # Lee la línea de la salida del subproceso
            if output == '' and self.proceso.poll() is not None: # Sale del bucle si output es una cadena vacía y si el subproceso ya no se está ejecutando
                break

            if output:
                msg = output.strip() # Elimina espacios al inicio y al final de la cadena
                if not self.ventana_abierta: # Si la ventana está cerrada, sale del bucle
                    break

                if "Detenido" in msg: # Actualiza la interfaz gráfica según el valor de los prints
                    self.toggle_botones('asistente_detenido')
                    self.label_iniciar.config(text='Presiona en "iniciar"')
                elif "Escuchando..." in msg:
                    self.label_iniciar.config(text='Escuchando...')
                elif 'Procesando...' in msg:
                    self.label_iniciar.config(text='Espere...')
                elif 'Internet no detectado. Reintentando...' in msg:
                    self.label_iniciar.config(text='Internet no detectado. Reintentando...')

    def iniciar(self): # Inicia el subproceso correspondiente al asistente virtual
        self.label_iniciar.config(text='Iniciando. Espere...')
        self.toggle_botones('asistente_iniciado')
        try:
            self.proceso = subprocess.Popen(['.venv\\Scripts\\pythonw', 'asistente_virtual.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1, universal_newlines=True)
        except:
            self.proceso = subprocess.Popen(['pythonw', 'asistente_virtual.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1, universal_newlines=True)
        thread = threading.Thread(target=self.leer_salida) # Crea un hilo para leer la salida del subproceso
        thread.start()

    def detener(self): # Detiene el subproceso correspondiente al asistente virtual
        if self.proceso:
            self.proceso.terminate()
            self.toggle_botones('asistente_detenido')
            self.label_iniciar.config(text='Presiona en "Iniciar asistente"')

    def cambiar_valor(self, clave: str, valor: str | int | float):
        self.config.set('Assistant', clave, valor)
        with open('config.ini', 'w') as f:
            self.config.write(f)

    def guardar_nombre(self):
        new_name = self.new_name_entry.get()
        if new_name != '' and all(letter.isalpha() for letter in new_name):
            self.cambiar_valor('name', new_name)
            self.new_name_entry['text'] = ''
            self.label_error['text'] = ''
            self.intro_label['text'] = f'Tu asistente se llama "{new_name}". Pídele algo'
            self.new_name_entry.delete(0, tk.END)
            self.set_msg_temp('Nombre modificado')
        else:
            self.label_error['text'] = 'Coloca un nombre válido'

    def guardar_humor(self):
        new_humor = self.new_humor_entry.get()
        if new_humor != '' and new_humor.isnumeric():
            self.cambiar_valor('humor', new_humor)
            self.new_humor_entry['text'] = ''
            self.label_error['text'] = ''            
            self.new_humor_entry.delete(0, tk.END)
            self.set_msg_temp(f'Nivel de humor al {new_humor}%')
        else:
            self.label_error['text'] = 'Coloca un valor válido'

    def toggle_botones(self, estado): # Activa o desactiva los botones, dependiendo si el asistente está activo o no
        if estado == 'asistente_iniciado':
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.save_name_button.config(state=tk.DISABLED)
            self.save_humor_button.config(state=tk.DISABLED)
        elif estado == 'asistente_detenido':
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            self.save_name_button.config(state=tk.NORMAL)
            self.save_humor_button.config(state=tk.NORMAL)

    def set_msg_temp(self, msg): # Coloca un mensaje temporal
        self.label_msg_temp['text'] = msg

        def reset_value():
            self.label_msg_temp['text'] = ''

        threading.Timer(5, lambda: reset_value()).start()

if __name__ == "__main__":
    app = AssistantGUI()
