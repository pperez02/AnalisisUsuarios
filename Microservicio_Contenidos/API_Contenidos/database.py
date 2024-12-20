from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from . import models, crud 
import os 

"""
Autor: Grupo GA01 - ASEE
Versión: 1.0
Descripción: Conexión a la base de datos contenidos.db y creación de sesión

"""

# URL de la base de datos (SQLite en este caso)
# Acceso antes de DOCKER!!! SQLALCHEMY_DATABASE_URL = "sqlite:///./Microservicio_Contenidos/contenidos.db"

#Acceso a la base de datos tras realizar los cambios con Docker
DB_PATH = os.getenv("DB_PATH", "/app/contenidos.db")  # /app es el directorio de trabajo del contenedor
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"

# Crear el motor para interactuar con la base de datos
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Crear una fábrica de sesiones para hacer queries
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para los modelos de SQLAlchemy
Base = declarative_base()

# Dependencia para obtener una sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def initialize_database():
    if not os.path.exists(DB_PATH):
        # Crea las tablas si no existen
        Base.metadata.create_all(bind=engine)
        print("Base de datos creada y tablas inicializadas.")

        # Insertar valores iniciales
        db = SessionLocal()
        try:
            subtitulosExistentes = db.query(models.Subtitulo).count()
            if subtitulosExistentes == 0:
                subtitulo_nuevo = models.Subtitulo(idSubtitulo="1", idioma="Inglés")    
                db.add(subtitulo_nuevo)  
                subtitulo_nuevo = models.Subtitulo(idSubtitulo="2", idioma="Español")    
                db.add(subtitulo_nuevo)  
                subtitulo_nuevo = models.Subtitulo(idSubtitulo="3", idioma="Italiano")    
                db.add(subtitulo_nuevo)  
                subtitulo_nuevo = models.Subtitulo(idSubtitulo="4", idioma="Portugués")    
                db.add(subtitulo_nuevo)      

            subtitulosContenidoExistentes = db.query(models.SubtituloContenido).count()
            if subtitulosContenidoExistentes == 0:
                subtitulosContenidoNuevo = models.SubtituloContenido(idSubtitulosContenido="1", idSubtitulo="1")
                db.add(subtitulosContenidoNuevo)
                subtitulosContenidoNuevo = models.SubtituloContenido(idSubtitulosContenido="1", idSubtitulo="2")
                db.add(subtitulosContenidoNuevo)
                subtitulosContenidoNuevo = models.SubtituloContenido(idSubtitulosContenido="1", idSubtitulo="3")
                db.add(subtitulosContenidoNuevo)
                subtitulosContenidoNuevo = models.SubtituloContenido(idSubtitulosContenido="1", idSubtitulo="4")
                db.add(subtitulosContenidoNuevo)
            
            doblajesExistentes = db.query(models.Subtitulo).count()
            if doblajesExistentes == 0:
                doblaje_nuevo = models.Doblaje(idDoblaje="1", idioma="Inglés")    
                db.add(doblaje_nuevo)  
                doblaje_nuevo = models.Doblaje(idDoblaje="2", idioma="Español")    
                db.add(doblaje_nuevo)  
                doblaje_nuevo = models.Doblaje(idDoblaje="3", idioma="Italiano")    
                db.add(doblaje_nuevo)  
                doblaje_nuevo = models.Doblaje(idDoblaje="4", idioma="Portugués")    
                db.add(doblaje_nuevo)

            doblajesContenidoExistentes = db.query(models.DoblajeContenido).count()
            if doblajesContenidoExistentes == 0:
                doblajesContenidoNuevo = models.DoblajeContenido(idDoblajeContenido="1", idDoblaje="1")
                db.add(doblajesContenidoNuevo)
                doblajesContenidoNuevo = models.DoblajeContenido(idDoblajeContenido="1", idDoblaje="2")
                db.add(doblajesContenidoNuevo)
                doblajesContenidoNuevo = models.DoblajeContenido(idDoblajeContenido="1", idDoblaje="3")
                db.add(doblajesContenidoNuevo)
                doblajesContenidoNuevo = models.DoblajeContenido(idDoblajeContenido="1", idDoblaje="4")
                db.add(doblajesContenidoNuevo)

            generosExistentes = db.query(models.Genero).count()
            if generosExistentes == 0:
                generoNuevo = models.Genero(id="1", nombre="Drama", descripcion="Descripcion de drama: llorar")
                db.add(generoNuevo)
            
            contenidosExistentes = db.query(models.Contenido).count()
            if contenidosExistentes == 0:
                contenidoNuevo = models.Contenido(id="ContenidoPrueba1", tipoContenido="Pelicula", titulo="ContenidoPrueba", descripcion="Descripcion de prueba",
                                                   fechaLanzamiento="0000-00-00", idGenero=1, valoracionPromedio=0, idSubtitulosContenido="1", 
                                                   idDoblajeContenido="1", duracion=120, idDirector="1")
                db.add(contenidoNuevo)
                contenidoNuevo = models.Contenido(id="1", tipoContenido="Serie", titulo="Los Soprano", descripcion="Descripcion de los soprano",
                                                   fechaLanzamiento="0000-00-00", idGenero=1, valoracionPromedio=0, idSubtitulosContenido="1", 
                                                   idDoblajeContenido="1")
                db.add(contenidoNuevo)

            temporadasExistentes = db.query(models.Temporada).count()
            if temporadasExistentes == 0:
                temporadaNueva = models.Temporada(idContenido="1", idTemporada="1", numeroTemporada="1")
                db.add(temporadaNueva)
                temporadaNueva = models.Temporada(idContenido="1", idTemporada="2", numeroTemporada="3")
                db.add(temporadaNueva)
                temporadaNueva = models.Temporada(idContenido="1", idTemporada="3", numeroTemporada="3")
                db.add(temporadaNueva)

            episodiosExistentes = db.query(models.Episodio).count()
            if episodiosExistentes == 0:
                episodioNuevo = models.Episodio(idContenido="1", idTemporada="1", idEpisodio="1", 
                                                idDirector="1", numeroEpisodio="1", duracion="15")
                db.add(episodioNuevo)
                episodioNuevo = models.Episodio(idContenido="1", idTemporada="1", idEpisodio="2",
                                                 idDirector="1", numeroEpisodio="2", duracion="16")
                db.add(episodioNuevo)
                episodioNuevo = models.Episodio(idContenido="1", idTemporada="2", idEpisodio="3",
                                                 idDirector="1", numeroEpisodio="1", duracion="17")
                db.add(episodioNuevo)
                episodioNuevo = models.Episodio(idContenido="1", idTemporada="2", idEpisodio="4",
                                                 idDirector="1", numeroEpisodio="2", duracion="11")
                db.add(episodioNuevo)
                episodioNuevo = models.Episodio(idContenido="1", idTemporada="3", idEpisodio="5",
                                                 idDirector="1", numeroEpisodio="1", duracion="20")
                db.add(episodioNuevo)
                episodioNuevo = models.Episodio(idContenido="1", idTemporada="3", idEpisodio="6",
                                                 idDirector="1", numeroEpisodio="2", duracion="21")
                db.add(episodioNuevo)
                
            actoresExistentes = db.query(models.Actor).count()
            if actoresExistentes == 0:
                #Pelicula de prueba para vincular a los nuevos Actores
                contenido_vinculado_actores = models.Contenido(id="ContenidoActores1", tipoContenido="Pelicula", titulo = "PeliculaActores", descripcion="prueba", 
                                    fechaLanzamiento="0000-00-00", idGenero="1", valoracionPromedio=0, idSubtitulosContenido="1", idDoblajeContenido="1", 
                                    duracion=120, idDirector="1")
                db.add(contenido_vinculado_actores)
                actor_nuevo = models.Actor(id="1", nombre="Robert Deniro", nacionalidad="EstadoUnidense", fechaNacimiento="1943-08-17")    
                db.add(actor_nuevo)  
                actor_nuevo = models.Actor(id="2", nombre="Tom Cruise", nacionalidad="EstadoUnidense", fechaNacimiento="1962-07-03")    
                db.add(actor_nuevo)  
                actor_nuevo = models.Actor(id="3", nombre="Tom Hardy", nacionalidad="Britanico", fechaNacimiento="1977-09-15")    
                db.add(actor_nuevo)  
                actor_nuevo = models.Actor(id="4", nombre="George Clooney", nacionalidad="EstadoUnidense", fechaNacimiento="1961-05-06")    
                db.add(actor_nuevo)

                for i in 1,2,3,4:
                    reparto_nuevo = models.Reparto(idContenido="ContenidoActores1", idActor=str(i))
                    db.add(reparto_nuevo)

            directoresExistentes = db.query(models.Director).count()
            if directoresExistentes == 0:
                directorNuevo = models.Director(id="1", nombre="Francis Ford Coppola", nacionalidad="EstadoUnidense", fechaNacimiento="1939-04-07")    
                db.add(directorNuevo)  
                directorNuevo = models.Director(id="2", nombre="Stanley Kubrik", nacionalidad="Estadounidense", fechaNacimiento="1928-07-26")    
                db.add(directorNuevo)  
                directorNuevo = models.Director(id="3", nombre="Jean Luc Godard", nacionalidad="Frances", fechaNacimiento="1930-12-03")    
                db.add(directorNuevo)  
                directorNuevo = models.Director(id="4", nombre="David Lynch", nacionalidad="EstadoUnidense", fechaNacimiento="1946-01-20")    
                db.add(directorNuevo)
                #Pelicula de prueba para vincular a los nuevos directores

                for i in 1,2,3,4:
                    idContenidoD = "ContenidoDirectores"+str(i)
                    contenido_vinculado_directores = models.Contenido(id=idContenidoD, tipoContenido="Pelicula", titulo = "PeliculaDirectores"+str(i), descripcion="prueba", 
                                    fechaLanzamiento="0000-00-00", idGenero="1", valoracionPromedio=0, idSubtitulosContenido="1", idDoblajeContenido="1", 
                                    duracion=120, idDirector=str(i))
                    db.add(contenido_vinculado_directores)

            db.commit()
            print("Valores iniciales insertados (Contenidos).")
        finally:
            db.close()