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
        idPlanSuscripcion=user.idPlanSuscripcion
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

# Función para actualizar un usuario
def update_user(db: Session, user_id: str, user_data: schemas.UserUpdate):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user:
        #Se convierten los datos en un diccionario, excluyendo los campos no enviados
        update_data = {k: v for k, v in user_data.model_dump(exclude_unset=True).items() if v is not None}
        for key, value in update_data.items():
            setattr(user, key, value)
        
        db.commit()
        db.refresh(user)
    return user

# Función para obtener un plan de suscripción por ID
def get_plan_suscripcion(db: Session, plan_id: str):
    return db.query(models.PlanSuscripcion).filter(models.PlanSuscripcion.id == plan_id).first()

def get_planes_suscripcion(db: Session):
    return db.query(models.PlanSuscripcion).all()

# Crear un nuevo método de pago
def create_metodo_pago(db: Session, metodo_pago: schemas.MetodoPagoCreate):
    db_metodo_pago = models.MetodoPago(
        tipo=metodo_pago.tipo,
        numeroTarjeta=metodo_pago.numeroTarjeta,
        emailPaypal=metodo_pago.emailPaypal
    )
    db.add(db_metodo_pago)
    db.commit()
    db.refresh(db_metodo_pago)
    return db_metodo_pago

# Obtener un método de pago por ID
def get_metodo_pago(db: Session, metodo_pago_id: str):
    return db.query(models.MetodoPago).filter(models.MetodoPago.id == metodo_pago_id).first()

# Obtener todos los métodos de pago
def get_metodos_pago(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.MetodoPago).offset(skip).limit(limit).all()

def get_metodos_pago_usuario(db: Session, user_id: str):

    metodospagousuario = db.query(models.MetodoPagoUsuario).filter(models.MetodoPagoUsuario.idUsuario == user_id).all()

    if not metodospagousuario:
        return None
    
    metodos_pago = db.query(models.MetodoPago).filter(models.MetodoPago.id.in_([mpu.idMetodoPago for mpu in metodospagousuario])).all()
    return metodos_pago

def create_metodo_pago_usuario(db: Session, idUsuario: str, idMetodoPago: str):
    metodoPagoUsuario = models.MetodoPagoUsuario(idUsuario=idUsuario, idMetodoPago=idMetodoPago)
    db.add(metodoPagoUsuario)
    db.commit()
    db.refresh(metodoPagoUsuario)
    return metodoPagoUsuario