from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import engine, get_db, initialize_database

"""
Autor: Grupo GA01 - ASEE
Versión: 1.0
Descripción: Microservicio de Usuarios con los endpoints

Comando de ejecución: 

"""

#Crear la aplicacion
app = FastAPI(
    title="Microservicio de Usuarios",
    description="API para gestionar los usuarios, métodos de pago, suscripciones y listas personalizadas.",
    version="1.0.0",
)

# Crear la base de datos
initialize_database()

# Dependency para obtener la sesión de base de datos
def get_database():
    db = next(get_db())
    return db

@app.get("/usuarios", response_model=list[schemas.User])
def get_usuarios(skip: int = 0, limit: int = 10, db: Session = Depends(get_database)):
    return crud.get_users(db, skip=skip, limit=limit)

@app.post("/usuarios/registro", response_model=schemas.User)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_database)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email ya registrado")
    return crud.create_user(db, user)

@app.post("/usuarios/login", response_model=schemas.User)
def login_user(credentials: schemas.UserLogin, db: Session = Depends(get_database)):
    db_user = crud.get_user_by_email(db, email=credentials.email)
    if not db_user or db_user.password != credentials.password:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    return db_user    