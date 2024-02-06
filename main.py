from fastapi import FastAPI #importar librerias/bibliotecas necesarias
from fastapi.middleware.cors import CORSMiddleware #middleware para habilitar todos los origenes
import random

app = FastAPI() #instancia de la clase 

origins = [ # origenes permitidos para la api
    "http://localhost:4200", # front
    "http://localhost:8080",
]

app.add_middleware( # añadir middleware para habilitar el CORS
    CORSMiddleware, 
    allow_origins=origins, # permitir origenes
    allow_credentials=True, #permitir credenciales
    allow_methods=["*"], # permitir todos los metodos http
    allow_headers=["*"], # permitir todos los headers de las peticiones
)

palabras = ['python', 'hola', 'bienvenido','sharon','pote','jugo'] #lista donde se encuentran las palabras a adivinar 
palabra_secreta = random.choice(palabras) #guarda en la variable alguna palabras que pertenezca a la lista 

#dos listas, una para las letras correctas y otra para las letras incorrectas. Inicialmente, ambas listas estarán vacías. 
letras_correctas = []
letras_incorrectas = []

@app.get("/palabras") #ruta de seleccion de palabras
async def get_palabras():
   return {'palabra': random.choice(palabras)} #esta linea de coigo selecciona una palabra randon de mi arreglo palabras

#metodo que evalua si la palabra secreta esta correcta y la muestra, para no seguir introduciendo letras
def palabra_revelada(palabra_secreta: str, letras_correctas: list) -> bool: #Funcion que toma dos argumentos, palabra a adivinar y las letras correctas 
  palabra_mostrar = ''.join(['_' if letra not in letras_correctas else letra for letra in palabra_secreta]) # la función join para convertir la lista resultante en una cadena
  return palabra_mostrar == palabra_secreta

@app.post("/adivinar/") #ruta o metodo para seleccionar letras y adivinar la palabra
async def adivinar_letra(letra: str):
   if palabra_revelada(palabra_secreta, letras_correctas): #llama el metodo y comprueba si las letras formaron la palabra correcta retorna el mensaje
      return {"resultado": False, "mensaje": "La palabra ya ha sido adivinada, no puedes seguir introduciendo letras."}
   elif letra in palabra_secreta: #si la letra pertenece a la palabra secreta la agrega
      letras_correctas.append(letra)
      return {"resultado": True, "letras_correctas": letras_correctas}
   else:
      letras_incorrectas.append(letra)
      return {"resultado": False, "letras_incorrectas": letras_incorrectas}
   
def mostrar_palabra_secreta():
   palabra_mostrar = ""
   for letra in palabra_secreta:
       if letra in letras_correctas:
           palabra_mostrar += letra #si la letra es correcta agrega a la palabra a mostrar
       else:
           palabra_mostrar += "_"
   return palabra_mostrar

@app.get("/mostrar_palabra/")
async def mostrar_palabra():
   return {"palabra secreta": mostrar_palabra_secreta()}

#funcion principal
@app.get("/")
def bienvenida():
   return "Bienvenidos al juego del ahorcado"


