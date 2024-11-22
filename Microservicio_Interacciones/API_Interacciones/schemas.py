from pydantic import BaseModel, EmailStr
from typing import Optional
from enum import Enum

"""
Autor: Grupo GA01 - ASEE
Versión: 1.1
Descripción: Descripción de los esquemas utilizados para validar los datos
"""

class Contenido(BaseModel):
    titulo: str
    descripcion: Optional[str]
    fechaLanzamiento: str
    idGenero: str
    valoracionPromedio: Optional[float] = None
    idSubtitulosContenido: Optional[str] = None
    idDoblajeContenido: Optional[str] = None

# Esquema utilizado para las listas de "Me gusta" de los usuarios
class ListaMeGusta(BaseModel):
    idUsuario: str
    idContenido: str

# Esquema utilizado para validar las valoraciones dadas por los usuarios
class ValoracionUsuarioContenido(BaseModel):
    idUsuario: str
    idContenido: str
    puntuacion: int

class Tendencia(BaseModel):
    idContenido: str
    me_gusta_total: int

class TendenciasResponse(BaseModel):
    tendencias: list[Tendencia]

class ContenidoMeGusta(BaseModel):
    id: str
    titulo: str
    descripcion: Optional[str]
    fechaLanzamiento: str
    idGenero: str
    valoracionPromedio: Optional[float] = None
    idSubtitulosContenido: Optional[str] = None
    idDoblajeContenido: Optional[str] = None