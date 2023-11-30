frasesIntroductorias = [ # Frases iniciales que se filtran de rec cuando inicia el asistente
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

frasesFinales = [ # Frases fnales que se filtran de rec cuando inicia el asistente
    'por favor',
    'gracias',
    'muchas gracias',
    'muchisimas gracias'
]

palabras_raiz = ['buscame', 'buscar', 'buscas', 'busca', 'buscarias', 'busques'] # Frases iniciales que se filtran de rec dentro de la función buscar(), junto con los complementos de la siguiente lista
complemento = [' el', ' la', ' los', ' las']
frases_de_buscar = []
for palabra in palabras_raiz:
    frases_de_buscar.append(palabra)
    for comp in complemento:
        frases_de_buscar.append(palabra + comp)

frases_de_escribir = [
    'escribir',
    'escribis',
    'escribi',
    'escribes',
    'escribe',
    'escribas'
]

frases_de_repetir = [
    'repeti',
    'repite',
    'repetis',
    'repetir',
    'repitas'
]
