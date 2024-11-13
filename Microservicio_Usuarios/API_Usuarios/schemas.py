from pydantic import BaseModel, EmailStr
from typing import Optional
from enum import Enum

"""
Autor: Grupo GA01 - ASEE
Versión: 1.1
Descripción: Descripción de los esquemas utilizados para validar los datos
"""

# Esquema base para el usuario, que no incluye el ID
class UserBase(BaseModel):
    nombre: str
    email: EmailStr  # Usar EmailStr para validar que el formato del email es correcto
    password: str
    idioma: Optional[str] = None  # Nuevo atributo para el idioma
    idPlanSuscripcion: Optional[str] 
    idListaPersonalizada: Optional[str] = None
    idHistorial: Optional[str] = None

# Esquema de creación de usuario
class UserCreate(UserBase):
    pass  # Se hereda todo de UserBase, no se necesita modificar nada aquí

# Esquema para representar a un usuario
class User(UserBase):
    id: str  # El ID se generará automáticamente

    class Config:
        from_attributes = True  # Permite a Pydantic trabajar con los modelos de SQLAlchemy

# Esquema para el inicio de sesión de usuario
class UserLogin(BaseModel):
    email: EmailStr
    password: str
    class Config:
        from_attributes = True  # Esto permite a Pydantic trabajar con los modelos de SQLAlchemy, si es necesario        

# Esquema para la actualización de usuario
class UserUpdate(BaseModel):
    nombre: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    idioma:Optional[str]
    idPlanSuscripcion: Optional[str] = None
    idListaPersonalizada: Optional[str] = None
    idHistorial: Optional[str] = None
    class Config:
        from_attributes = True  # Permite a Pydantic trabajar con los modelos de SQLAlchemy, si es necesario

# Esquema para el idioma del usuario
class UserLanguage(BaseModel):
    idioma: str  # Idioma preferido del usuario
    class Config:
        from_attributes = True  # Permite a Pydantic trabajar con los modelos de SQLAlchemy, si es necesario

#Esquemas necesarias para cambiar o cancelar una suscripción a la plataforma
class AccionSuscripcion(str, Enum):
    cambiar = "cambiar"
    cancelar = "cancelar"

class SubscriptionUpdate(BaseModel):
    accion: AccionSuscripcion  # Usa el Enum aquí
    idPlanSuscripcion: Optional[str]