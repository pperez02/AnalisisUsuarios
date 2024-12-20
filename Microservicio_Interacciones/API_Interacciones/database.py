from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from . import models, crud 
import os 

"""
Autor: Grupo GA01 - ASEE
Versión: 1.0
Descripción: Conexión a la base de datos usuarios.db y creación de sesión

"""

# URL de la base de datos (SQLite en este caso)
#Acceso antes de los cambios de Docker!!! SQLALCHEMY_DATABASE_URL = "sqlite:///./Microservicio_Interacciones/interacciones.db"

#Acceso a la base de datos tras realizar los cambios con Docker
DB_PATH = os.getenv("DB_PATH", "/app/interacciones.db")  # /app es el directorio de trabajo del contenedor
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

# Función para inicializar la base de datos
def initialize_database():
    if not os.path.exists(DB_PATH):
        # Crea las tablas si no existen
        Base.metadata.create_all(bind=engine)
        print("Base de datos creada y tablas inicializadas.")
