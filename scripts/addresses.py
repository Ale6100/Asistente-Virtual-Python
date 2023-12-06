import os

user = os.environ.get('USERNAME') or os.environ.get('USER') # El usuario de tu PC actual

addresses = {
    'googlemaps': {
        'sitios': ['Google Maps', 'Maps'], # Palabras clave para identificar la página
        'url': 'https://www.google.com.ar/maps',
        'buscador': 'https://www.google.com.ar/maps/search/' # Acceso al buscador de cada página
    },
    'google': {
        'sitios': ['Google', 'el buscador', 'navegador'],
        'url': 'https://www.google.com.ar/',
        'buscador': 'https://www.google.com.ar/search?q='
    },
    'youtube': {
        'sitios': ['Youtube'],
        'url': 'https://www.youtube.com/',
        'buscador': 'https://www.youtube.com/results?search_query='
    },
    'steam': {
        'sitios': ['Steam', 'Stim'],
        'url': 'https://store.steampowered.com/',
        'buscador': 'https://store.steampowered.com/search/?term='
    },
    'facebook': {
        'sitios': ['Facebook'],
        'url': 'https://www.facebook.com/',
        'buscador': 'https://www.facebook.com/search/top/?q='
    },
    'twitch': {
        'sitios': ['Twitch'],
        'url': 'https://www.twitch.tv/',
        'buscador': 'https://www.twitch.tv/search?term='
    },
    'twitter': {
        'sitios': ['Twitter'],
        'url': 'https://x.com/',
        'buscador': 'https://x.com/search?q='
    },
    'mercadolibre': {
        'sitios': ['MercadoLibre', 'Mercado Libre'],
        'url': 'https://www.mercadolibre.com.ar/',
        'buscador': 'https://listado.mercadolibre.com.ar/'
    },
    'linkedin': {
        'sitios': ['LinKedIn'],
        'url': 'https://www.linkedin.com/',
        'buscador': 'https://www.linkedin.com/search/results/all/?keywords='
    },
    'github': {
        'sitios': ['GitHub'],
        'url': 'https://github.com/',
        'buscador': 'https://github.com/search?q='
    },
    'wikipedia': {
        'sitios': ['Wikipedia'],
        'url': 'https://es.wikipedia.org/',
        'buscador': 'https://es.wikipedia.org/wiki/'
    },
    'tiktok': {
        'sitios': ['Tik Tok', 'Tic Tac', 'Tic Toc'],
        'url': 'https://www.tiktok.com/',
        'buscador': 'https://www.tiktok.com/search?q='
    },
    'zoom': {
        'sitios': ['zoom'],
        'url': 'https://zoom.us/',
        'buscador': 'https://explore.zoom.us/es/search/#q='
    },
    'amazon': {
        'sitios': ['Amazon'],
        'url': 'https://www.amazon.com/',
        'buscador': 'https://www.amazon.com/s?k='
    },
    'whatsapp': {
        'sitios': ['WhatsApp'],
        'url': 'https://web.whatsapp.com/',
    },
    'netflix': {
        'sitios': ['Netflix'],
        'url': 'https://www.netflix.com/',
    },
    'disney': {
        'sitios': ['Disney'],
        'url': 'https://www.disneyplus.com/',
    },
    'prime': {
        'sitios': ['Prime Video'],
        'url': 'https://www.primevideo.com/',
    },
    'starplus': {
        'sitios': ['Star Plus'],
        'url': 'https://www.starplus.com/',
    },
    'geogebra': {
        'sitios': ['Geogebra'],
        'url': 'https://www.geogebra.org/calculator',
    },
    'drive': {
        'sitios': ['Google Drive'],
        'url': 'https://drive.google.com/drive/u/0/my-drive',
    },
    'mercadopago': {
        'sitios': ['MercadoPago', 'Mercado Pago'],
        'url': 'https://www.mercadopago.com.ar/',
    },
    'hbo': {
        'sitios': ['HBO Max', ' Max'],
        'url': 'https://play.hbomax.com/',
    },
    'traductor': {
        'sitios': ['Traductor', 'Translate'],
        'url': 'https://translate.google.com.ar/',
    },
    'nacion': {
        'sitios': ['Banco Nacion'],
        'url': 'https://hb.redlink.com.ar/bna/login.htm',
    },
    'santander': {
        'sitios': ['Banco Santander'],
        'url': 'https://www2.personas.santander.com.ar/obp-webapp/angular/#!/login',
    },
    'buscagatos': {
        'sitios': ['Buscaminas', 'Buscagatos'],
        'url': 'https://buscagatos.netlify.app/',
    },
    'sourcecode': {
        'sitios': ['codigo', 'documentacion', 'ayuda'],
        'url': 'https://github.com/Ale6100/Asistente-Virtual-Python.git',
    },
    'plazofijo': {
        'sitios': ['Simulador plazo fijo', 'Simulador de plazo fijo'],
        'url': 'https://simuladorplazofijo.netlify.app/',
    },
    'canciones': {
        'sitios': ['canciones', 'musica', 'lista de reproduccion'],
        'url': f'C:/Users/{user}/Music/av/musica.xspf',
    },
    'word': {
        'sitios': ['word'],
        'url': 'https://www.microsoft365.com/launch/word',
    },
    'excel': {
        'sitios': ['excel'],
        'url': 'https://www.microsoft365.com/launch/excel',
    },
    'powerpoint': {
        'sitios': ['powerpoint'],
        'url': 'https://www.microsoft365.com/launch/powerpoint',
    },
    'outlook': {
        'sitios': ['outlook'],
        'url': 'https://office.live.com/start/Outlook.aspx',
    },
    'gmail': {
        'sitios': ['gmail'],
        'url': 'https://mail.google.com/',
    },
    'chatgpt': {
        'sitios': ['chat gpt'],
        'url': 'https://chat.openai.com/',
    },
    'notas': {
        'sitios': ['nota'],
        'url': 'https://lista-de-notas.netlify.app',
    }
}

dir_mixer = {
    'alarma': {
        'nombre': 'Alarma',
        'volumen': 0.5
    },
    'wazaa': {
        'nombre': 'Wazaa',
        'volumen': 0.25
    },
    'hello_m_f': {
        'nombre': 'Hello_m_f',
        'volumen': 1
    },
    'Excel_preg': {
        'nombre': 'Excelente_pregunta',
        'volumen': 0.5
    },
    'Marad_ee': {
        'nombre': 'Maradona_eeeeee',
        'volumen': 1
    },
    'No_lo_se_tu_dime': {
        'nombre': 'No_lo_se_tu_dime',
        'volumen': 1
    },
    'muy_buena_preg': {
        'nombre': 'Auron_es_una_muy_buena_pregunta',
        'volumen': 0.5
    },
    'info_vale_millones': {
        'nombre': 'Esta_informacion_vale_millones',
        'volumen': 1
    },
    'Uvuewewe': {
        'nombre': 'Uvuewewe',
        'volumen': 0.5
    },
    'Hasta_la_proxima': {
        'nombre': 'Hasta_la_proxima',
        'volumen': 0.1
    },
    'Ah_re_bolu': {
        'nombre': 'Ah_re_bolu',
        'volumen': 0.5
    },
    'Estup': {
        'nombre': 'Estup',
        'volumen': 0.5
    },
    'Imbec': {
        'nombre': 'Imbec',
        'volumen': 0.75
    },
    'buen_servicio': {
        'nombre': 'que_buen_servicio',
        'volumen': 0.33
    },
    'es_bellisimo': {
        'nombre': 'es_bellisimo',
        'volumen': 1
    }
}
