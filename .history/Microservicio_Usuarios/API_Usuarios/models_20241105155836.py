import uuid
from sqlalchemy import Column, String, ForeignKey, Float, Integer, PrimaryKeyConstraint
from .database import Base

"""
Autor: Grupo GA01 - ASEE
Versión: 1.1
Descripción: Descripción de los modelos de datos utilizados en 
la base de datos
"""

# Microservicio Usuarios

class User(Base):
    __tablename__ = "Usuario"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)  # ID generado automáticamente
    nombre = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    idioma = Column(String, nullable=True)  # Nuevo atributo para el idioma
    # Claves externas
    idPlanSuscripcion = Column(String, ForeignKey("PlanSuscripcion.id"), nullable=True,index=True)  # Ahora no es unique, ya que puede haber varios usuarios con el mismo plan
    idListaPersonalizada = Column(String, unique=True, index=True, nullable=True)
    idHistorial = Column(String, unique=True, index=True, nullable=True)


    def __repr__(self):
        return f"<User(id={self.id}, nombre={self.nombre}, email={self.email}, idioma={self.idioma})>"

class MetodoPagoUsuario(Base):
    __tablename__ = "MetodoPagoUsuario"

    idUsuario = Column(String, ForeignKey("Usuario.id"), index=True)  # Referencia correcta al nombre de la tabla
    idMetodoPago = Column(String, ForeignKey("MetodoPago.id"), index=True)

    __table_args__ = (
        PrimaryKeyConstraint('idUsuario', 'idMetodoPago'),
    )

class MetodoPago(Base):
    __tablename__ = "MetodoPago"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)  # ID generado automáticamente
    tipo = Column(String)
    numeroTarjeta = Column(String, nullable=True) 
    emailPaypal = Column(String, nullable=True, index=True)  # Puede ser opcional si no siempre hay Paypal

class PlanSuscripcion(Base):
    __tablename__ = "PlanSuscripcion"

    id = Column(String, primary_key=True, index=True)  # ID generado automáticamente
    nombre = Column(String)
    precioMensual = Column(Float)
    numeroDispositivos = Column(Integer)
