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
    
class PeliculaUpdate(ContenidoBase):
    duracion: Optional[int]
    idDirector: Optional[str]
    class Config:
        from_attributes = True   

class SerieUpdate(ContenidoBase):
    pass
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

class TemporadaBase(BaseModel):
    numeroTemporada: int

class TemporadaCreate(TemporadaBase):
    pass

class Temporada(TemporadaBase):
    idTemporada: str  # Generado automáticamente
    idContenido: str
    class Config:
        from_attributes = True


class EpisodioBase(BaseModel):
    idDirector: str
    numeroEpisodio: int
    duracion: int  # En minutos

class EpisodioCreate(EpisodioBase):
    pass

class Episodio(EpisodioBase):
    idEpisodio: str  # Generado automáticamente
    idContenido: str
    idTemporada: str
    class Config:
        from_attributes = True

class GeneroBase(BaseModel):
    nombre: str
    descripcion: str

class GeneroCreate(GeneroBase):
    pass

class GeneroUpdate(GeneroBase):
    pass

class Genero(GeneroBase):
    pass    