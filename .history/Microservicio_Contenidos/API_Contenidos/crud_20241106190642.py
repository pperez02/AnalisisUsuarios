from sqlalchemy.orm import Session
from . import models, schemas
import uuid

# Función para crear una película
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

# Función para crear una serie
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

# Función para actualizar un contenido
def update_content(db: Session, content_id: str, content: schemas.ContenidoUpdate):
    content_query = db.query(models.Contenido).filter(models.Contenido.id == content_id).first()
    if content_query:
        content_query.tipoContenido = content.tipoContenido
        content_query.titulo = content.titulo
        content_query.descripcion = content.descripcion
        content_query.fechaLanzamiento = content.fechaLanzamiento
        content_query.idGenero = content.idGenero
        content_query.valoracionPromedio = content.valoracionPromedio
        content_query.idSubtitulosContenido = content.idSubtitulosContenido
        content_query.idDoblajeContenido = content.idDoblajeContenido
        if content.tipoContenido == "Pelicula":
            content_query.duracion = content.duracion
            content_query.idDirector = content.idDirector
        db.commit()
        db.refresh(content_query)
    return content_query           

# Función para añadir subtítulos a un contenido
def update_subtitulo(db: Session, content_id: str, subtitulo_id: str):
    content_query = db.query(models.Contenido).filter(models.Contenido.id == content_id).first()
    subtitulo_query = db.query(models.Subtitulo).filter(models.Subtitulo.idSubtitulo == subtitulo_id).first()
    if content_query and subtitulo_query:
        db_SubtituloContenido = models.SubtituloContenido (
            idSubtitulosContenido = content_query.idSubtitulosContenido,
            idSubtitulo = subtitulo_query.idSubtitulo
        )
        db.add(db_SubtituloContenido)
        db.commit()
        db.refresh(db_SubtituloContenido)

    return db_SubtituloContenido

# Función para añadir doblajes a un contenido
def update_doblaje(db: Session, content_id: str, doblaje_id: str):
    content_query = db.query(models.Contenido).filter(models.Contenido.id == content_id).first()
    doblaje_query = db.query(models.Doblaje).filter(models.Doblaje.idDoblaje == doblaje_id).first()
    if content_query and doblaje_query:
        db_DoblajeContenido = models.DoblajeContenido (
            idDoblajeContenido = content_query.idDoblajeContenido,
            idDoblaje = doblaje_query.idDoblaje
        )
        db.add(db_DoblajeContenido)
        db.commit()
        db.refresh(db_DoblajeContenido)

    return db_DoblajeContenido    