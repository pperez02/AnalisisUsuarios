from sqlalchemy.orm import Session
from . import models, schemas

"""
Autor: Grupo GA01 - ASEE
Versión: 1.0
Descripción: Funciones CRUD para interactuar con la base de datos
"""

BASE_URL = "http://127.0.0.1:8000"

# Función para obtener los géneros de los contenidos del historial y "me gusta" de un usuario
def obtener_generos_usuario(db: Session, user_id: str):
    usuario = None
    
    # Obtener el usuario
    response = requests.get(f"{BASE_URL}/usuarios").json()
    for user in response:
        if user.id == user_id:
            usuario = user
    
    # Obtener el historial del usuario
    if usuario:
        historial_id = usuario.idHistorial        

    if historial_id:
        historial = db.query(models.HistorialUsuario).filter(models.HistorialUsuario.idHistorial == historial_id).all()

    # Obtener los géneros de los contenidos en su historial
    generos = []
    if historial:
        for entrada in historial:
            contenido = requests.get(f"{BASE_URL}/contenidos/{entrada.idContenido}").json()
            genero_id = contenido.idGenero
            genero = requests.get(f"{BASE_URL}/generos/{genero_id}").first()

            if genero not in generos:
                generos.append(genero)
    
    # Obtener los contenidos que al usuario le gustan
    me_gusta = db.query(models.ListaMeGusta).filter(models.ListaMeGusta.idUsuario == user_id).all()
    if me_gusta:
        for entrada in me_gusta:
            contenido = requests.get(f"{BASE_URL}/contenidos/{entrada.idContenido}").json()
            genero_id = contenido.idGenero
            genero = requests.get(f"{BASE_URL}/generos/{genero_id}").first()

            if genero not in generos:
                generos.append(genero)            

    # Retornar los géneros adecuados para el usuario
    return generos