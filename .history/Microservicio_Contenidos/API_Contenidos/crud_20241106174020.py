from sqlalchemy.orm import Session
from . import models, schemas
import uuid

# Crear una película
def create_pelicula(db: Session, pelicula: schemas.PeliculaCreate):  
    db_contenido = models.Contenido (
        tipoContenido="Pelicula",
        titulo=pelicula.titulo,
        descripcion=pelicula.descripcion,
        fechaLanzamiento=pelicula.fechaLanzamiento,
        idGenero=pelicula.idGenero,
        valoracionPromedio=pelicula.valoracionPromedio,
        idSubtitulosContenido=pelicula.idSubtitulosContenido,
        idDoblajeContenido=pelicula.idDoblajeContenido,
        duracion=pelicula.duracion,
        idDirector=pelicula.idDirector
    )
    db.add(db_contenido)
    db.commit()
    db.refresh(db_contenido)
    
    return db_contenido

# Crear una serie
def create_serie(db: Session, serie: schemas.ContenidoBase):
    
    db_serie = models.Contenido (
        tipoContenido="Serie",
        titulo=serie.titulo,
        descripcion=serie.descripcion,
        fechaLanzamiento=serie.fechaLanzamiento,
        idGenero=serie.idGenero,
        valoracionPromedio=serie.valoracionPromedio,
        idSubtitulosContenido=serie.idSubtitulosContenido,
        idDoblajeContenido=serie.idDoblajeContenido,
        duracion=None,
        idDirector=None
    )
    db.add(db_serie)
    db.commit()
    db.refresh(db_serie)

    return db_serie
