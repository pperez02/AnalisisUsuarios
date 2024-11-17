from sqlalchemy.orm import Session
from . import models, schemas

"""
Autor: Grupo GA01 - ASEE
Versión: 1.0
Descripción: Funciones CRUD para interactuar con la base de datos
"""

BASE_URL = "http://127.0.0.1:8000"

# Función para obtener los géneros de los contenidos del historial y "me gusta" de un usuario
def get_generos_usuario(db: Session, usuario_id: str):
    usuario = None
    generos_puntos = {}
    
    # Obtener el usuario
    response = requests.get(f"{BASE_URL}/usuarios").json()
    for user in response:
        if user.id == usuario_id:
            usuario = user
    
    # Obtener el historial del usuario
    if usuario:
        historial_id = usuario.idHistorial        

    if historial_id:
        historial = db.query(models.HistorialUsuario).filter(models.HistorialUsuario.idHistorial == historial_id).all()

    # Obtener los géneros de los contenidos en su historial
    if historial:
        for entrada in historial:
            contenido = requests.get(f"{BASE_URL}/contenidos/{entrada.idContenido}").json()
            genero_id = contenido.idGenero

            if genero_id:
                if genero_id not in generos_puntos:
                    generos_puntos[genero_id] = 1
                else:
                    generos_puntos[genero_id] += 1   
    
    # Obtener los contenidos que al usuario le gustan
    me_gusta = db.query(models.ListaMeGusta).filter(models.ListaMeGusta.idUsuario == usuario_id).all()
    if me_gusta:
        for entrada in me_gusta:
            contenido = requests.get(f"{BASE_URL}/contenidos/{entrada.idContenido}").json()
            genero_id = contenido.idGenero

            if genero_id:
                if genero_id not in generos_puntos:
                    generos_puntos[genero_id] = 1
                else:
                    generos_puntos[genero_id] += 1 

    # Ordenar los géneros por el número de repeticiones de mayor a menor
    generos_ordenados = sorted(generos_puntos.items(), key=lambda x: x[1], reverse=True)

    # Quedarse solo con los dos más repetidos para las recomendaciones
    top_2_generos = [genero for genero, _ in generos_ordenados[:2]]                          

    # Retornar los géneros
    return top_2_generos

# Función para obtener contenidos de los dos géneros favoritos de un usuario
def get_recomendaciones_usuario(db: Session, usuario_id: str):
    # Obtenemos los dos géneros favoritos del usuario
    generos = get_generos_usuario(db, usuario_id)
    
    # Obtenemos la lista de contenidos en función de esos géneros
    recomedaciones = []
    if generos:
        lista1 = requests.get(f"{BASE_URL}/generos/{generos[0].id}").json()
        lista2 = requests.get(f"{BASE_URL}/generos/{generos[1].id}").json()
        recomendaciones.extend(lista1)
        recomendaciones.extend(lista2)

    return recomendaciones        