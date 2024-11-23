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

@app.get("/usuarios/{idUsuario}", response_model=schemas.User)
def get_usuarios(idUsuario: str, db: Session = Depends(get_database)):
    usuario = crud.get_user(db, user_id=idUsuario)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

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

@app.put("/usuarios/{idUsuario}/perfil")
def update_user_profile(idUsuario: str, user_data: schemas.UserUpdate, db: Session = Depends(get_database)):
    print(user_data)
    user = crud.update_user(db, user_id=idUsuario, user_data=user_data)
    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"message": "Perfil actualizado exitosamente"}

@app.put("/usuarios/{idUsuario}/idioma")
def update_user_language(idUsuario: str, idioma: schemas.UserLanguage, db: Session = Depends(get_database)):
    # Aquí puedes implementar la lógica para actualizar el idioma del usuario
    user = crud.get_user(db, user_id=idUsuario)
    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    # Supongamos que agregamos un campo 'idioma' en el modelo User
    user.idioma = idioma.idioma  # Este campo debe estar definido en tu modelo
    db.commit()
    return {"message": "Idioma actualizado exitosamente"}

@app.put("/usuarios/{idUsuario}/suscripcion")
def update_subscription(idUsuario: str, subscription: schemas.SubscriptionUpdate, db: Session = Depends(get_database)):
    user = crud.get_user(db, user_id=idUsuario)
    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    if subscription.accion == "cambiar":
        
        nuevoPlan = crud.get_plan_suscripcion(db, subscription.idPlanSuscripcion)
        if nuevoPlan is None:
            raise HTTPException(status_code=404, detail="Plan de suscripción no encontrado")
        user.idPlanSuscripcion = subscription.idPlanSuscripcion  
        db.commit()
        return {"message": "Suscripción cambiada exitosamente", "nuevoPlan": subscription.idPlanSuscripcion}

    elif subscription.accion == "cancelar":
        
        user.idPlanSuscripcion = None  # O la lógica que decida cómo manejar la cancelación
        db.commit()
        return {"message": "Suscripción cancelada exitosamente"}

    raise HTTPException(status_code=400, detail="Acción no válida")

@app.get("/metodos-pago", response_model=list[schemas.MetodoPago])
def get_payment_methods(db: Session = Depends(get_database)):
    return crud.get_metodos_pago(db)

@app.get("/usuarios/{idUsuario}/metodos-pago", response_model=list[schemas.MetodoPago])
def get_user_payment_methods(idUsuario: str, db: Session = Depends(get_database)):
    user = crud.get_user(db, user_id=idUsuario)
    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    metodosPagoUsuario = crud.get_metodos_pago_usuario(db, user_id=idUsuario)
    return metodosPagoUsuario

@app.post("/usuarios/{idUsuario}/metodos-pago", response_model=schemas.MetodoPagoUsuarioCreate)
def add_payment_method(idUsuario: str, metodo_pago: schemas.MetodoPagoCreate, db: Session = Depends(get_database)):
    user = crud.get_user(db, user_id=idUsuario)
    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    metodoPagoCreado = crud.create_metodo_pago(db, metodo_pago)
    idMetodoPago = metodoPagoCreado.id
    return crud.create_metodo_pago_usuario(db, idUsuario=user.id, idMetodoPago=idMetodoPago)

# Endpoint para obtener un listado con todos los planes de suscripcición existentes en la BD
@app.get("/planes-suscripcion", response_model=list[schemas.PlanSuscripcion])
def get_planes_suscripcion(db: Session = Depends(get_database)):
    planes = crud.get_planes_suscripcion(db=db)
    if not planes:
        raise HTTPException(status_code=404, detail="No se han encontrado Planes de Suscripcion")
    return planes