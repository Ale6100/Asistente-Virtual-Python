introductory_phrases = [ # Frases iniciales que se filtran de rec cuando inicia el asistente
    'yo necesito',
    'necesito'
    'podrias',
    'seria bueno que',
    'por favor',
    'quiero',
    'me gustaria',
    'me gustaria que'
    'serias tan amable de',
    'seria de gran ayuda si',
    'harias un gran favor si pudieras',
    'podes',
    'puedes',
    'estaria bueno',
    "che",
    'quiero que'
]

final_phrases = [ # Frases fnales que se filtran de rec cuando inicia el asistente
    'por favor',
    'gracias',
    'muchas gracias',
    'muchisimas gracias'
]

root_words = ['buscame', 'buscar', 'buscas', 'busca', 'buscarias', 'busques'] # Frases iniciales que se filtran de rec dentro de la función search(), junto con los complementos de la siguiente lista
complement = [' el', ' la', ' los', ' las']
search_phrases = []
for palabra in root_words:
    search_phrases.append(palabra)
    for comp in complement:
        search_phrases.append(palabra + comp)

writing_phrases = [
    'escribir',
    'escribis',
    'escribi',
    'escribes',
    'escribe',
    'escribas'
]

repeat_phrases = [
    'repeti',
    'repite',
    'repetis',
    'repetir',
    'repitas'
]
