import uuid
from sqlalchemy import Column, String, ForeignKey, Float, Integer, PrimaryKeyConstraint
from .database import Base

"""
Autor: Grupo GA01 - ASEE
Versión: 1.1
Descripción: Descripción de los modelos de datos utilizados en la base de datos
"""

class ValoracionUsuarioContenido(Base):
    __tablename__ = "valoracion_usuario_contenido"
    idUsuario = Column(String, nullable=False)  # Referencia lógica a Usuarios
    idContenido = Column(String, nullable=False)  # Referencia lógica a Contenido
    puntuacion = Column(Float, nullable=False)  # Escala de 0 a 10

    __table_args__ = (
        PrimaryKeyConstraint('idUsuario', 'idContenido'),
    )    

class ListaMeGusta(Base):
    __tablename__ = "lista_me_gusta"
    idUsuario = Column(String, nullable=False)  # Referencia lógica a Usuarios
    idContenido = Column(String, nullable=False)  # Referencia lógica a Contenido
        
    __table_args__ = (
        PrimaryKeyConstraint('idUsuario', 'idContenido'),
    )

class ListaPersonalizada(Base):
    __tablename__ = "lista_personalizada"
    idLista = Column(String, nullable=False)
    idContenido = Column(String, nullable=False)  # Referencia lógica a Contenido

    __table_args__ = (
        PrimaryKeyConstraint('idLista', 'idContenido'),
    )

class HistorialUsuario(Base):
    __tablename__ = "historial_usuario"
    idHistorial = Column(String, nullable=False)
    idContenido = Column(String, nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint('idHistorial', 'idContenido')
    )       
