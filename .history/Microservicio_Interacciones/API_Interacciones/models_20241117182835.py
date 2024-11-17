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
    id_usuario = Column(String, primary_key=True, nullable=False)  # Referencia lógica a Usuarios
    id_contenido = Column(String, primary_key=True, nullable=False)  # Referencia lógica a Contenido
    puntuacion = Column(Float, nullable=False)  # Escala de 0 a 10

class ListaMeGusta(Base):
    __tablename__ = "lista_me_gusta"
    id_usuario = Column(String, primary_key=True, nullable=False)  # Referencia lógica a Usuarios
    id_contenido = Column(String, primary_key=True, nullable=False)  # Referencia lógica a Contenido

class ListaPersonalizada(Base):
    __tablename__ = "lista_personalizada"
    id_lista = Column(String, primary_key=True, nullable=False)
    id_contenido = Column(String, primary_key=True, nullable=False)  # Referencia lógica a Contenido
