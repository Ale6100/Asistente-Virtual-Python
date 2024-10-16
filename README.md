# Asistente virtual con Python

> Ahora impulsado con IA!

Bienvenido! este es mi primer asistente creado con Python. Hace un tiempo hice uno con JavaScript [aquí](https://github.com/Ale6100/Asistente-Virtual-JS.git) pero por las limitaciones de ese lenguaje no pude explotar su potencial.

Mi objetivo con este proyecto es lograr que el asistente sea lo suficientemente útil como para que desees utilizarlo a diaro, sabiendo que lo puedes dejar encendido en segundo plano para que esté listo en cualquier momento que lo necesites.

`Nota 1`: Esto no es un Chat GPT con audio. La filosofía de este proyecto que inició en el 2020 es que el asistente pueda acatar pedidos de manera interactiva en tu computadora. Para más detalle ve la tabla que está más abajo.

`Nota 2`: El asistente ha sido testeado en un entorno con Windows 11 de 64 bits, no puedo garantizar su correcto funcionamiento en otros casos.

## Guía para usuarios 🧑‍💻

### Descarga ⬇️

Si deseas obtener una copia local del asistente listo para usar, haz click [aquí](https://github.com/Ale6100/Asistente-Virtual-Python/raw/main/Asistente_virtual.rar). Te descargará una capreta comprimida en formato `.rar` llamada "Asistente_virtual" que tendrás que descomprimir.

_Recuerda volver aquí de vez en cuando para asegurarte de tener siempre la última versión!_

### Uso 📝

1. Abre el archivo ejecutable Asistente_virtual dentro de la carpeta con su mismo nombre

2. Si es la primera vez que lo abres tendrás que obtener tu Api Key gratuita de Groq e ingresarla en el campo correspondiente. Consíguela [aquí](https://console.groq.com/keys). Esta Api Key le proporciona al asistente virtual una inteligencia artificial. Anteriormente no era necesaria pero decidí implementarla para mejorar la experiencia del usuario.

3. Presiona el botón `Iniciar asistente`

4. Notarás que hay un texto que alterna entre los valores:
    * Iniciando. Espere...
    * Espere...
    * Escuchando...

    Asegúrate de hablar siempre que esté presente el tercer valor, de lo contrario no podrá escucharte

5. Hazle un pedido! Considera que:

    * Todas los pedidos deben iniciar con el nombre del asistente. Por defecto se llama "Okay" por simplicidad (puedes decir "Okey" también, ya que lo interpreta como "Okay"). Por ejemplo: `Okay, abrir Twitter`

    * Con un botón en la interfaz puedes activar y desactivar el **Modo conversacional** (de manera predeterminada viene desactivado), donde el asistente no acatará pedidos, si no que simplemente conversará sobre los temas que desees. Cuando hablas con este modo también es necesario iniciar con el nombre del asistente. Este botón estará habilitado únicamente cuando el asistente esté detenido.

    * Con otro botón puedes activar y desactivar el **Modo discreto** (de manera predeterminada viene desactivado), donde el asistente no te responderá con voz, estará silenciado. Este botón estará habilitado únicamente cuando el asistente esté iniciado.

    * Pedido encapsulado: Para mejorar el entendimiento, opcionalmente puedes decir su nombre por segunda vez en un mismo pedido. En este caso, el asistente interpretará que el pedido está entre la primera y la segunda vez que lo nombraste. Por ejemplo, si dices `bla bla bla Okay, abrir Twitter Okay bla bla bla`, el pedido será `abrir Twitter`

    * Te responde "no te entendí" cuando entendió mal o hiciste un pedido que no está dentro de los disponibles

    * Todas las palabras clave tienen variantes (por ejemplo en vez de decir "abre" se puede decir "abrís")

    * Algunos pedidos requieren condiciones muy específicas para funcionar correctamente, las cuales se detallan en la siguiente tabla. Considera además que, en general, aquellos ubicados en la parte superior tienen mayor prioridad que los situados más abajo.

| Palabras clave | Descripción | Ejemplo | Condición
| :--- | :--- | :--- | :---
| `basta` | Apaga al asistente | Okay, basta | La palabra `basta` debe decirse al final
| `cancelar` | Cancela el pedido que estás solicitando | Okay, abrir YouTube. No, cancelar | La palabra `cancelar` debe decirse al final
| `cerrar` ... `archivo` | Cierra el programa actual | Okay, cerrar archivo | ---
| `tecla` X | Presiona la tecla solicitada | Okay, presioná la tecla P | Debe decirse al final del pedido
| `alarma en` n `minutos` | Programa una alarma para dentro de n minutos | Okay, activá la alarma en 5 minutos | la palabra `alarma` debe decirse justo antes del `en`
| `buscar` X `en` Y | Busca en el sitio Y lo que le pediste (X) | Okay, buscar "Mercado Libre" en Linkedin | Sólo funciona en sitios preconfigurados
| `en` n `minutos` | Programa la ejecución de otro pedido para dentro de n minutos | Okay, abrir Netflix en tres minutos | "n" debe ser un número natural
| `hora` | Consultar la hora | Okay, decime qué hora es | ---
| `fecha` | Consultar la fecha | Okay, ¿qué fecha es hoy? | ---
| `atajo` n | Abre el n-ésimo programa disponible de la barra de tareas | Okay, atajo 1 | `n` debe ser un número natural entre 1 y 9. No lo abrirá si no lo tenés disponible
| `abre` X | Abre el sitio X | Okay, abre Twitter | Sólo funciona en sitios preconfigurados
| `reproduce musica` | Setea el volumen al 20% y abre una lista de reproducción | Okay, reproduce música | La lista de reproducción debe estar en C:/Users/{usuario}/Music/av/musica.xspf
| `mute` | Activa/desactiva el mute | Okay, mute | ---
| `minimizar` | Minimiza el programa actual | Okay, minimizar | ---
| `minimizar todo` | Minimiza todos los programas | Okay, minimizar todo | ---
| `volumen`...`%` | Cambia el volumen de la computadora | Okay, volumen al 20% | Sólo coloca valores pares
| `chiste` | Te dice un chiste único | Okay, decime un chiste | ---
| `cómo te llamás` | Te dice su nombre | Okay, ¿Cómo te llamás? | ---
| `captura de pantalla` | Hace una captura de pantalla | Okay, sacá una captura de pantalla | Guarda la captura en la carpeta `screenshots` ubicada donde está el asistente
| `iniciá` / `detené` el `cronómetro` | Inicia o detiene un cronómetro | Okay, iniciá el cronómetro | ---
| `nivel de humor` | Consulta el porcentaje de "humor" (5% por defecto) | Okay, decime tu nivel de humor | ---
| `humor`...`X%` | Cambia el nivel de humor al n%, siendo n un número entero entre 0 y 100 | Okay, nivel de humor al 10% | ---
| `ayuda` | Te redirige a este readme para entender mejor al asistente | Okay, necesito ayuda | ---
| `ver código fuente` | Te redirige al código fuente del asistente | Okay, ver código fuente | ---
| `temperatura` | Busca en google la info pedida sobre el clima | Okay, temperatura del fin de semana | ---

Tiene varios activadores más pero sólo sirven para aumentar la interactividad

También es posible hacerle varios pedidos al mismo tiempo!

### Limitaciones 🚨

1. Está hecho para ser utilizado en windows

2. A la hora de hacer un pedido debes ser claro y conciso, sin pausas

3. Se necesita conexión activa a internet para que funcione el reconocedor de voz y la IA. En caso de que se desconecte, tratará de reconectarse un par de veces

4. Si suspendés la computadora y la volvés a encender, el asistente dejará de funcionar como máximo 60 segudos, luego volverá a estar disponible

5. Dado que utilizo Llama 3 (una IA no muy avanzada), es natural que de vez en cuando no funcione como debería, incluso a veces puede inventarse datos. Sus memorias se reinician cada 100 escuchas para minimizar el margen de error, y la mayoría de las veces que se detectan respuestas inesperadas.

## Guía para programadores 👨‍💻

### Pre-requisitos 📋

El código está hecho y testeado utilizando la versión 3.12.5 de Python y un Windows 11 de 64bits.

### Descarga el código ⬇️

Si deseas obtener una copia local, descarga el archivo comprimido .zip desde el botón verde "code" o haz click [aquí](https://github.com/Ale6100/Asistente-Virtual-Python/archive/refs/heads/main.zip)

### Instalación 🔧 (en windows)

Primero debes crear un entorno virtual con el comando

```bash
py -3 -m venv .venv
```

luego actívalo con el comando

```bash
.venv\Scripts\activate
```

A continuación, instala las dependencias con el comando

```bash
pip install -r requirements.txt
```

**Recuerda que debes activar el entorno virtual siempre que desees usarlo**

### Modificación 🛠️

Si deseas modificar al asistente, considera que:

* Los archivos relevantes a tener en cuenta en todo momento son:
  * Carpetas `dist` y `.venv` - Archivos compilados y entorno virtual. No las subo a GitHub porque te debes crear las tuyas.
  * [GUI.py](GUI.py) - Interfaz gráfica. Este es el archivo central, el que debe ser ejecutado para inicializar la aplicación
  * [/scripts/asistente_virtual.py](./scripts/asistente_virtual.py) - Lógica gruesa del asistente
  * Carpeta [scripts](./scripts) - Archivos python de apoyo
  * Carpeta [complementos](./complementos) - Recursos complementarios
  * [config.ini](./config.ini) - Archivo donde guardo configuración dinámica y persistente del asistente
  * [scripts/train_ai.py](./scripts/train_ai.py) - Aquí entreno a la IA para que entienda la estructura de la mayoría de los pedidos

* Una vez que estés conforme con tus cambios, coloca en la terminal el comando:

```bash
pyinstaller --noconsole --name "Asistente_virtual" --icon=complementos/icon.ico --contents-directory . --add-data "complementos;complementos" --add-data "scripts;scripts" --add-data "config.ini;." GUI.py
```

para compilar el proyecto en la carpeta dist. Asegúrate de haber eliminado (o vaciado) la carpeta dist antes de compilar para evitar errores imprevistos. Luego abre el archivo Asistente_virtual.exe ubicado en `dist/Asistente_virtual` y utiliza tu versión modificada!

### Despliegue 📦

Podrás iniciar el asistente ejecutando [GUI.py](GUI.py) o abriendo el archivo compilado [dist/Asistente_virtual/Asistente_virtual.exe](/dist/Asistente_virtual/Asistente_virtual.exe) en caso de que lo tengas creado

## Autor ✒️

| ![Alejandro Portaluppi](https://avatars.githubusercontent.com/u/107259761?size=50)
|:-:
| **Alejandro Portaluppi**
|[![GitHub](https://img.shields.io/badge/github-%23121011.svg?&style=for-the-badge&logo=github&logoColor=white)](https://github.com/Ale6100) [![LinkedIn](https://img.shields.io/badge/linkedin%20-%230077B5.svg?&style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/alejandro-portaluppi)
