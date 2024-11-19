from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import engine, get_db, initialize_database

"""
Autor: Grupo GA01 - ASEE
Versión: 1.0
Descripción: Microservicio de Usuarios con los endpoints

Comando de ejecución: 

"""

#Crear la aplicacion
app = FastAPI(
    title="Microservicio de Interacciones",
    description="API para gestionar las recomendaciones e interacciones de usuarios y contenido multimedia.",
    version="1.0.0",
)

# Crear la base de datos
initialize_database()

# Dependency para obtener la sesión de base de datos
def get_database():
    db = next(get_db())
    return db

@app.get("/usuarios/{idUsuario}/recomendaciones", response_model=list[schemas.Contenido])
def get_recomendaciones(idUsuario: str, db: Session = Depends(get_db)):
    recomendaciones = crud.get_recomendaciones_usuario(db=db, usuario_id=idUsuario)
    if not recomendaciones:
        raise HTTPException(status_code=404, detail="No se pudieron recuperar las recomendaciones")
    return contenidos    