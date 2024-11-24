from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
import requests

# Comando de ejecución: uvicorn Streamflix:app --reload --host localhost --port 8003

#Creación de la API de interfaz
app = FastAPI()

BASE_URL_CONTENIDOS = "http://127.0.0.1:8000"
BASE_URL_USUARIOS = "http://127.0.0.1:8001"
BASE_URL_INTERACCIONES = "http://127.0.0.1:8002"

#Métodos auxiliares
def cargar_datos(user_id: str):
    """
    Obtiene y organiza los datos necesarios para la pantalla principal.
    """
    mensajes = []  # Lista para almacenar mensajes personalizados
    recomendaciones = []
    tendencias = []
    historial = []
    generos = []
    generos_con_contenidos = []

    # Realizamos las solicitudes a los microservicios
    recomendaciones_response = requests.get(f"{BASE_URL_INTERACCIONES}/usuarios/{user_id}/recomendaciones")
    if recomendaciones_response.ok:
        recomendaciones = recomendaciones_response.json()
    else:
        mensajes.append("No se pudieron obtener las recomendaciones personalizadas.")
    
    tendencias_response = requests.get(f"{BASE_URL_INTERACCIONES}/contenido/tendencias")
    if tendencias_response.ok:
        tendencias = tendencias_response.json()
    else:
        mensajes.append("No se pudieron obtener las tendencias.")

    historial_response = requests.get(f"{BASE_URL_INTERACCIONES}/usuarios/{user_id}/historial")
    if historial_response.ok:
        historial = historial_response.json()
    else:
        mensajes.append("No se pudo recuperar el historial de usuario.")

    generos_response = requests.get(f"{BASE_URL_CONTENIDOS}/generos")
    if generos_response.ok:
        generos = generos_response.json()
    else:
        mensajes.append("No se pudieron obtener los géneros.")

    # Recuperar los contenidos por género
    for genero in generos:
        contenidos_response = requests.get(f"{BASE_URL_CONTENIDOS}/generos/{genero['id']}/contenidos")
        if contenidos_response.ok:
            generos_con_contenidos.append({
                "nombre": genero["nombre"],
                "contenidos": contenidos_response.json()
            })
        else:
            mensajes.append(f"No se pudieron obtener los contenidos para el género {genero['nombre']}.")

    # Si no hay mensajes, significa que todo salió bien
    if not mensajes:
        mensajes.append("Los datos se cargaron correctamente.")

    return {
        "recomendaciones": recomendaciones,
        "tendencias": tendencias,
        "historial": historial,
        "generos_con_contenidos": generos_con_contenidos,
        "mensaje": " | ".join(mensajes)  # Unimos todos los mensajes en una sola cadena
    }

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
    
    # Redirigimos al endpoint de pantalla principal con el `user_id`
    return RedirectResponse(url=f"/pantalla_principal?user_id={user_id}", status_code=303)

@app.get("/admin_login", response_class=HTMLResponse)
async def admin_index(request: Request):
    # Renderiza la página index.html y la devuelve al usuario
    return templates.TemplateResponse("admin_login.html", {"request": request})

# Endpoint para hacer login
@app.post("/admin_login")
async def admin_login(request: Request, email: str = Form(...), password: str = Form(...)):
    # Enviar las credenciales al microservicio para verificar el login
    data = {"email": email, "password": password}
    response = requests.post(f"{BASE_URL_USUARIOS}/usuarios/login", json=data)
    
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Credenciales inválidas")
    
    # Si las credenciales son correctas, obtenemos los datos del usuario
    user_data = response.json()
    user_id = user_data.get("id")
    
    # Redirigimos al endpoint de pantalla principal con el `user_id`
    return RedirectResponse(url=f"/menu_admin?user_id={user_id}", status_code=303)



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

@app.post("/registro")
async def registrar_usuario(
    request: Request, 
    name: str = Form(...), 
    email: str = Form(...), 
    password: str = Form(...), 
    language: str = Form(None), 
    subscription_plan: str = Form(...)
):
    # Datos para el microservicio de usuarios
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
    
    # Redirigimos al endpoint de pantalla principal con el `user_id`
    return RedirectResponse(url=f"/pantalla_principal?user_id={user_id}", status_code=303)


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
    detalles_pelicula["idDirector"] = nombre_director

    #Obtener el reparto
    reparto = requests.get(f"{BASE_URL_CONTENIDOS}/contenidos/{detalles_pelicula["id"]}/reparto")
    detalles_reparto = reparto.json()

    #Obtener los subtitulos
    subtitulos = requests.get(f"{BASE_URL_CONTENIDOS}/contenidos/{detalles_pelicula["idSubtitulosContenido"]}/subtitulos")
    detalles_subtitulos = subtitulos.json()
    
    #Obtener los doblajes
    doblajes = requests.get(f"{BASE_URL_CONTENIDOS}/contenidos/{detalles_pelicula["idDoblajeContenido"]}/doblajes")
    detalles_doblajes = doblajes.json()
    
    # Renderiza la plantilla detalles_pelicula.html con los datos de la película
    return templates.TemplateResponse("detalles_pelicula.html", {
        "request": request,
        "pelicula": detalles_pelicula,
        "reparto": detalles_reparto,
        "subtitulos": detalles_subtitulos,
        "doblajes": detalles_doblajes
    })


@app.get("/buscar", response_class=HTMLResponse)
async def buscar(request: Request, query: str, tipo: str):
    # Realizamos la búsqueda de contenidos o actores según el tipo
    if tipo == "contenido":
        response = requests.get(f"{BASE_URL_CONTENIDOS}/contenidos/{query}/buscar")
    elif tipo == "actor":
        response = requests.get(f"{BASE_URL_CONTENIDOS}/contenidos/{query}/actores")
    else:
        raise HTTPException(status_code=400, detail="Tipo de búsqueda no válido")

    # Si la respuesta no es exitosa (status_code != 200), manejamos el error pero no lanzamos una excepción
    if response.status_code != 200:
        resultados = []
        mensaje = "No se han encontrado resultados."
    else:
        resultados = response.json().get("resultados", [])
        # Si los resultados están vacíos, ponemos el mensaje de "No se han encontrado resultados"
        if not resultados:
            mensaje = "No se han encontrado resultados."
        else:
            mensaje = ""

    # Renderizamos la página con los resultados, ya sea vacíos o con el mensaje
    return templates.TemplateResponse(
        "resultados_busqueda.html",
        {
            "request": request,
            "resultados": resultados,
            "tipo": tipo,
            "query": query,
            "mensaje": mensaje
        }
    ) 
import logging
logging.basicConfig(level=logging.INFO)

@app.get("/pantalla_principal", response_class=HTMLResponse)
async def pantalla_principal(request: Request, user_id: str):
    datos = cargar_datos(user_id)  # Centralizamos la lógica aquí
    mensaje = datos.get("mensaje", "Error al cargar los datos")
    
    # Renderizamos la pantalla principal
    return templates.TemplateResponse(
        "pantalla_principal.html",
        {
            "request": request,
            "user_id": user_id,
            "recomendaciones": datos["recomendaciones"],
            "tendencias": datos["tendencias"],
            "historial": datos["historial"],
            "generos_con_contenidos": datos["generos_con_contenidos"],
            "mensaje": mensaje,
        }
    )

@app.get("/menu_admin", response_class=HTMLResponse)
async def menu_admin(request: Request, user_id: str):
    # Renderizamos el menu de admin.
    return templates.TemplateResponse(
        "menu_admin.html",
        {
            "request": request,
            "user_id": user_id,
        }
    )

@app.get("/usuarios/{user_id}/perfil", response_class=HTMLResponse)
async def get_user_profile(request: Request, user_id: str):
    #Llama al endpoint /perfil para obtener el perfil de un usuario y lo renderiza en HTML
    response = requests.get(f"{BASE_URL_USUARIOS}/usuarios/{user_id}")
    me_gusta_response = requests.get(f"{BASE_URL_INTERACCIONES}/usuarios/{user_id}/me-gusta")
    
    if response.status_code == 200:
        # Obtiene los datos del perfil del usuario
        user_profile = response.json()

        # Inicializa los datos de "Me Gusta"
        contenidos_me_gusta = []
        mensaje_me_gusta = None

        if me_gusta_response.status_code == 200:
            # Obtiene la lista de contenidos "Me Gusta" y la convierte a una lista de objetos ContenidoMeGusta
            me_gusta_data = me_gusta_response.json()
            contenidos_me_gusta = [
                {
                    'id': contenido['id'],
                    'titulo': contenido['titulo'],
                    'descripcion': contenido.get('descripcion', ''),
                    'fechaLanzamiento': contenido['fechaLanzamiento'],
                    'idGenero': contenido['idGenero'],
                    'valoracionPromedio': contenido.get('valoracionPromedio', None),
                    'idSubtitulosContenido': contenido.get('idSubtitulosContenido', None),
                    'idDoblajeContenido': contenido.get('idDoblajeContenido', None)
                }
                for contenido in me_gusta_data
            ]
        else:
            # Si no hay "Me Gusta", guarda un mensaje indicando que no existen
            mensaje_me_gusta = "No existen 'Me Gusta' para este usuario."
        
        # Renderiza la plantilla HTML con los datos del perfil y los "Me Gusta"
        return templates.TemplateResponse(
            "perfil.html",  # Plantilla HTML que renderizará los datos
            {
                "request": request,
                "user_id": user_id,
                "nombre": user_profile['nombre'],
                "email": user_profile['email'],
                "password": user_profile['password'],
                "me_gusta": contenidos_me_gusta,  # Pasa la lista de contenidos "Me Gusta"
                "mensaje_me_gusta": mensaje_me_gusta  # Pasa el mensaje en caso de que no haya "Me Gusta"
            }
        )
    else:
        # En caso de error al obtener los datos del perfil
        error_message = f"Error al obtener el perfil del usuario: {response.status_code}"
        return templates.TemplateResponse(
            "perfil.html",
            {
                "request": request,
                "error_message": error_message,
            }
        )


@app.delete("/interacciones/me-gusta")
async def eliminar_interaccion(request: Request):
    """
    Endpoint para manejar la eliminación de una interacción "Me Gusta"
    en el sistema de interacciones.
    """
    # Leer el cuerpo de la solicitud
    datos = await request.json()

    # Extraer idUsuario e idContenido
    idUsuario = datos.get("idUsuario")
    idContenido = datos.get("idContenido")

    # Validar que los datos requeridos estén presentes
    if not idUsuario or not idContenido:
        raise HTTPException(status_code=400, detail="Faltan datos obligatorios: idUsuario o idContenido")

    # Construir la URL de la API de interacciones
    url = f"{BASE_URL_INTERACCIONES}/usuarios/{idUsuario}/me-gusta/{idContenido}"

    # Realizar la petición DELETE a la API de interacciones
    try:
        response = requests.delete(url)

        # Verificar el estado de la respuesta
        if response.status_code == 200:
            return {"message": "Interacción eliminada correctamente"}
        elif response.status_code == 404:
            raise HTTPException(status_code=404, detail="Interacción no encontrada")
        else:
            raise HTTPException(status_code=500, detail="Error al eliminar la interacción")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al comunicarse con la API de interacciones: {str(e)}")
    
@app.post("/usuarios/{id_usuario}/perfil")
async def actualizar_perfil(request: Request, id_usuario: str):
    """
    Endpoint para actualizar el perfil de un usuario.
    """
    data = await request.form()

    # Extraemos los datos del JSON recibido
    nombre = data.get('name')
    password = data.get('password')
    email = data.get('email')  # Aunque no editable, se puede validar
    idioma = data.get('language')

    # Construir el payload para la API externa
    payload = {
        "nombre": nombre,
        "password": password,
        "email": email,
        "idioma": idioma
    }

    # URL del endpoint de la API externa para actualizar el perfil
    api_url = f"{BASE_URL_USUARIOS}/usuarios/{id_usuario}/perfil"

    try:
        # Enviar la solicitud PUT a la API externa
        response = requests.put(api_url, json=payload)

        # Comprobar el estado de la respuesta de la API
        if response.status_code == 200:
            data = response.json()
            return RedirectResponse(url=f"/usuarios/{id_usuario}/perfil", status_code=303)
        else:
            raise HTTPException(status_code=response.status_code, detail="Error al actualizar el perfil en la API externa")

    except requests.exceptions.RequestException as e:
        # Manejar errores de red o conexión
        raise HTTPException(status_code=500, detail=f"Error al comunicarse con la API externa: {str(e)}")
    

@app.get("/perfil_usuario/{user_id}")
async def obtener_perfil_usuario(user_id: str):
    """
    Obtiene los datos del perfil del usuario desde la API de usuarios.
    """
    try:
        # Hacer una solicitud GET al servicio de usuarios para obtener el perfil
        response = requests.get(f"{BASE_URL_USUARIOS}/usuarios/{user_id}")
        
        if response.status_code != 200:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        # Obtener los datos del usuario
        user_data = response.json()
        
        # Devolver los datos del usuario
        return {
            "nombre": user_data["nombre"],
            "email": user_data["email"],
            "idioma": user_data.get("idioma", "es"),  # Asumir 'es' si no está presente
        }
    except requests.exceptions.RequestException as e:
        # En caso de error al hacer la petición a la API de usuarios
        raise HTTPException(status_code=500, detail=f"Error al obtener el perfil del usuario: {str(e)}")
    

@app.get("/usuarios/{userId}/me-gusta")
def obtener_me_gusta(userId: str):

    try:
        # Hacer una solicitud GET al servicio de usuarios para obtener el perfil
        response = requests.get(f"{BASE_URL_INTERACCIONES}/usuarios/{userId}/me-gusta")
        
        if response.status_code != 200:
            raise HTTPException(status_code=404, detail="No se han encontrado contenidos a los que el usuario le haya dado me gusta")

        # Obtener los datos del usuario
        contenidos = response.json()
        print(contenidos)
        
        # Devolver los datos del usuario
        return contenidos
    except requests.exceptions.RequestException as e:
        # En caso de error al hacer la petición a la API de usuarios
        raise HTTPException(status_code=500, detail=f"Error al obtener el perfil del usuario: {str(e)}")

@app.get("/usuarios/{user_id}/metodos-pago")
async def get_user_payment_methods(user_id: str):
    """
    Este endpoint obtiene los métodos de pago de un usuario a través de la API de usuarios
    y devuelve una lista con los métodos de pago (Tarjeta o PayPal).
    """
    # Hacemos la petición GET a la API de usuarios para obtener los métodos de pago
    try:
        response = requests.get(f"{BASE_URL_USUARIOS}/usuarios/{user_id}/metodos-pago")
        
        # Verificamos si la respuesta fue exitosa
        if response.status_code == 200:
            payment_methods = response.json()
            # Formateamos la respuesta según el esquema necesario
            formatted_methods = []
            for method in payment_methods:
                if method['tipo'] == 'Tarjeta de Crédito':
                    formatted_methods.append({
                        'tipo': method['tipo'],
                        'numeroTarjeta': method.get('numeroTarjeta'),
                        'emailPaypal': None
                    })
                elif method['tipo'] == 'Paypal':
                    formatted_methods.append({
                        'tipo': method['tipo'],
                        'numeroTarjeta': None,
                        'emailPaypal': method.get('emailPaypal')
                    })
            return formatted_methods
        else:
            raise HTTPException(status_code=response.status_code, detail="Error al obtener métodos de pago del usuario")
    
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error al comunicar con la API externa: {str(e)}")

@app.post("/usuarios/{user_id}/metodos-pago")
async def add_payment_method(user_id: str, request: Request):
    try:
        # Obtener los datos del formulario
        form_data = await request.form()
        payment_method = form_data.get("payment-method")
        payment_details = form_data.get("payment-details")

        # Preparar los datos según el tipo de método de pago
        if payment_method == "credit_card":
            numeroTarjeta = form_data.get("numeroTarjeta")
            data = {
                "tipo": "Tarjeta de Crédito",
                "numeroTarjeta": numeroTarjeta,
                "emailPaypal": None  # No se utiliza para tarjeta de crédito
            }
        elif payment_method == "paypal":
            email = form_data.get("email")
            data = {
                "tipo": "Paypal",
                "numeroTarjeta": None,  # No se utiliza para PayPal
                "emailPaypal": email
            }
        else:
            raise HTTPException(status_code=400, detail="Método de pago no válido")

        # Realizar la solicitud POST al servicio de la API de usuarios para agregar el método de pago
        response = requests.post(
            f"{BASE_URL_USUARIOS}/usuarios/{user_id}/metodos-pago",
            json=data
        )

        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Error al agregar el método de pago")
        print("Redirigiendo...")
        return RedirectResponse(url=f"/usuarios/{user_id}/perfil", status_code=303)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Funciones para la gestión del administrador
@app.get("/administrador/series/{idSerie}", response_class=HTMLResponse)
async def get_actualizar_serie(request: Request, idSerie: str):
    response = requests.get(f"{BASE_URL_CONTENIDOS}/series/{idSerie}")
    generos_response = request.get(f"{BASE_URL_CONTENIDOS}/generos")
    
    if response.status_code == 200:
        # Obtiene los datos de la serie
        serie_data = response.json()
        generos = []

        if generos_response.status_code == 200:
            # Obtiene la lista de géneros y la convierte a una lista de objetos Genero
            generos_data = generos_response.json()
            generos = [
                {
                    'id': genero['id'],
                    'nombre': genero['nombre'],
                    'descripcion': genero.get('descripcion', '')
                }
                for genero in generos_data
            ]
        else:
            # En caso de error al obtener los géneros
            error_message = f"Error al obtener los géneros de la base de datos: {response.status_code}"
            return templates.TemplateResponse(
                "admin_actualizar_serie.html",
                {
                    "request": request,
                    "error_message": error_message
                }
            )    

        # Renderiza la plantilla HTML con los datos de la serie
        return templates.TemplateResponse(
            "admin_actualizar_serie.html",  # Plantilla HTML que renderizará los datos
            {
                "request": request,
                "serie_id": idSerie
                "titulo": serie_data['titulo'],
                "descripcion": serie_data['descripcion'],
                "fecLanzamiento": serie_data['fechaLanzamiento'],
                "idGenero": serie_data['idGenero']
                "generos": generos,  # Pasa la lista de todos los géneros para elegir
                "duracion": serie_data['duracion']
            }
        )
    else:
        # En caso de error al obtener los datos de la serie
        error_message = f"Error al obtener los datos de la serie: {response.status_code}"
        return templates.TemplateResponse(
            "admin_actualizar_serie.html",
            {
                "request": request,
                "error_message": error_message,
            }
        )    