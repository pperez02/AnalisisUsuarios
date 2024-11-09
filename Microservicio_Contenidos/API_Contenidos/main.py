from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import engine, get_db, initialize_database

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

initialize_database()

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

@app.put("/peliculas/{idPelicula}")
def update_pelicula(idPelicula: str, pelicula_data: schemas.PeliculaUpdate, db: Session = Depends(get_db)):
    pelicula = crud.update_content(db=db, content_id=idPelicula, content=pelicula_data)
    if pelicula is None:
        raise HTTPException(status_code=404, detail="Película no encontrada")
    return {"message": "Datos de película actualizados exitosamente"}

@app.put("/series/{idSerie}")
def update_serie(idSerie: str, serie_data: schemas.SerieUpdate, db: Session = Depends(get_db)):
    serie = crud.update_content(db=db, content_id=idSerie, content=serie_data)
    if serie is None:
        raise HTTPException(status_code=404, detail="Serie no encontrada")
    return {"message": "Datos de serie actualizados exitosamente"}

@app.post("/contenidos/{idContenido}/subtitulos/{idSubtitulo}")
def update_subtitulos(idContenido: str, idSubtitulo: str, db: Session = Depends(get_db)):
    return crud.update_subtitulo(db=db, content_id=idContenido, subtitulo_id=idSubtitulo)   

@app.post("/contenidos/{idContenido}/doblajes/{idDoblaje}")
def update_doblaje(idContenido: str, idDoblaje: str, db: Session = Depends(get_db)):
    return crud.update_doblaje(db=db, content_id=idContenido, doblaje_id=idDoblaje) 