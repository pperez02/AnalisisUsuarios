from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import engine, get_db, initialize_database

"""
Autor: Grupo GA01 - ASEE
Versión: 1.0
Descripción: Microservicio de Usuarios con los endpoints

Comando de ejecución: 

"""

#Crear la aplicacion
app = FastAPI(
    title="Microservicio de Interacciones",
    description="API para gestionar las recomendaciones e interacciones de usuarios y contenido multimedia.",
    version="1.0.0",
)

# Crear la base de datos
initialize_database()

# Dependency para obtener la sesión de base de datos
def get_database():
    db = next(get_db())
    return db

@app.get("/usuarios/{idUsuario}/recomendaciones", response_model=list[schemas.Contenido])
def get_recomendaciones(idUsuario: str, db: Session = Depends(get_db)):
    recomendaciones = crud.get_recomendaciones_usuario(db=db, usuario_id=idUsuario)
    if not recomendaciones:
        raise HTTPException(status_code=404, detail="No se pudieron recuperar las recomendaciones")
    return recomendaciones  

# Endpoint para dar "Me gusta" a un contenido
@app.post("/usuarios/{idUsuario}/me-gusta/{idContenido}", response_model=schemas.ListaMeGusta)
def action_megusta(idUsuario: str, idContenido: str, db: Session = Depends(get_db)):
    return crud.dar_me_gusta(db=db, idUsuario=idUsuario, idContenido=idContenido)

# Endpoint para eliminar un "Me gusta" a un contenido
@app.delete("/usuarios/{idUsuario}/me-gusta/{idContenido}")
def action_eliminar_me_gusta(idUsuario: str, idContenido: str, db: Session = Depends(get_db)):
    eliminado = crud.quitar_me_gusta(db=db, idUsuario=idUsuario, idContenido=idContenido)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Contenido no encontrado en la lista de me gusta")
    return {"message": "Contenido eliminado de la lista de Me gusta"}  

# Endpoint para añadir una puntuación a un contenido
@app.post("/usuarios/{idUsuario}/valoraciones/{idContenido}", response_model=schemas.ValoracionUsuarioContenido)
def action_valorar_contenido(valoracion: int, idUsuario: str, idContenido: str, db: Session = Depends(get_db)):
    valoracionUsuarioContenido = crud.valorar_contenido(db=db, idUsuario=idUsuario, idContenido=idContenido, valoracion=valoracion)
    if not valoracionUsuarioContenido:
        raise HTTPException(status_code=500, detail="Error al añadir la valoración")
    return valoracionUsuarioContenido

# Endpoint para obtener los contenidos más populares basados en "me gusta".
@app.get("/contenido/tendencias", response_model=schemas.TendenciasResponse)
def obtener_tendencias(limite: int = 2, db: Session = Depends(get_db)):
    contenidos = crud.get_mas_me_gusta(db, limite)
    tendencias = [
        schemas.Tendencia(idContenido=c.idContenido, me_gusta_total=c.me_gusta_total)
        for c in contenidos
    ]
    return schemas.TendenciasResponse(tendencias=tendencias)