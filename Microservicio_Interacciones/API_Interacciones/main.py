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

# Endpoint para obtener lista de me gusta
@app.get("/usuarios/{idUsuario}/me-gusta", response_model=list[schemas.ContenidoMeGusta])
def mostrar_megusta(idUsuario: str, db: Session = Depends(get_db)):
    me_gusta = crud.mostrar_me_gusta(db=db, usuario_id=idUsuario)    
    #if not me_gusta: TODO esto impide que devuelva una lista vacia
    #    raise HTTPException(status_code=404, detail="No se pudieron recuperar los me gusta")
    return me_gusta

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

# Endpoint para añadir contenido al historial
@app.post("/usuarios/{idUsuario}/historial/{idContenido}")
def actualizar_historial(idUsuario: str, idContenido: str, db: Session = Depends(get_db)):
    try:
        entrada = crud.crear_entrada_historial(db=db, usuario_id=idUsuario, contenido_id=idContenido)
        return {"message": "Contenido añadido al historial", "entrada": entrada}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint para devolver el historial del usuario
@app.get("/usuarios/{idUsuario}/historial", response_model=list[schemas.Contenido])
def get_historial(idUsuario: str, db: Session = Depends(get_db)):
    historial = crud.get_historial_usuario(db=db, usuario_id=idUsuario)
    if not historial:
         raise HTTPException(status_code=404, detail="No se ha encontrado historial")    
    return historial     

# Endpoint para obtener los contenidos más populares basados en "me gusta".
@app.get("/contenido/tendencias", response_model=schemas.TendenciasResponse)
def obtener_tendencias(limite: int = 2, db: Session = Depends(get_db)):
    contenidos = crud.get_mas_me_gusta(db, limite)
    tendencias = [
        schemas.Tendencia(idContenido=c.idContenido, me_gusta_total=c.me_gusta_total)
        for c in contenidos
    ]
    return schemas.TendenciasResponse(tendencias=tendencias)

# Endpoint para añadir contenido a la lista personalizada
@app.post("/usuarios/{idUsuario}/listaPersonalizada/{idContenido}")
def insert_content_into_LP(idUsuario: str, idContenido: str, db: Session = Depends(get_db)):
    try:
        LP = crud.insert_content_into_LP(db=db, usuario_id=idUsuario, contenido_id=idContenido)
        return {"message": "Contenido añadido a lista personalizada", "LP": LP}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# Endpoint para devolver la ListaPersonalizada de usuario
@app.get("/usuarios/{idUsuario}/listaPersonalizada", response_model=list[schemas.ContenidoGetId])
def get_LP_user(idUsuario: str, db: Session = Depends(get_db)):
    try:
        LP = crud.get_LP_user(db=db, usuario_id=idUsuario)
        return LP  # Si LP es una lista vacía, el cliente recibirá `[]`
    except HTTPException as e:
        raise e  # Devolver errores HTTP generados en CRUD
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error inesperado: {e}"
        )
    
# Endpoint para eliminar contenido de la listaPersonalizada
@app.delete("/usuarios/{idUsuario}/listaPersonalizada/{idContenido}")
def delete_conent_from_user_LP(idUsuario: str, idContenido: str, db: Session = Depends(get_db)):
    eliminado = crud.delete_conent_from_user_LP(db=db, idUsuario=idUsuario, idContenido=idContenido)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Contenido no eliminado de ListaPersonalizada")
    return {"message": "Contenido eliminado de ListaPersonalizada"}