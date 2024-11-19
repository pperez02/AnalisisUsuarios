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
    descripcion: str
    fechaLanzamiento: str
    idGenero: str
    valoracionPromedio: Optional[float] = None
    idSubtitulosContenido: Optional[str] = None
    idDoblajeContenido: Optional[str] = None