from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import requests

# Comando de ejecución: uvicorn Streamflix:app --reload --host localhost --port 8003


app = FastAPI()

BASE_URL_CONTENIDOS = "http://127.0.0.1:8000"
BASE_URL_USUARIOS = "http://127.0.0.1:8001"
BASE_URL_INTERACCIONES = "http://127.0.0.1:8002"


# Configuración de rutas estáticas para CSS
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configuración de plantillas Jinja2
templates = Jinja2Templates(directory="templates")

# Endpoint para la página principal
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    # Renderiza la página index.html y la devuelve al usuario
    return templates.TemplateResponse("index.html", {"request": request})

# Endpoint para hacer login
@app.post("/login")
async def login(request: Request, email: str = Form(...), password: str = Form(...)):
    # Enviar las credenciales al microservicio para verificar el login
    data = {"email": email, "password": password}
    response = requests.post(f"{BASE_URL_USUARIOS}/usuarios/login", json=data)
    
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Credenciales inválidas")
    
    # Si las credenciales son correctas, obtenemos los datos del usuario
    user_data = response.json()
    user_id = user_data.get("id")
    
    # Redirigimos a la página principal
    return templates.TemplateResponse("pantalla_principal.html", {"request": request, "user_id": user_id})

# Endpoint para mostrar la página de registro
@app.get("/registro_usuario", response_class=HTMLResponse)
async def registro_usuario(request: Request):
    return templates.TemplateResponse("registro_usuario.html", {"request": request})

# Endpoint para obtener los planes de suscripción
@app.get("/planes_suscripcion")
async def obtener_planes():
    # Aquí haces una solicitud a tu microservicio que devuelve los planes
    response = requests.get(f"{BASE_URL_USUARIOS}/planes-suscripcion")
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="No se pudieron obtener los planes.")
    return response.json()

# Endpoint para registrar un nuevo usuario
@app.post("/registro")
async def registrar_usuario(request: Request, name: str = Form(...), email: str = Form(...), password: str = Form(...), language: str = Form(None), subscription_plan: str = Form(...)):
    # Aquí haces una solicitud para registrar al usuario en tu microservicio
    data = {
        "nombre": name,
        "email": email,
        "password": password,
        "idioma": language,
        "idPlanSuscripcion": subscription_plan
    }
    response = requests.post(f"{BASE_URL_USUARIOS}/usuarios/registro", json=data)
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Error al registrar el usuario.")
    
    # Guardamos el id del usuario retornado
    user_data = response.json()
    user_id = user_data.get("id")
    
    # Podrías guardar el `user_id` para uso posterior si es necesario
    return templates.TemplateResponse("pantalla_principal.html", {"request": request, "user_id": user_id})

#TODO AÑADIDO
# Endpoint para mostrar los detalles de una película
@app.get("/detalles_pelicula/{idContenido}", response_class=HTMLResponse)
async def detalles_pelicula(request: Request, idContenido: str):
    # Solicita los detalles de la película al microservicio de contenidos
    contenido = requests.get(f"{BASE_URL_CONTENIDOS}/contenidos/{idContenido}")
    
    if contenido.status_code != 200:
        raise HTTPException(status_code=404, detail="No se encontraron los detalles de la película.")
      
    # Extrae los detalles de la película del JSON de la respuesta
    detalles_pelicula = contenido.json()

    #Extraer nombre del genero a partir del id
    genero = requests.get(f"{BASE_URL_CONTENIDOS}/generos/{detalles_pelicula["idGenero"]}")
    detalles_genero = genero.json()
    nombre_genero = detalles_genero["nombre"]

    #Extraer nombre del director a partir del id
    director = requests.get(f"{BASE_URL_CONTENIDOS}/directores/{detalles_pelicula["idDirector"]}")
    detalles_director = director.json()
    nombre_director = detalles_director["nombre"]

    #Cambiar los valores de ids por nombres
    detalles_pelicula["idGenero"] = nombre_genero
    #detalles_pelicula["idDirector"] = nombre_director
    
    # Renderiza la plantilla detalles_pelicula.html con los datos de la película
    return templates.TemplateResponse("detalles_pelicula.html", {
        "request": request,
        "pelicula": detalles_pelicula
    })

