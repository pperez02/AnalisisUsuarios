from pydantic import BaseModel
from typing import Optional

class ContenidoBase(BaseModel):
    titulo: str
    descripcion: str
    fechaLanzamiento: str
    idGenero: str
    valoracionPromedio: Optional[float] = None
    idSubtitulosContenido: Optional[str] = None
    idDoblajeContenido: Optional[str] = None

class ContenidoCreate(ContenidoBase):
    tipoContenido: str

class Contenido(ContenidoBase):
    id: str #Generado Automaticamente
    class Config:
        from_attributes = True
    
class ContenidoUpdate(ContenidoBase):
    duracion: Optional[int]
    idDirector: Optional[str]
    class Config:
        from_attributes = True   

class PeliculaCreate(ContenidoBase):
    duracion: int
    idDirector: str
    class Config:
        from_attributes = True

class Pelicula(ContenidoBase):
    id: str

    class Config:
        from_attributes = True

class SerieCreate(ContenidoBase):
    pass
     