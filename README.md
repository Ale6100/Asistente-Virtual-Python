# Asistente virtual en Python (no terminado)

Bienvenido! este es mi primer asistente. Lo inicié en el 2020 y ahora planeo mejorarlo mucho gracias a Python y las nuevas tecnologías que aprendí con el paso del tiempo.

Hace poco hice uno con JavaScript (https://github.com/Ale6100/Asistente-Virtual-JS.git) pero por las limitaciones de ese lenguaje no pude explotar su potencial.

Está hecho para ser utilizado en windows. Por ahora no está listo para que lo puedas usar, sin embargo puedes abrir el archivo "Asistente_virtual.exe" en la carpeta "dist" para ver el estado actual.

## Activadores

* Hay pedidos que tienen condiciones muy específicas para que funcionen bien. Se especifican en la tabla.

* Todas las palabras clave tienen variantes (por ejemplo en vez de decir "abre" se puede decir "abrís").

* Todas los pedidos deben iniciar con el nombre del asistente. Por ahora se llama "Okay" por simplicidad.

| Palabras clave | Descripción | Ejemplo | Condición
| :--- | :--- | :--- | :--- |
| `basta` | Apaga al asistente | Okay, basta | --- |
| `cancelar` | Cancela el pedido que estás solicitando | Okay, abrir YouTube. No, cancelar | La palabra `cancelar` debe decirse al final |
| `en` n `minutos` | Programa la ejecución de otro pedido para dentro de n minutos | Okay, abrir Netflix en tres minutos | `minutos` debe decirse al final, y "n" debe ser un número natural |
| `buscar` X `en` Y | Busca en el sitio Y lo que le pediste (X) | Okay, buscar "Mercado Libre" en Linkedin | Debe invocarse tal como se especifica en "Descripción". Sólo funciona en sitios preconfigurados |
| `escribir` | Escribe lo que quieras (sin símbolos) | Okay, escribir "comprar salsa de tomate" | La palabra `escribir` debe decirse al principio |
| `repetí` | Repite lo que quieras | Okay, repetí "hola me llamo Roberto" | La palabra `repetí` debe decirse al principio |
| `estas ahí` | Esto es más que nada para chequar si te está escuchando | Okay, ¿estás ahí? | --- |
| `hora` | Consultar la hora | Okay, decime qué hora es | --- |
| `fecha` | Consultar la fecha | Okay, ¿qué fecha es hoy? | --- |
| `atajo` n | Abre el n-ésimo programa disponible de la barra de tareas | Okay, atajo 1 | `n` debe ser un número del 1 al 9 |
| `abre` X | Abre el sitio X | Okay, abre Twitter | Sólo funciona en sitios preconfigurados |
| `reproduce musica` | Abre una lista de reproducción | Okay, reproduce música | La lista de reproducción debe estar en C:/Users/{usuario}/Music/av/musica.xspf |
| `cerrar` | Cierra el programa actual | Okay, cerrar | --- |
| `silenciar` | Activa/desactiva el mute | Okay, silenciar | --- |
| `minimizar todo` | Minimiza todos los programas | Okay, minimizar todo | --- |
| `minimizar` | Minimiza el programa actual | Okay, minimizar | --- |
| `volumen`...`%` | Cambia el volumen de la computadora | Okay, volumen al 20% | Sólo coloca valores pares |
| `chiste` | Te dice un chiste | Okay, decime un chiste | --- |
| `cómo te llamás` | Te dice su nombre | Okay, ¿Cómo te llamás? | --- |
| `tecla` X | Presiona la tecla solicitada | Okay, presioná la tecla T | --- |
| `captura de pantalla` | Hace una captura de pantalla | Okay, sacá una captura de pantalla | Guarda la captura en la ubicación del programa |
| `inicia` / `detené` el `cronómetro` | Inicia o detiene un cronómetro | Okay, iniciá el cronómetro | Se reinicia si apagás al asistente |
| `ayuda` | Te redirige a este readme para entender mejor al asistente | Okay, necesito ayuda | --- |
| `ver código fuente` | Te redirige al código fuente del asistente | Okay, ver código fuente | --- |

Tiene 3 activadores más pero solo están para aumentar la interactividad (`hola`, `gracias` y `okey`)