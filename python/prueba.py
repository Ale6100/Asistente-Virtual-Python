from translate import Translator

traduccion = Translator(to_lang="en").translate("perro", src = 'es', dest = 'en' ).text

print(traduccion)