# Asistente virtual en Python

Bienvenido! este es mi primer asistente con Python. Hace un tiempo hice uno con JavaScript (https://github.com/Ale6100/Asistente-Virtual-JS.git) pero por las limitaciones de ese lenguaje no pude explotar su potencial.

Mi objetivo con este proyecto es lograr que el asistente sea lo suficientemente útil como para que desees utilizarlo a diaro, sabiendo que lo puedes dejar encendido en segundo plano para que esté listo en cualquier momento que lo necesites.

## Comenzando 🚀

Lee las siguientes instrucciones si deseas obtener una copia del proyecto en tu computadora.

Primero debes descargar el archivo comprimido _zip_ desde el botón verde "code" o  hacer click [aquí](https://github.com/Ale6100/Asistente-Virtual-Python/archive/refs/heads/main.zip).

### Pre-requisitos 📋
El código está hecho y testeado utilizando la versión 3.11.4 de Python y un windows 11 de 64bits.

Estoy consciente de que no estoy dejando documentación de las librerías utilizadas, es una tarea que tengo pendiente.

### Instalación y uso 🔧

Puedes ver el estado actual del asistente abriendo el ejecutable "Asistente_virtual.exe" en la carpeta [dist/Asistente_virtual](dist/Asistente_virtual). Si te da error o deseas modificarlo, considera que la carpeta dist se genera automáticamente a la hora de compilar el proyecto entero. El código central está repartido entre los archivos [asistente_virtual.py](asistente_virtual.py) (asistente) y [GUI.py](GUI.py) (interfaz gráfica).

Puedes ejecutar el archivo GUI.py cada vez que hagas un cambio para iniciar al asistente y testear si funciona. Una vez que estés conforme con tus cambios, coloca en la terminal el comando

```
pyinstaller --windowed --name "Asistente_virtual" --add-data "complementos;complementos" --add-data "scripts;scripts" --icon=complementos/icon.ico --add-data "asistente_virtual.py;." GUI.py
```

para compilar el proyecto en la carpeta dist. Asegúrate de haber eliminado (o vaciado) la carpeta dist antes de compilar para evitar errores imprevistos. Luego abre el archivo Asistente_virtual.exe tal como expliqué anteriormente y utiliza tu versión modificada!

## Pedidos por voz 🤖

* Todas los pedidos deben iniciar con el nombre del asistente. Por ahora se llama "Okay" por simplicidad

* Pedido encapsulado: Para mejorar el entendimiento, opcionalmente puedes decir su nombre por segunda vez en un mismo pedido. En este caso, el asistente interpretará que el pedido está en medio de la primera y la segunda vez que lo nombraste

* Sólo podrás hablar cuando el texto "Escuchando..." está visible

* Te responde "no te entendí" cuando escuchó algo pero no lo relacionó con ningún pedido existente. Esto significa que pudo haber entendido mal o hiciste un pedido que no está dentro de los disponibles

* Todas las palabras clave tienen variantes (por ejemplo en vez de decir "abre" se puede decir "abrís")

* Hay pedidos que tienen condiciones muy específicas para que funcionen bien. Se especifican en la siguiente tabla

* En general, los pedidos que están más arriba de esta tabla tienen mayor prioridadad que los de abajo

| Palabras clave | Descripción | Ejemplo | Condición
| :--- | :--- | :--- | :--- |
| `basta` | Apaga al asistente | Okay, basta | --- |
| `cancelar` | Cancela el pedido que estás solicitando | Okay, abrir YouTube. No, cancelar | La palabra `cancelar` debe decirse al final |
| `en` n `minutos` | Programa la ejecución de otro pedido para dentro de n minutos | Okay, abrir Netflix en tres minutos | `minutos` debe decirse al final, y "n" debe ser un número natural |
| `buscar` X `en` Y | Busca en el sitio Y lo que le pediste (X) | Okay, buscar "Mercado Libre" en Linkedin | Debe invocarse siguiendo el patrón mencionado. Sólo funciona en sitios preconfigurados |
| `escribir` | Escribe lo que quieras (sin símbolos) | Okay, escribir "comprar salsa de tomate" | La palabra `escribir` debe decirse al principio |
| `repetí` | Repite lo que quieras | Okay, repetí "hola me llamo Roberto" | La palabra `repetí` debe decirse al principio |
| `estas ahí` | Esto es más que nada para chequar si te está escuchando | Okay, ¿estás ahí? | --- |
| `hora` | Consultar la hora | Okay, decime qué hora es | --- |
| `fecha` | Consultar la fecha | Okay, ¿qué fecha es hoy? | --- |
| `atajo` n | Abre el n-ésimo programa disponible de la barra de tareas | Okay, atajo 1 | `n` debe ser un número natural entre 1 y 9. No lo abrirá si no lo tenés disponible |
| `abre` X | Abre el sitio X | Okay, abre Twitter | Sólo funciona en sitios preconfigurados |
| `reproduce musica` | Abre una lista de reproducción | Okay, reproduce música | La lista de reproducción debe estar en C:/Users/{usuario}/Music/av/musica.xspf |
| `cerrar` | Cierra el programa actual | Okay, cerrar | --- |
| `silenciar` | Activa/desactiva el mute | Okay, silenciar | --- |
| `minimizar todo` | Minimiza todos los programas | Okay, minimizar todo | --- |
| `minimizar` | Minimiza el programa actual | Okay, minimizar | --- |
| `volumen`...`%` | Cambia el volumen de la computadora | Okay, volumen al 20% | Sólo coloca valores pares |
| `chiste` | Te dice un chiste relacionado a la informática | Okay, decime un chiste | --- |
| `cómo te llamás` | Te dice su nombre | Okay, ¿Cómo te llamás? | --- |
| `tecla` X | Presiona la tecla solicitada | Okay, presioná la tecla T | --- |
| `captura de pantalla` | Hace una captura de pantalla | Okay, sacá una captura de pantalla | Guarda la captura en la ubicación del programa |
| `iniciá` / `detené` el `cronómetro` | Inicia o detiene un cronómetro | Okay, iniciá el cronómetro | Se reinicia si apagás al asistente |
| `alarma`... `en` n `minutos` | Programa una alarma para dentro de n minutos | Okay, activá la alarma en 5 minutos | --- |
| `nivel de humor` | Consulta el porcentaje de "humor" (5% por defecto) | Okay, decime tu nivel de humor | --- |
| `humor`...`X%` | Cambia el nivel de humor al n%, siendo n un número entero entre 0 y 100. Se reestablece en 5% cada vez que se apaga al asistente | Okay, nivel de humor al 10% | --- |
| `ayuda` | Te redirige a este readme para entender mejor al asistente | Okay, necesito ayuda | --- |
| `ver código fuente` | Te redirige al código fuente del asistente | Okay, ver código fuente | --- |

Tiene 3 activadores más pero solo están para aumentar la interactividad (`okey` a secas, `hola` y `gracias`)

Estoy abierto a sugerencias!

## Limitaciones 🚨

1. Está hecho para ser utilizado en windows

2. A la hora de hacer un pedido debes ser claro y conciso, sin pausas

3. Se necesita conexión activa a internet para que funcione el reconocedor de voz. En caso de que se desconecte, tratará de reconectarse dos veces

4. Existe una mínima posibilidad de que el asistente se bloquee si suspendes la computadora y la vuelves a encender. Si eso pasa simplemente reinicialo apretando en el botón "Detener asistente" y luego en "Iniciar asistente"

## Autor ✒️

* **Alejandro Portaluppi** - [LinkedIn](https://www.linkedin.com/in/alejandro-portaluppi/)
