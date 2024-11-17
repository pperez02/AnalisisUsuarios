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
def update_content(db: Session, content_id: str, content_data: Union[schemas.PeliculaUpdate, schemas.SerieUpdate]):
    # Buscar el contenido a actualizar en la base de datos
    content = db.query(models.Contenido).filter(models.Contenido.id == content_id).first()
    
    # Si no existe el contenido, se devuelve un None
    if not content:
        return None

    # Convertir los datos en un diccionario, excluyendo los campos no enviados
    update_data = {k: v for k, v in content_data.model_dump(exclude_unset=True).items() if v is not None}
    
    # Actualizar los campos del contenido usando setattr
    for key, value in update_data.items():
        setattr(content, key, value)
    
    # Confirmar los cambios en la base de datos
    db.commit()
    db.refresh(content)
    
    return content
          
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

# Obtiene datos específicos de una Pelicula por id
def get_pelicula_by_id(db: Session, id_contenido: str):
    return db.query(models.Contenido).filter(
        models.Contenido.id == id_contenido,
        models.Contenido.tipoContenido == "Pelicula").first()

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

def get_contenido_by_id(db: Session, id_contenido: str):
    return db.query(models.Contenido).filter(models.Contenido.id == id_contenido).first()    

def get_serie_con_temporadas_episodios(db: Session, idSerie: str):

    serie = db.query(models.Contenido).filter(
        models.Contenido.id == idSerie,
        models.Contenido.tipoContenido == "Serie"
    ).first()

    if not serie:
        return None
    
    #Obtener todas sus temporadas y episodios
    temporadas = db.query(models.Temporada).filter(models.Temporada.idContenido == idSerie).all()
    temporadas_data = []

    for temporada in temporadas:
        episodios = db.query(models.Episodio).filter(models.Episodio.idTemporada == temporada.idTemporada).all()
        
        # Estructura de episodios para la respuesta
        episodios_data = [
            schemas.Episodio(
                idDirector=episodio.idDirector,
                idEpisodio=episodio.idEpisodio,
                duracion=episodio.duracion,
                numeroEpisodio=episodio.numeroEpisodio,
                idContenido=episodio.idContenido,
                idTemporada=episodio.idTemporada
            ) for episodio in episodios
        ]

        # Añadir los datos de la temporada con sus episodios
        temporadas_data.append(schemas.TemporadasGet(
            idTemporada=temporada.idTemporada,
            Episodios=episodios_data
        ))
    return schemas.SeriesGet(
        idSerie=serie.id,
        Temporadas=temporadas_data
    )

def get_all_series_con_temporadas_episodios(db: Session):
    # Obtener todas las series
    series = db.query(models.Contenido).filter(models.Contenido.tipoContenido == "Serie").all()
    series_data = []

    for serie in series:
        # Obtener todas las temporadas para la serie actual
        temporadas = db.query(models.Temporada).filter(models.Temporada.idContenido == serie.id).all()
        temporadas_data = []

        for temporada in temporadas:
            # Obtener todos los episodios para la temporada actual
            episodios = db.query(models.Episodio).filter(models.Episodio.idTemporada == temporada.idTemporada).all()
            
            # Estructura de episodios para la respuesta
            episodios_data = [
                schemas.Episodio(
                    idDirector=episodio.idDirector,
                    idEpisodio=episodio.idEpisodio,
                    duracion=episodio.duracion,
                    numeroEpisodio=episodio.numeroEpisodio,
                    idContenido=episodio.idContenido,
                    idTemporada=episodio.idTemporada
                ) for episodio in episodios
            ]

            # Añadir los datos de la temporada con sus episodios
            temporadas_data.append(schemas.TemporadasGet(
                idTemporada=temporada.idTemporada,
                Episodios=episodios_data
            ))

        # Añadir los datos de la serie con sus temporadas
        series_data.append(schemas.SeriesGet(
            idSerie=serie.id,
            Temporadas=temporadas_data
        ))

    return series_data  # Devolver todas las series con temporadas y episodios

# Función para obtener una temporada por idContenido y idTemporada
def get_temporada(db: Session, idContenido: str, idTemporada: str):
    return db.query(models.Temporada).filter(
        models.Temporada.idContenido == idContenido,
        models.Temporada.idTemporada == idTemporada
    ).first()

# Función para actualizar una temporada
def update_temporada(db: Session, idContenido: str, idTemporada: str, temporada: schemas.TemporadaUpdate):
    temporada_query = db.query(models.Temporada).filter(
        models.Temporada.idContenido == idContenido,
        models.Temporada.idTemporada == idTemporada
    ).first()
    if temporada_query:
        temporada_query.numeroTemporada = temporada.numeroTemporada
        db.commit()
        db.refresh(temporada_query)
    return temporada_query

# Función para obtener un episodio por idContenido, idTemporada e idEpisodio
def get_episodio(db: Session, idContenido: str, idTemporada: str, idEpisodio: str):
    return db.query(models.Episodio).filter(
        models.Episodio.idContenido == idContenido,
        models.Episodio.idTemporada == idTemporada,
        models.Episodio.idEpisodio == idEpisodio
    ).first()

# Función para actualizar un episodio
def update_episodio(db: Session,  idContenido: str, idTemporada: str, idEpisodio: str, episodio_nuevo: schemas.EpisodioUpdate):
    
    episodio_actual = get_episodio(db=db, idContenido=idContenido, idTemporada=idTemporada, idEpisodio=idEpisodio)
    if not episodio_actual:
        return None
    if episodio_nuevo.numeroEpisodio:
        episodio_actual.numeroEpisodio = episodio_nuevo.numeroEpisodio
    if episodio_nuevo.duracion:
        episodio_actual.duracion = episodio_nuevo.duracion
    if episodio_nuevo.idDirector:
        episodio_actual.idDirector = episodio_nuevo.idDirector
    db.commit()
    db.refresh(episodio_actual)

    return episodio_actual


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
def update_genero(db: Session, genero_id: str, genero: schemas.GeneroUpdate):
    # Asegúrate de que 'nombre' y 'descripcion' son de tipo string
    nombre = genero.nombre if isinstance(genero.nombre, str) else str(genero.nombre)
    descripcion = genero.descripcion if isinstance(genero.descripcion, str) else str(genero.descripcion)
    
    # Realiza la actualización usando valores seguros
    db_genero = db.query(models.Genero).filter(models.Genero.id == genero_id).first()
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

# Función para obtener los contenidos de un género específico
def get_contenidos_por_genero(db: Session, idGenero: str)
    return db.query(models.Contenido).filter(models.Contenido.idGenero == genero_id).all()    