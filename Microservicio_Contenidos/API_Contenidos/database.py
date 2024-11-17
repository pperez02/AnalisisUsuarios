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
SQLALCHEMY_DATABASE_URL = "sqlite:///./Microservicio_Contenidos/contenidos.db"

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
    if not os.path.exists("./Microservicio_Contenidos/contenidos.db"):
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
            
            contenidosExistentes = db.query(models.Contenido).count()
            if contenidosExistentes == 0:
                contenidoNuevo = models.Contenido(id="ContenidoPrueba1", tipoContenido="Pelicula", titulo="ContenidoPrueba",
                                                   fechaLanzamiento="0000-00-00", idGenero=1, valoracionPromedio=0, idSubtitulosContenido="0", 
                                                   idDoblajeContenido="0", duracion=120, idDirector="1")
                db.add(contenidoNuevo)

            db.commit()
            print("Valores iniciales insertados (Idiomas).")
        finally:
            db.close()