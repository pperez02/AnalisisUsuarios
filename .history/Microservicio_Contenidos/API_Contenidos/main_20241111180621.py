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

@app.post("/contenidos/{idContenido}/temporadas", response_model=schemas.Temporada)
def create_temporada(idContenido: str, temporada: schemas.TemporadaCreate, db: Session = Depends(get_db)):
    return crud.create_temporada(db=db, temporada=temporada, idContenido=idContenido)

@app.post("/contenidos/{idContenido}/temporadas/{idTemporada}/episodios", response_model=schemas.Episodio)
def create_episodio(idContenido: str, idTemporada: str, episodio: schemas.EpisodioCreate, db: Session = Depends(get_db)):
    return crud.create_episodio(db=db, episodio=episodio, idContenido=idContenido, idTemporada=idTemporada)

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

# Nuevo endpoint para eliminar contenido en distintos niveles
@app.delete("/contenidos/{idContenido}/temporadas/{idTemporada}/episodios/{idEpisodio}", tags=["Eliminar contenido"])
@app.delete("/contenidos/{idContenido}/temporadas/{idTemporada}", tags=["Eliminar contenido"])
@app.delete("/contenidos/{idContenido}", tags=["Eliminar contenido"])
def delete_content(
    idContenido: str, 
    idTemporada: str = None, 
    idEpisodio: str = None, 
    db: Session = Depends(get_db)
):
    if idEpisodio:
        # Eliminar episodio
        success = crud.delete_episode(db=db, idContenido=idContenido, idTemporada=idTemporada, idEpisodio=idEpisodio)
        if not success:
            raise HTTPException(status_code=404, detail="Episodio no encontrado")
        return {"message": "Episodio eliminado exitosamente"}

    elif idTemporada:
        # Eliminar temporada
        success = crud.delete_season(db=db, idContenido=idContenido, idTemporada=idTemporada)
        if not success:
            raise HTTPException(status_code=404, detail="Temporada no encontrada")
        return {"message": "Temporada eliminada exitosamente"}

    else:
        # Eliminar película o serie
        success = crud.delete_content(db=db, idContenido=idContenido)
        if not success:
            raise HTTPException(status_code=404, detail="Contenido no encontrado")
        return {"message": "Contenido eliminado exitosamente"}
    
@app.get("/contenidos/{idContenido}", response_model=schemas.Contenido)
def get_contenido(idContenido: str, db: Session = Depends(get_db)):
    # Llamada al CRUD para obtener el contenido por id
    contenido = crud.get_contenido_by_id(db=db, id_contenido=idContenido)
    
    # Si no se encuentra el contenido, se lanza una excepción 404
    if not contenido:
        raise HTTPException(status_code=404, detail="Contenido no encontrado")
    
    return contenido

@app.get("/contenidos", response_model=list[schemas.Contenido])
def obtener_todos_los_contenidos(db: Session = Depends(get_db)):
    contenidos = crud.get_all_contenidos(db)
    return contenidos

@app.get("/generos/{idGenero}", response_model=schemas.Genero)
def get_genero(idGenero: str, db: Session = Depends(get_db)):
    genero = crud.get_genero(db=db, genero_id=idGenero)
    return genero

@app.post("/generos", response_model=schemas.Genero)
def create_genero(genero: schemas.GeneroCreate, db: Session = Depends(get_db)):
    return crud.create_genero(db=db, genero=genero)

@app.put("/generos/{idGenero}")
def update_genero(idGenero: str, genero_data: schemas.GeneroUpdate, db: Session = Depends(get_db)):
    genero = crud.update_genero(db=db, genero_id=idGenero, genero=genero_data)
    if genero is None:
        raise HTTPException(status_code=404, detail="Género no encontrado")
    return {"message": "Datos del género actualizados exitosamente"}            

@app.delete("/generos/{idGenero}")
def delete_genero(idGenero: str, db: Session = Depends(get_db)):
    success = crud.delete_genero(db=db, genero_id=idGenero)
    if not success:
        raise HTTPException(status_code=404, detail="Género no encontrado")
    return {"message": "Género eliminado exitosamente"}        