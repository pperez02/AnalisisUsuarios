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

def get_subtitulos(db: Session, idContenido: str):
    # Realizamos la consulta uniendo las tablas SubtituloContenido y Subtitulo por idSubtitulo
    subtitulos = (
        db.query(models.Subtitulo)  # Seleccionamos la tabla Subtitulo desde models
        .join(models.SubtituloContenido, models.SubtituloContenido.idSubtitulo == models.Subtitulo.idSubtitulo)  # Unimos SubtituloContenido con Subtitulo
        .filter(models.SubtituloContenido.idSubtitulosContenido == idContenido)  # Filtramos por idContenido
        .all()  # Ejecutamos la consulta y obtenemos todos los resultados
    )
    return subtitulos

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

#Funcion para obtener los doblajes
def get_doblajes(db: Session, idContenido: str):
    # Realizamos la consulta uniendo las tablas DoblajesContenido y Doblajes por idDoblaje
    doblajes = (
        db.query(models.Doblaje)  # Seleccionamos la tabla Doblaje desde models
        .join(models.DoblajeContenido, models.DoblajeContenido.idDoblaje == models.Doblaje.idDoblaje)  # Unimos SubtituloContenido con Subtitulo
        .filter(models.DoblajeContenido.idDoblajeContenido == idContenido)  # Filtramos por idContenido
        .all()  # Ejecutamos la consulta y obtenemos todos los resultados
    )
    return doblajes  

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

# Consulta de todas las series
def get_todoseries(db: Session):
    return db.query(models.Contenido).filter(models.Contenido.tipoContenido == "Serie")

# Consulta de todas las series
def get_todopeliculas(db: Session):
    return db.query(models.Contenido).filter(models.Contenido.tipoContenido == "Pelicula")

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

# Función para consultar todos los géneros de la base de datos
def get_generos(db: Session):
    return db.query(models.Genero).all()

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

#Funcion para obtener el reparto
def get_reparto(db: Session, idContenido: str):
    # Realizamos la consulta uniendo las tablas Reparto y Actor por idActor
    reparto = (
        db.query(models.Actor)  # Seleccionamos la tabla Actor
        .join(models.Reparto, models.Reparto.idActor == models.Actor.id)  # Unimos Reparto con Actor
        .filter(models.Reparto.idContenido == idContenido)  # Filtramos por idContenido
        .all()  # Ejecutamos la consulta y obtenemos todos los resultados
    )
    return reparto

#Funcion para actualizar el reparto
def update_reparto(db: Session, idContenido: str, idActor: str):
    db_contenido = db.query(models.Contenido).filter(models.Contenido.id == idContenido).first()
    db_actor = db.query(models.Actor).filter(models.Actor.id == idActor).first()
    if db_contenido and db_actor:
        db_reparto = models.Reparto (
            idContenido = db_contenido.id,
            idActor = db_actor.id
        )
        db.add(db_reparto)
        db.commit()
        db.refresh(db_reparto)

    return db_reparto

def get_actor(db: Session, idActor: str):
    actor = db.query(models.Actor).filter(models.Actor.id == idActor).first()
    return actor

def get_director(db: Session, idDirector: str):
    director = db.query(models.Director).filter(models.Director.id == idDirector).first()
    return director

def get_content_by_actor(db: Session, idActor: str):
    #Obtener los idContenido de Reparto en los que existe el idActor
    idsContenido_by_actor = db.query(models.Reparto.idContenido).filter(models.Reparto.idActor == idActor).all()

    #Extraer solo los idContenido de los resultados obtenidos
    contenido_ids = [contenido.idContenido for contenido in idsContenido_by_actor]

    #Recuperar los contenidos correspondientes a esos idContenido
    contenidos = db.query(models.Contenido).filter(models.Contenido.id.in_(contenido_ids)).all()

    return contenidos

def get_content_by_director(db: Session, idDirector: str):
    # Recuperar los contenidos dentro de la tabla contenidos con ese idDirector
    contenidos = db.query(models.Contenido).filter(models.Contenido.idDirector == idDirector ).all()
    return contenidos

def get_actors_by_content(db: Session, idContenido: str):
    #Obtener los idActores de Reparto en los que existe el idContenido
    idsActor_by_content = db.query(models.Reparto.idActor).filter(models.Reparto.idContenido == idContenido).all()

    #Extraer solo los idActor de los resultados obtenidos
    actors_ids = [actor.idActor for actor in idsActor_by_content]

    #Recuperar los actores correspondientes a esos idActor
    actors = db.query(models.Actor).filter(models.Actor.id.in_(actors_ids)).all()

    return actors

def get_director_by_content(db: Session, idContenido: str):
    # Recuperar el director dentro de la tabla contenidos con ese idContenido
    id_director = db.query(models.Contenido.idDirector).filter(models.Contenido.id == idContenido )
    director = db.query(models.Director).filter(models.Director.id == id_director).first()
    return director

# Función para obtener los contenidos de un género específico
def get_contenidos_por_genero(db: Session, idGenero: str):
    return db.query(models.Contenido).filter(models.Contenido.idGenero == idGenero).all()

# Función para crear un actor
def create_actor(db: Session, actor: schemas.ActorCreate):
    db_actor = models.Actor (
        nombre=actor.nombre,
        nacionalidad=actor.nacionalidad,
        fechaNacimiento=actor.fechaNacimiento
    )
    db.add(db_actor)
    db.commit()
    db.refresh(db_actor)
    
    return db_actor

# Función para crear un director
def create_director(db: Session, director: schemas.DirectorCreate):
    db_director = models.Director (
        nombre=director.nombre,
        nacionalidad=director.nacionalidad,
        fechaNacimiento=director.fechaNacimiento
    )
    db.add(db_director)
    db.commit()
    db.refresh(db_director)
    
    return db_director    

# Función para actualizar un actor
def update_actor(db: Session, idActor: str, actor: schemas.ActorUpdate):
    actor_query = db.query(models.Actor).filter(models.Actor.id == idActor).first()
    if actor_query:
        actor_query.nombre=actor.nombre
        actor_query.nacionalidad=actor.nacionalidad
        actor_query.fechaNacimiento=actor.fechaNacimiento
        db.commit()
        db.refresh(actor_query)
    return actor_query

# Función para actualizar un director
def update_director(db: Session, idDirector: str, director: schemas.DirectorUpdate):
    director_query = db.query(models.Director).filter(models.Director.id == idDirector).first()
    if director_query:
        director_query.nombre=director.nombre
        director_query.nacionalidad=director.nacionalidad
        director_query.fechaNacimiento=director.fechaNacimiento
        db.commit()
        db.refresh(director_query)
    return director_query

# Función para eliminar un actor
def delete_actor(db: Session, actor_id: str) -> bool:
    actor = db.query(models.Actor).filter(models.Actor.id == actor_id).first()
    if actor:
        db.delete(actor)
        db.commit()
        return True
    return False

# Función para eliminar un director
def delete_director(db: Session, director_id: str) -> bool:
    director = db.query(models.Director).filter(models.Director.id == director_id).first()
    if director:
        db.delete(director)
        db.commit()
        return True
    return False

# Función para dar una valoración a un contenido
def valorar_contenido(db: Session, idContenido: str, valoracion: int):
    contenido = db.query(models.Contenido).filter(models.Contenido.id == idContenido).first()
    print(contenido)
    if not contenido:
        return None   
    contenido.valoracionPromedio = (contenido.valoracionPromedio + valoracion)/2
    db.commit()
    db.refresh(contenido)
    return contenido

def obtener_contenidos_busqueda(db: Session, busqueda: str):
    # Se obtienen todos los contenidos que contienen la búsqueda en el título
    contenidos_por_titulo = db.query(models.Contenido).filter(
        models.Contenido.titulo.ilike(f"%{busqueda}%")
    ).all()

    # Se buscan los géneros cuyo nombre incluye la búsqueda
    generos_coincidentes = db.query(models.Genero).filter(
        models.Genero.nombre.ilike(f"%{busqueda}%")
    ).all()

    # Crear un mapa completo de idGenero -> nombre (todos los géneros en la base de datos)
    todos_los_generos = db.query(models.Genero).all()
    genero_map = {genero.id: genero.nombre for genero in todos_los_generos}

    # Extraer los IDs de los géneros coincidentes con la búsqueda
    genero_ids = [genero.id for genero in generos_coincidentes]

    # Buscar contenidos por género
    contenidos_por_genero = db.query(models.Contenido).filter(
        models.Contenido.idGenero.in_(genero_ids)
    ).all()

    # Se juntan resultados y eliminan los duplicados
    contenidos_totales = contenidos_por_titulo + contenidos_por_genero
    contenidos_unicos = {contenido.id: contenido for contenido in contenidos_totales}.values()

    # Formatear la respuesta incluyendo el nombre del género
    resultados = [
        {
            "id": contenido.id,
            "titulo": contenido.titulo,
            "genero": genero_map.get(contenido.idGenero, "Género desconocido")  # Siempre usa el mapa completo
        }
        for contenido in contenidos_unicos
    ]

    if not resultados:
        return None
    
    return resultados


def obtener_actores_busqueda(db: Session, busqueda: str):
    actores = db.query(models.Actor).filter(models.Actor.nombre.ilike(f"%{busqueda}%"))

    
    actores_coincidentes = [
        {
            "id": actor.id,
            "nombre": actor.nombre,
            "nacionalidad": actor.nacionalidad
        }
        for actor in actores
    ]

    if not actores_coincidentes:
        return None
    return actores_coincidentes


def get_actores(db: Session):
    return db.query(models.Actor).all()

def get_directores(db: Session):
    return db.query(models.Director).all()

def eliminar_actor(db: Session, idActor: str) -> bool:
    # Buscar al actor en la base de datos
    actor = db.query(models.Actor).filter(models.Actor.id == idActor).first()
    if not actor:
        return False

    db.delete(actor)
    db.commit()  # Confirmar los cambios en la base de datos
    return True

def eliminar_director(db: Session, idDirector: str) -> bool:
    # Buscar al director en la base de datos
    director = db.query(models.Director).filter(models.Director.id == idDirector).first()
    if not director:
        return False

    db.delete(director)
    db.commit()  # Confirmar los cambios en la base de datos
    return True

