from sqlalchemy.orm import Session
from . import models, schemas
import uuid
from typing import Union

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

# Función para crear una temporada
def create_temporada(db: Session, temporada: schemas.TemporadaCreate, idContenido: str):
    db_temporada = models.Temporada(
        idContenido=idContenido,
        numeroTemporada=temporada.numeroTemporada
    )
    db.add(db_temporada)
    db.commit()
    db.refresh(db_temporada)
    return db_temporada

# Función para crear un episodio
def create_episodio(db: Session, episodio: schemas.EpisodioCreate, idContenido: str, idTemporada: str):
    db_episodio = models.Episodio(
        idContenido=idContenido,
        idTemporada=idTemporada,
        idDirector=episodio.idDirector,
        numeroEpisodio=episodio.numeroEpisodio,
        duracion=episodio.duracion
    )
    db.add(db_episodio)
    db.commit()
    db.refresh(db_episodio)
    return db_episodio

# Función para actualizar un contenido
def update_content(db: Session, content_id: str, content: Union[schemas.PeliculaUpdate, schemas.SerieUpdate]):
    content_query = db.query(models.Contenido).filter(models.Contenido.id == content_id).first()
    if content_query:
        # Actualiza los campos comunes a ambos tipos
        content_query.titulo = content.titulo
        content_query.descripcion = content.descripcion
        content_query.fechaLanzamiento = content.fechaLanzamiento
        content_query.idGenero = content.idGenero
        content_query.valoracionPromedio = content.valoracionPromedio
        content_query.idSubtitulosContenido = content.idSubtitulosContenido
        content_query.idDoblajeContenido = content.idDoblajeContenido

        # Solo para las películas, actualiza `duracion` e `idDirector`
        if isinstance(content, schemas.PeliculaUpdate):
            if content.duracion is not None:
                content_query.duracion = content.duracion
            if content.idDirector is not None:
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

# Función para eliminar una película o serie
def delete_content(db: Session, idContenido: str) -> bool:
    content = db.query(models.Contenido).filter(models.Contenido.id == idContenido).first()
    if content:
        db.delete(content)
        db.commit()
        return True
    return False

# Función para eliminar una temporada de una serie
def delete_season(db: Session, idContenido: str, idTemporada: str) -> bool:
    season = db.query(models.Temporada).filter(
        models.Temporada.idContenido == idContenido,
        models.Temporada.idTemporada == idTemporada
    ).first()
    if season:
        db.delete(season)
        db.commit()
        return True
    return False

# Función para eliminar un episodio de una temporada específica
def delete_episode(db: Session, idContenido: str, idTemporada: str, idEpisodio: str) -> bool:
    episode = db.query(models.Episodio).filter(
        models.Episodio.idContenido == idContenido,
        models.Episodio.idTemporada == idTemporada,
        models.Episodio.idEpisodio == idEpisodio
    ).first()
    if episode:
        db.delete(episode)
        db.commit()
        return True
    return False

# Consulta de contenido por id
def get_contenido_by_id(db: Session, id_contenido: str):
    # Consulta general para obtener el tipo de contenido y otros datos básicos
    contenido = db.query(models.Contenido).filter(models.Contenido.id == id_contenido).first()
    
    if not contenido:
        return None
    
    # Diferenciación entre Pelicula y Serie
    if contenido.tipoContenido == "Pelicula":
        return get_pelicula_by_id(db, id_contenido)
    elif contenido.tipoContenido == "Serie":
        return get_serie_by_id(db, id_contenido)
    else:
        return contenido

# Obtiene datos específicos de una Pelicula por id
def get_pelicula_by_id(db: Session, id_contenido: str):
    return db.query(models.Contenido).filter(models.Contenido.id == id_contenido and models.Contenido.tipoContenido == "Pelicula").first()

# Obtiene datos específicos de una Serie por id
def get_serie_by_id(db: Session, id_contenido: str):
    return db.query(models.Contenido).filter(models.Contenido.id == id_contenido and models.Contenido.tipoContenido == "Serie").first()

# Consulta de todos los contenidos
def get_all_contenidos(db: Session):
    # Obtener todos los contenidos generales (Peliculas o Series)
    contenidos = db.query(models.Contenido).all()
    
    # Crear una lista para almacenar los resultados
    resultado_contenidos = []

    # Iterar sobre cada contenido y diferenciar si es Pelicula o Serie
    for contenido in contenidos:
        if contenido.tipoContenido == "Pelicula":
            pelicula = get_pelicula_by_id(db, contenido.id)  # Obtener detalles de la Película
            if pelicula:
                resultado_contenidos.append(pelicula)
        elif contenido.tipoContenido == "Serie":
            serie = get_serie_by_id(db, contenido.id)  # Obtener detalles de la Serie
            if serie:
                resultado_contenidos.append(serie)

    return resultado_contenidos

# Función para consultar los datos de un género
def get_genero(db: Session, genero_id: str):
    return db.query(models.Genero).filter(models.Genero.id == genero_id).first()
    
# Función para crear un nuevo género de contenido
def create_genero(db: Session, genero: schemas.GeneroCreate):
    db_genero = models.Genero(
        nombre=genero.nombre,
        descripcion=genero.descripcion
    )
    db.add(db_genero)
    db.commit()
    db.refresh(db_genero)
    return db_genero

# Función para actualizar un género existente
def update_genero(db: Session, genero_id: str, genero: GeneroUpdate):
    # Asegúrate de que 'nombre' y 'descripcion' son de tipo string
    nombre = genero.nombre if isinstance(genero.nombre, str) else str(genero.nombre)
    descripcion = genero.descripcion if isinstance(genero.descripcion, str) else str(genero.descripcion)
    
    # Realiza la actualización usando valores seguros
    db_genero = db.query(Genero).filter(Genero.id == genero_id).first()
    if db_genero:
        db_genero.nombre = nombre
        db_genero.descripcion = descripcion
        db.commit()
        db.refresh(db_genero)
    return db_genero

# Función para eliminar un género existente
def delete_genero(db: Session, genero_id: str) -> bool:
    genero = db.query(models.Genero).filter(models.Genero.id == genero_id).first()
    if genero:
        db.delete(genero)
        db.commit()
        return True
    return False    