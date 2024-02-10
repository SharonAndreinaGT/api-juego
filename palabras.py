import random
from unidecode import unidecode

def cargar_diccionario(ruta_diccionario):
    with open(ruta_diccionario, "r", encoding="utf-8") as file:
        return [line.strip().lower() for line in file]

def filtrar_palabras(palabras, longitud_max=12):
    palabras_filtradas = [palabra for palabra in palabras if len(palabra) <= longitud_max and palabra.isalpha()]
    palabras_sin_acentos = [unidecode(palabra) for palabra in palabras_filtradas]
    return palabras_sin_acentos

def obtener_palabra_secreta():
    palabras = filtrar_palabras(cargar_diccionario("es_ES.dic"))
    return random.choice(palabras)
