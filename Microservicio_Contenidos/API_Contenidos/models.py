import uuid
from sqlalchemy import Column, String, ForeignKey, Float, Integer, PrimaryKeyConstraint
from .database import Base

"""
Autor: Grupo GA01 - ASEE
Versión: 1.1
Descripción: Descripción de los modelos de datos utilizados en 
la base de datos
"""

# Microservicio Contenidos

#TODO Comprobar si en la DB la herencia funciona como en el código. //TODO de momento está quitada 
class Contenido(Base):
    __tablename__ = "Contenido"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)  # ID generado automáticamente
    tipoContenido = Column(String)  #'Pelicula' o 'Serie'

    titulo = Column(String)
    descripcion = Column(String)
    fechaLanzamiento = Column(String)  # Formato: YYYY-MM-DD
    idGenero = Column(String, ForeignKey("Genero.id"))
    valoracionPromedio = Column(Float)  # Escala de 0 a 10
    idSubtitulosContenido = Column(String, ForeignKey("SubtituloContenido.idSubtitulosContenido"))
    idDoblajeContenido = Column(String, ForeignKey("DoblajeContenido.idDoblajeContenido"))

    #Parametros exclusivos de Pelicula
    duracion = Column(Integer, nullable=True)  # En minutos
    idDirector = Column(String, ForeignKey("Director.id"), nullable=True) 

class Temporada(Base):
    __tablename__ = "Temporada"

    idContenido = Column(String, ForeignKey("Contenido.id"))
    idTemporada = Column(String, default=lambda: str(uuid.uuid4()), index=True)
    numeroTemporada = Column(Integer)

    #TODO comprobar si con las primarykeys anda, o si hay que especificar el 'PrimaryKeyConstraint'
    __table_args__ = (
        PrimaryKeyConstraint('idContenido', 'idTemporada'),
    )

class Episodio(Base):
    __tablename__ = "Episodio"

    idContenido = Column(String, ForeignKey("Contenido.id"))
    idTemporada = Column(String, ForeignKey("Temporada.idTemporada"))
    idEpisodio = Column(String, default=lambda: str(uuid.uuid4()), index=True)
    idDirector = Column(String, ForeignKey("Director.id"))
    numeroEpisodio = Column(Integer)
    duracion = Column(Integer)  # En minutos

    #TODO comprobar si con las primarykeys anda, o si hay que especificar el 'PrimaryKeyConstraint'
    __table_args__ = (
        PrimaryKeyConstraint('idContenido', 'idTemporada', 'idEpisodio'),
    )

class Trailer(Base):
    __tablename__ = "Trailer"

    idContenido = Column(String, ForeignKey("Contenido.id"))
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    titulo = Column(String)
    duracion = Column(Integer)  # En minutos
    idDoblajeContenido = Column(String, ForeignKey("DoblajeContenido.idDoblajeContenido"))
    fecha_trailer = Column(String)  # Formato: YYYY-MM-DD

class Genero(Base):
    __tablename__ = "Genero"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    nombre = Column(String)
    descripcion = Column(String)

class Reparto(Base):
    __tablename__ = "Reparto"

    idContenido = Column(String, ForeignKey("Contenido.id"), index=True)
    idActor = Column(String, ForeignKey("Actor.id"), index=True)

    __table_args__ = (
        PrimaryKeyConstraint('idContenido', 'idActor'),
    )



class Actor(Base):
    __tablename__ = "Actor"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    nombre = Column(String)
    nacionalidad = Column(String)
    fechaNacimiento = Column(String)  # Formato: YYYY-MM-DD

class Director(Base):
    __tablename__ = "Director"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    nombre = Column(String)
    nacionalidad = Column(String)
    fechaNacimiento = Column(String)  # Formato: YYYY-MM-DD

class SubtituloContenido(Base):
    __tablename__ = "SubtituloContenido"

    idSubtitulosContenido= Column(String, index=True)
    idSubtitulo = Column(String, ForeignKey("Subtitulo.idSubtitulo"))

    __table_args__ = (
        PrimaryKeyConstraint('idSubtitulosContenido', 'idSubtitulo'),
    )

class Subtitulo(Base):
    __tablename__ = "Subtitulo"

    idSubtitulo = Column(String, primary_key=True) #TODO
    idioma = Column(String)

class DoblajeContenido(Base):
    __tablename__ = "DoblajeContenido"

    idDoblajeContenido = Column(String,  index=True)
    idDoblaje = Column(String, ForeignKey("Doblaje.idDoblaje"))

    __table_args__ = (
        PrimaryKeyConstraint('idDoblajeContenido', 'idDoblaje'),
    )

class Doblaje(Base):
    __tablename__ = "Doblaje"

    idDoblaje = Column(String, primary_key=True)
    idioma = Column(String)