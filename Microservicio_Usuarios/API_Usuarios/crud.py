from sqlalchemy.orm import Session
from . import models, schemas

"""
Autor: Grupo GA01 - ASEE
Versión: 1.0
Descripción: Funciones CRUD para interactuar con la base de datos
"""

# Función para crear un nuevo usuario
def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        nombre=user.nombre,
        email=user.email,
        password=user.password,
        idioma=user.idioma,
        idPlanSuscripcion=user.idPlanSuscripcion,
        idListaPersonalizada=user.idListaPersonalizada,
        idHistorial=user.idHistorial
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Función para obtener un usuario por ID
def get_user(db: Session, user_id: str):
    return db.query(models.User).filter(models.User.id == user_id).first()

# Función para obtener un usuario por email
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

# Función para obtener todos los usuarios
def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.User).offset(skip).limit(limit).all()