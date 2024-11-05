from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import engine, get_db

"""
Autor: Grupo GA01 - ASEE
Versión: 1.0
Descripción: Microservicio de Contenidos con los endpoints

Comando de ejecución: 

"""

#Crear la aplicacion
app = FastAPI(
    title="Microservicio de Contenidos",
    description="API para gestionar los contenidos, actores, directores y categorías.",
    version="1.0.0",
)

models.Base.metadata.create_all(bind=engine)

# Dependency para obtener la sesión de base de datos
def get_database():
    db = next(get_db())
    return db

@app.post("/peliculas", response_model=schemas.Pelicula)
def create_pelicula(pelicula: schemas.PeliculaCreate, db: Session = Depends(get_db)):
    return crud.create_pelicula(db=db, pelicula=pelicula)

@app.post("/series", response_model=schemas.Contenido)
def create_serie(serie: schemas.SerieCreate, db: Session = Depends(get_db)):
    return crud.create_serie(db=db, serie=serie)