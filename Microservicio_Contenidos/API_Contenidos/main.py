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
    # Si no todos los campos son enviados mediante el cliente, el metodo debe recibir un "None"
    pelicula = crud.update_content(db=db, content_id=idPelicula, content_data=pelicula_data)
    if pelicula is None:
        raise HTTPException(status_code=404, detail="Película no encontrada")
    return {"message": "Datos de película actualizados exitosamente"}

@app.put("/series/{idSerie}")
def update_serie(idSerie: str, serie_data: schemas.SerieUpdate, db: Session = Depends(get_db)):
    serie = crud.update_content(db=db, content_id=idSerie, content_data=serie_data)
    if serie is None:
        raise HTTPException(status_code=404, detail="Serie no encontrada")
    return {"message": "Datos de serie actualizados exitosamente"}

@app.post("/contenidos/{idContenido}/subtitulos/{idSubtitulo}")
def update_subtitulos(idContenido: str, idSubtitulo: str, db: Session = Depends(get_db)):
    return crud.update_subtitulo(db=db, content_id=idContenido, subtitulo_id=idSubtitulo)  

@app.get("/contenidos/{idContenido}/subtitulos")
def get_subtitulos(idContenido: str, db: Session = Depends(get_db)):
    return crud.get_subtitulos(db=db, idContenido=idContenido)

@app.post("/contenidos/{idContenido}/doblajes/{idDoblaje}")
def update_doblaje(idContenido: str, idDoblaje: str, db: Session = Depends(get_db)):
    return crud.update_doblaje(db=db, content_id=idContenido, doblaje_id=idDoblaje)

@app.get("/contenidos/{idContenido}/doblajes")
def get_doblajes(idContenido: str, db: Session = Depends(get_db)):
    return crud.get_doblajes(db=db, idContenido=idContenido) 

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
    
@app.get("/peliculas/{idContenido}", response_model=schemas.Contenido)
def get_peliculas(idContenido: str, db: Session = Depends(get_db)):
    # Llamada al CRUD para obtener el contenido por id
    contenido = crud.get_pelicula_by_id(db=db, id_contenido=idContenido)    
    # Si no se encuentra el contenido, se lanza una excepción 404
    if not contenido:
        raise HTTPException(status_code=404, detail="Pelicula no encontrada")    
    return contenido

@app.get("/contenidos", response_model=list[schemas.Contenido])
def obtener_todos_los_contenidos(db: Session = Depends(get_db)):
    contenidos = crud.get_all_contenidos(db)
    return contenidos

@app.get("/contenidos/{idContenido}", response_model=schemas.Contenido)
def get_contenido(idContenido: str, db: Session = Depends(get_db)):
    # Llamada al CRUD para obtener el contenido por id
    contenido = crud.get_contenido_by_id(db=db, id_contenido=idContenido)    
    # Si no se encuentra el contenido, se lanza una excepción 404
    if not contenido:
        raise HTTPException(status_code=404, detail="Contenido no encontrado")    
    return contenido

@app.get("/series/{idSerie}", response_model=schemas.SeriesGet)
def get_series(idSerie: str, db: Session = Depends(get_db)):
    serie = crud.get_serie_con_temporadas_episodios(db=db, idSerie=idSerie)
    if not serie:
        raise HTTPException(status_code=404, detail="Serie no encontrada")  
    return serie

@app.get("/series", response_model=list[schemas.SeriesGet])
def get_all_series(db: Session = Depends(get_db)):
    series = crud.get_all_series_con_temporadas_episodios(db=db)

    if not series:
        raise HTTPException(status_code=404, detail="No existen series")
    
    return series

@app.get("/contenidos/{idContenido}/temporadas/{idTemporada}", response_model=schemas.Temporada)
def get_temporada(idContenido: str, idTemporada: str, db: Session = Depends(get_db)):
    temporada = crud.get_temporada(db=db, idContenido=idContenido, idTemporada=idTemporada)
    if not temporada:
        raise HTTPException(status_code=404, detail="Temporada no encontrada")
    return temporada

@app.put("/contenidos/{idContenido}/temporadas/{idTemporada}")
def update_temporada(idContenido: str, idTemporada: str, temporada_data: schemas.TemporadaUpdate, db: Session = Depends(get_db)):
    temporada = crud.update_temporada(db=db, idContenido=idContenido, idTemporada=idTemporada, temporada=temporada_data)
    if not temporada:
        raise HTTPException(status_code=404, detail="Temporada no encontrada")
    return {"message": "Temporada actualizada exitosamente"}

@app.get("/contenidos/{idContenido}/temporadas/{idTemporada}/episodios/{idEpisodio}", response_model=schemas.Episodio)
def get_episodio(idContenido: str, idTemporada: str, idEpisodio: str, db: Session = Depends(get_db)):
    episodio = crud.get_episodio(db=db, idContenido=idContenido, idTemporada=idTemporada, idEpisodio=idEpisodio)
    if not episodio:
        raise HTTPException(status_code=404, detail="Episodio no encontrado")
    return episodio

@app.put("/contenidos/{idContenido}/temporadas/{idTemporada}/episodios/{idEpisodio}")
def update_episodio(idContenido: str, idTemporada: str, idEpisodio: str, episodio_data: schemas.EpisodioUpdate, db: Session = Depends(get_db)):
    episodio_nuevo = crud.update_episodio(db=db, idContenido=idContenido, idTemporada=idTemporada, idEpisodio=idEpisodio, episodio_nuevo=episodio_data)
    if not episodio_nuevo:
        raise HTTPException(status_code=404, detail="Episodio no actualizado")
    return {"message": "Episodio actualizado exitosamente"}


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

@app.get("/generos/{idGenero}/contenidos", response_model=list[schemas.Contenido])
def get_contenidos_genero(idGenero: str, db: Session = Depends(get_db)):
    contenidos = crud.get_contenidos_por_genero(db=db, idGenero=idGenero)
    if not contenidos:
        raise HTTPException(status_code=404, detail="No existe ningún contenido con ese genero")
    return contenidos 

# Endpoint para asignar una nueva valoración a un contenido y recalcular el promedio
@app.put("/contenidos/{idContenido}/valoracion")
def actualizar_valoracion_contenido(idContenido: str, valoracion: int, db: Session = Depends(get_db)):
    valoracion_contenido = crud.valorar_contenido(db=db, idContenido=idContenido, valoracion=valoracion)
    if not valoracion_contenido:
        raise HTTPException(status_code=404, detail="Contenido no encontrado")
    return {"message": "Valoración del contenido actualizada exitosamente"} 

#Endpoint para buscar contenidos por: titulo, genero 
@app.get("/contenidos/{busqueda}/buscar")
def buscar_contenidos(busqueda: str, db: Session = Depends(get_db)):
    contenidos = crud.obtener_contenidos_busqueda(db=db, busqueda=busqueda)
    if not contenidos:
        raise HTTPException(status_code=404, detail="No existen resultados para esa búsqueda")
    return {"resultados": contenidos}

#Endpoint para buscar actores por: nombre
@app.get("/contenidos/{busqueda}/actores")
def buscar_actores(busqueda: str, db: Session = Depends(get_db)):
    actores = crud.obtener_actores_busqueda(db=db, busqueda=busqueda)
    if not actores:
        raise HTTPException(status_code=404, detail="No existen actores para esa búsqueda")
    return {"resultados": actores}

    
# Endpoint para obtener el reparto de un contenido

@app.get("/contenidos/{idContenido}/reparto")
def get_reparto(idContenido: str, db: Session = Depends(get_db)):
    reparto = crud.get_reparto(db=db, idContenido=idContenido)
    if not reparto:
         raise HTTPException(status_code=404, detail="No se ha podido recuperar reparto")
    return reparto
#Asociar actores a una pelicula. Param: NO lista de actores, un solo actor (idActor)
@app.post("/contenidos/{idContenido}/reparto/{idActor}", response_model=schemas.Reparto)
def update_reparto(idContenido: str, idActor: str, db: Session = Depends(get_db)):
    reparto = crud.update_reparto(db=db, idContenido=idContenido, idActor=idActor)

    if not reparto:
        raise HTTPException(status_code=404, detail="No se ha podido asociar actores a pelicula")
    return reparto

#Funciones para obtener la información de un actor/director por su ID
@app.get("/actores/{idActor}", response_model=schemas.Actor)
def get_actor(idActor: str, db: Session = Depends(get_db)):
    actor = crud.get_actor(db=db, idActor=idActor)
    if actor is None:
        raise HTTPException(status_code=404, detail="Actor no encontrado")
    return actor

@app.get("/directores/{idDirector}", response_model=schemas.Director)
def get_director(idDirector: str, db: Session = Depends(get_db)):
    director = crud.get_director(db=db, idDirector=idDirector)
    if director is None:
        raise HTTPException(status_code=404, detail="Director no encontrado")
    return director

#Funciones para obtener los contenidos relacionados con un actor/director por su ID
@app.get("/actores/{idActor}/contenidos")
def get_content_by_actor(idActor: str, db: Session = Depends(get_db)):
    content = crud.get_content_by_actor(db=db, idActor=idActor)
    return content

@app.get("/directores/{idDirector}/contenidos")
def get_content_by_director(idDirector: str, db: Session = Depends(get_db)):
    content = crud.get_content_by_director(db=db, idDirector=idDirector)
    return content

#Funciones para obtener los actores/director relacionados con un contenido
@app.get("/contenidos/{idContenido}/reparto")
def get_actors_by_content(idContenido: str, db: Session = Depends(get_db)):
    actors = crud.get_actors_by_content(db=db, idContenido=idContenido)
    return actors

@app.get("/contenidos/{idContenido}/director")
def get_director_by_content(idContenido: str, db: Session = Depends(get_db)):
    director = crud.get_director_by_content(db=db, idContenido=idContenido)
    return director