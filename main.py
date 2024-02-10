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

#dos listas, una para las letras correctas y otra para las letras incorrectas. Inicialmente, ambas listas estarán vacías. 
letras_correctas = []
letras_incorrectas = []
palabra_mostrar = ""
palabra_secreta= "" #variable que almacena la palabra secreta	
vidas = 6 #variable que almacena las vidas del jugador

@app.get("/palabras") #ruta de seleccion de palabras
async def get_palabras():
   global letras_correctas, letras_incorrectas, palabra_secreta, vidas
   letras_correctas = []
   letras_incorrectas = []
   palabra_secreta = random.choice(palabras)
   vidas = 6
   
   return {'palabra': palabra_secreta}


#metodo que evalua si la palabra secreta esta correcta y la muestra, para no seguir introduciendo letras
def palabra_revelada() -> bool:
    global palabra_secreta, palabra_mostrar
    palabra_mostrar = ['_'] * len(palabra_secreta)  # inicializa la palabra a mostrar con guiones bajos

    if palabra_secreta == "": # si la palabra secreta está vacía
       palabra_secreta = random.choice(palabras) # selecciona una palabra al azar de la lista de palabras
      
    for correcta in letras_correctas:  # recorre la lista de letras correctas
        letra = correcta["letra"]  # almacena la letra
        posiciones = correcta["posiciones"]  # almacena las posiciones de la letra en la palabra secreta

        for pos in posiciones:  # para cada posición de la letra en la palabra secreta
            palabra_mostrar[pos] = letra  # reemplaza el guion bajo con la letra en la posición correcta

    palabra_mostrar = "".join(palabra_mostrar)  # une la lista en una cadena
    print(palabra_mostrar, "palabra", palabra_secreta)

    return palabra_mostrar == palabra_secreta  # compara la palabra a mostrar con la palabra secreta

@app.post("/adivinar/") #ruta o metodo para seleccionar letras y adivinar la palabra
async def adivinar_letra(letra: str):
   global palabra_secreta, vidas
   existe = False
   
   if palabra_secreta == "": #si la palabra secreta esta vacia
      palabra_secreta = random.choice(palabras)
   
   if letra in palabra_secreta: #si la letra pertenece a la palabra secreta la agrega
      letra_correcta = {"letra": letra, "posiciones": [pos for pos, char in enumerate(palabra_secreta) if char == letra]} #almacena la letra y la posicion en la que se encuentra
      
      for correcta in letras_correctas: #recorre la lista de letras correctas
         if correcta["letra"] is letra: #si la letra esta en la lista de letras correctas
            existe = True
            break
      
      if not existe: #si no existe la letra en la lista de letras correctas
         letras_correctas.append(letra_correcta) #agrega la letra a la lista de letras correctas
         
      if palabra_revelada(): #llama el metodo y comprueba si las letras formaron la palabra correcta retorna el mensaje
         return {"resultado": True, "mensaje": "La palabra ya ha sido adivinada, no puedes seguir introduciendo letras.", "palabra": palabra_mostrar}
            
      return {"resultado": False, "palabra": palabra_mostrar}
   else:
      vidas = vidas - 1 #si la letra no pertenece a la palabra secreta resta una vida
         
      return {"resultado": False, "vidas": vidas, "palabra": palabra_mostrar}

@app.delete("/reiniciar/") #ruta o metodo para reiniciar el juego
async def reiniciar():
   global letras_correctas, letras_incorrectas, palabra_secreta, vidas
   letras_correctas = []
   letras_incorrectas = []
   palabra_secreta = random.choice(palabras)
   vidas = 6

#funcion principal
@app.get("/")
def bienvenida():
   return "Bienvenidos al juego del ahorcado"


