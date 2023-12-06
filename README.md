# Asistente virtual con Python
Bienvenido! este es mi primer asistente creado con Python. Hace un tiempo hice uno con JavaScript (https://github.com/Ale6100/Asistente-Virtual-JS.git) pero por las limitaciones de ese lenguaje no pude explotar su potencial.

Mi objetivo con este proyecto es lograr que el asistente sea lo suficientemente útil como para que desees utilizarlo a diaro, sabiendo que lo puedes dejar encendido en segundo plano para que esté listo en cualquier momento que lo necesites.

`Importante`: El asistente ha sido testeado en un entorno con Windows 11 de 64 bits, no puedo garantizar su correcto funcionamiento en otros casos.

## Guía para usuarios 🧑‍💻
### Descarga ⬇️
Si deseas obtener una copia local del asistente listo para usar, haz click [aquí](https://github.com/Ale6100/Asistente-Virtual-Python/raw/main/Asistente_virtual.rar). Te descargará una capreta comprimida en formato `.rar` llamada "Asistente_virtual" que tendrás que descomprimir.

_Recuerda volver aquí de vez en cuando para asegurarte de tener siempre la última versión!_

### Uso 📝
1. Abre el archivo ejecutable Asistente_virtual dentro de la carpeta con su mismo nombre

2. Presiona el botón `Iniciar asistente`

3. Notarás que mientras está iniciado hay un texto que alterna entre los valores:
    * Iniciando. Espere...
    * Espere...
    * Escuchando...

    Asegúrate de hablar siempre que esté presente el tercer valor, de lo contrario no podrá escucharte

4. Hazle un pedido! Considera que:

    * Todas los pedidos deben iniciar con el nombre del asistente. Por defecto se llama "Okay" por simplicidad (puedes decir "Okey" también, ya que lo interpreta como "Okay"). Por ejemplo: `Okay, abrir Twitter`

    * Pedido encapsulado: Para mejorar el entendimiento, opcionalmente puedes decir su nombre por segunda vez en un mismo pedido. En este caso, el asistente interpretará que el pedido está en medio de la primera y la segunda vez que lo nombraste. Por ejemplo, si dices `bla bla bla Okay, abrir Twitter Okay bla bla bla`, el pedido será `abrir Twitter`

    * Te responde "no te entendí" cuando entendió mal o hiciste un pedido que no está dentro de los disponibles

    * Todas las palabras clave tienen variantes (por ejemplo en vez de decir "abre" se puede decir "abrís")

    * Algunos pedidos requieren condiciones muy específicas para funcionar correctamente, las cuales se detallan en la siguiente tabla. Considera además que, en general, aquellos ubicados en la parte superior tienen mayor prioridad que los situados más abajo.

| Palabras clave | Descripción | Ejemplo | Condición
| :--- | :--- | :--- | :--- |
| `basta` | Apaga al asistente | Okay, basta | --- |
| `cancelar` | Cancela el pedido que estás solicitando | Okay, abrir YouTube. No, cancelar | La palabra `cancelar` debe decirse al final |
| `en` n `minutos` | Programa la ejecución de otro pedido para dentro de n minutos | Okay, abrir Netflix en tres minutos | `minutos` debe decirse al final, y "n" debe ser un número natural |
| `buscar` X `en` Y | Busca en el sitio Y lo que le pediste (X) | Okay, buscar "Mercado Libre" en Linkedin | Debe invocarse siguiendo el patrón mencionado. Sólo funciona en sitios preconfigurados |
| `escribir` | Escribe lo que quieras sin símbolos y en minúsculas | Okay, escribir "comprar salsa de tomate" | --- |
| `repetí` | Repite lo que quieras | Okay, repetí "hola me llamo Esteban" | --- |
| `estas ahí` | Esto es más que nada para chequar si te está escuchando | Okay, ¿estás ahí? | --- |
| `hora` | Consultar la hora | Okay, decime qué hora es | --- |
| `fecha` | Consultar la fecha | Okay, ¿qué fecha es hoy? | --- |
| `atajo` n | Abre el n-ésimo programa disponible de la barra de tareas | Okay, atajo 1 | `n` debe ser un número natural entre 1 y 9. No lo abrirá si no lo tenés disponible |
| `abre` X | Abre el sitio X | Okay, abre Twitter | Sólo funciona en sitios preconfigurados |
| `reproduce musica` | Setea el volumen al 20% y abre una lista de reproducción | Okay, reproduce música | La lista de reproducción debe estar en C:/Users/{usuario}/Music/av/musica.xspf |
| `cerrar` X `archivo` | Cierra el programa actual | Okay, cerrar archivo | --- |
| `mute` | Activa/desactiva el mute | Okay, mute | --- |
| `minimizar todo` | Minimiza todos los programas | Okay, minimizar todo | --- |
| `minimizar` | Minimiza el programa actual | Okay, minimizar | --- |
| `volumen`...`%` | Cambia el volumen de la computadora | Okay, volumen al 20% | Sólo coloca valores pares |
| `chiste` | Te dice un chiste relacionado a la informática (son malísimos) | Okay, decime un chiste | --- |
| `cómo te llamás` | Te dice su nombre | Okay, ¿Cómo te llamás? | --- |
| `tecla` X | Presiona la tecla solicitada | Okay, presioná la tecla P | --- |
| `captura de pantalla` | Hace una captura de pantalla | Okay, sacá una captura de pantalla | Guarda la captura en la carpeta `capturas_de_pantalla` ubicada donde está el asistente |
| `iniciá` / `detené` el `cronómetro` | Inicia o detiene un cronómetro | Okay, iniciá el cronómetro | --- |
| `alarma`... `en` n `minutos` | Programa una alarma para dentro de n minutos | Okay, activá la alarma en 5 minutos | --- |
| `nivel de humor` | Consulta el porcentaje de "humor" (5% por defecto) | Okay, decime tu nivel de humor | --- |
| `humor`...`X%` | Cambia el nivel de humor al n%, siendo n un número entero entre 0 y 100 | Okay, nivel de humor al 10% | --- |
| `ayuda` | Te redirige a este readme para entender mejor al asistente | Okay, necesito ayuda | --- |
| `ver código fuente` | Te redirige al código fuente del asistente | Okay, ver código fuente | --- |

Tiene 3 activadores más pero solo están para aumentar la interactividad (`Okay` a secas, `gracias` y `hola`)

### Limitaciones 🚨
1. Está hecho para ser utilizado en windows

2. A la hora de hacer un pedido debes ser claro y conciso, sin pausas

3. Se necesita conexión activa a internet para que funcione el reconocedor de voz. En caso de que se desconecte, tratará de reconectarse un par de veces

4. Si suspendés la computadora y la volvés a encender, el asistente dejará de funcionar como máximo 60 segudos, luego volverá a estar disponible

## Guía para programadores 👨‍💻

### Pre-requisitos 📋
El código está hecho y testeado utilizando la versión 3.12.0 de Python y un Windows 11 de 64bits.

### Descarga ⬇️
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

Recuerda que debes activar el entorno virtual siempre que desees usarlo

### Modificación 🛠️
Si deseas modificar al asistente, considera que:

* Los archivos relevantes a tener en cuenta en todo momento son:
    * Carpetas `dist` y `.venv` - Archivos compilados y entorno virtual. No las subo a GitHub porque te debes crear las tuyas.
    * [GUI.py](GUI.py) - Interfaz gráfica
    * [/scripts/asistente_virtual.py](./scripts/asistente_virtual.py) - Lógica gruesa del asistente
    * Carpeta [scripts](./scripts) - Archivos python de apoyo
    * Carpeta [complementos](./complementos) - Recursos complementarios
    * [config.ini](./config.ini) - Archivo donde guardo configuración dinámica y persistente del asistente

* Una vez que estés conforme con tus cambios, coloca en la terminal el comando:

```bash
pyinstaller --noconsole --name "Asistente_virtual" --icon=complementos/icon.ico --contents-directory . --add-data "complementos;complementos" --add-data "scripts;scripts" --add-data "config.ini;." GUI.py
```

para compilar el proyecto en la carpeta dist. Asegúrate de haber eliminado (o vaciado) la carpeta dist antes de compilar para evitar errores imprevistos. Luego abre el archivo Asistente_virtual.exe ubicado en `dist/Asistente_virtual` y utiliza tu versión modificada!

`Nota:` personalmente, siempre que quiero compilar al asistente ejecuto el pedido "actualizar" del propio asistente, ya que además te elimina los archivos sobrantes. Este pedido no se encuentra en la tabla mostrada más arriba ya que no es para todos los usuarios.

### Despliegue 📦
Podrás iniciar el asistente ejecutando [GUI.py](GUI.py)
