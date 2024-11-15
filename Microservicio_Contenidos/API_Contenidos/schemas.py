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

class ContenidoUpdate(BaseModel):
    titulo: Optional[str] = None
    descripcion: Optional[str] = None
    fechaLanzamiento: Optional[str] = None
    idGenero: Optional[str] = None
    valoracionPromedio: Optional[float] = None
    idSubtitulosContenido: Optional[str] = None
    idDoblajeContenido: Optional[str] = None

class Contenido(ContenidoBase):
    id: str #Generado Automaticamente
    class Config:
        from_attributes = True
    
class PeliculaUpdate(ContenidoUpdate):
    duracion: Optional[int] = None
    idDirector: Optional[str] = None
    class Config:
        from_attributes = True   

class SerieUpdate(ContenidoUpdate):
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
    id: str # Generado automáticamente

    class Config:
        from_attributes = True

class TemporadasGet(BaseModel):
    idTemporada: str
    Episodios: list[Episodio]
class SeriesGet(BaseModel):
    idSerie: str
    Temporadas: list[TemporadasGet]

class TemporadaUpdate(BaseModel):
    numeroTemporada: Optional[int]

class EpisodioUpdate(BaseModel):
    numeroEpisodio: Optional[int] = None
    duracion: Optional[int] = None
    idDirector: Optional[str] = None

class RepartoUpdate(BaseModel):
    idActor: str

