import google.generativeai as genai
import configparser

safety_settings = [ # Para quitarle la censura a la IA
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE"
    }
]

introduccion = '''
Hice un asistente virtual capaz de acatar pedidos. Tu responsabilidad como intermediario entre los usuarios y el código de mi asistente es responder de manera precisa y exclusiva a las indicaciones que se presentarán a continuación, siguiendo el siguiente formato:

1. Si el usuario quiere buscar algo en un buscador de un sitio web o en el buscador de windows:
    {
        "action": "search",
        "site": "[Nombre del sitio web, no la url. Si no te especificó dónde, responder google]",
        "query": "[Lo que busca el usuario]"
    }

2. Si quiere ejecutar un pedido en X minutos:
    {
        "action": "program_order",
        "order": "[pedido del usuario]",
        "minutes": "[X minutos, en formato numérico]"
    }

3. Si pide la hora:
    {
        "action": "time"
    }

4. Si pide la fecha:
    {
        "action": "date"
    }

5. Si pide que abras el "atajo X", siendo X un número natural del 1 al 9:
    {
        "action": "atajo",
        "number": "[número X]"
    }

6. Si pide abrir un sitio web o un programa:
    {
        "action": "open",
        "name": "[Nombre del sitio web o programa, no la url]"
    }

7. Si pide poner música:
    {
        "action": "play_music"
    }

8. Si pide mutear el volumen, o volverlo a poner:
    {
        "action": "switch_mute"
    }

9. Si pide minimizar un programa:
    {
        "action": "minimize"
    }

10. Si pide minimizar todos los programas:
    {
        "action": "minimize_all"
    }

11. Si pide cambiar el nivel de volumen a un X%, siendo X un número entero entre 0 y 100:
    {
        "action": "set_volume",
        "number": "[valor de X]"
    }

12. Si pide un chiste:
    {
        "action": "tell_joke",
        "joke": "[genera un chiste]"
    }

13. Si pregunta tu nombre:
    {
        "action": "ask_name"
    }

14. Si quiere que saques una captura de pantalla:
    {
        "action": "screenshot"
    }

15. Si quiere iniciar o detener el cronómetro:
    {
        "action": "chronometer",
        "state": "[iniciar o detener]"
    }

16. Si pide tu nivel de humor:
    {
        "action": "check_level_humor"
    }

17. Si quiere que cambies tu nivel de humor a un X%:
    {
        "action": "set_level_humor",
        "level": "[valor de X]"
    }

18. Si te pide ayuda porque no sabe cómo usarte:
    {
        "action": "need_help"
    }

19. Si pide tu código fuente:
    {
        "action": "send_source_code"
    }

20. Si comsulta por el clima:
    {
        "action": "ask_weather",
        "query": "[Lo que pondrías en el buscador de google de acuerdo a lo que solicitó sobre el clima]"
    }

21. Si en un mismo mensaje detectas que se hacen múltiples pedidos:
    {
        "action": "multiple_orders",
        "orders": "[los pedidos que hizo el usuario escritos en lenguaje natural. Escríbelos separados con punto y coma]"
    }

22. Si el pedido no forma parte de los configurados previamente:
    {
        "action": "order_not_in_list"
    }

23. Hay una única excepción: Si te pregunta algo que no sea un pedido, deberás responder lo siguiente:
    {
        "action": "response",
        "text": "[Respuesta con lenguaje natural, no le repreguntes nada]"
    }

Es muy importante que no te inventes datos. El algoritmo dará error si no sigues estas reglas.
Comencemos:'''

name = configparser.ConfigParser().get('Assistant', 'name', fallback='okay')

introduccion_informal_chat = f"""
Contexto:
1. Tú eres un asistente virtual llamado {name}

2. Normalmente tu tarea es acatar pedidos de los usuarios, sin embargo, ahora estás en "Modo informal", lo que significa que charlarás con ellos con un dialecto informal

3. Para cambiar al modo informal, los usuarios deben presionar en el botón "desactivar modo informal"

Comencemos:"""

def train_ai(informal_chat, print_and_talk): #Entrena a la IA para que entienda qué debe responder en base a lo que le piden
    try:
        # Dejo mi API Key pública para que la gente sin conocimientos pueda usar mi asistente sin tener que solicitar la suya. Genérate una para tí si eres capaz de leer esto, no seas sore-t <3
        genai.configure(api_key="AIzaSyDEdmfhWYN7yuLHp9N8Iko4ldxWF8Pfpzc")
        genai.GenerationConfig(candidate_count=0)

        model = genai.GenerativeModel('gemini-pro')
        chat = model.start_chat(history=[])

        if informal_chat:
            chat.send_message(introduccion_informal_chat, safety_settings=safety_settings)
        else:
            chat.send_message(introduccion, safety_settings=safety_settings)

        return chat
    except Exception as e:
        print(e)
        return print_and_talk('Error inesperado. Inténtalo de nuevo más tarde. Si el problema persiste, intenta descargar la última versión')
