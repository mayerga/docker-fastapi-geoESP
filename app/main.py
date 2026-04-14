import logging
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from . import models, schemas, database
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

models.Base.metadata.create_all(bind=database.engine)
app = FastAPI(title="Lugares API")

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    logger.error(f"Error de validación: {exc}")
    return JSONResponse(
        status_code=400,
        content={"detail": "HTTP 400 Bad Request: Datos de entrada incorrectos"}
    )

@app.post("/lugares", response_model=schemas.Lugar, status_code=status.HTTP_201_CREATED)
def crear_lugar(lugar: schemas.LugarCreate, db: Session = Depends(database.get_db)):
    logger.info(f"Intentando crear lugar: {lugar.nombre}")

    nuevo_lugar = models.Lugar(nombre=lugar.nombre, comunidad=lugar.comunidad, altitud=lugar.altitud)
    db.add(nuevo_lugar)
    db.commit()
    db.refresh(nuevo_lugar)
    logger.info(f"Lugar creado con éxito. ID: {nuevo_lugar.id}")
    return nuevo_lugar

@app.get("/lugares", response_model=List[schemas.Lugar])
def leer_lugares(db: Session = Depends(database.get_db)):
    logger.info("Consultando lista de todos los lugares")
    return db.query(models.Lugar).all()

@app.get("/lugares/{lugar_id}", response_model=schemas.Lugar)
def leer_lugar(lugar_id: int, db: Session = Depends(database.get_db)):
    logger.info(f"Buscando lugar con ID: {lugar_id}")
    db_lugar = db.query(models.Lugar).filter(models.Lugar.id == lugar_id).first()
    if db_lugar is None:
        logger.warning(f"Error 404: Lugar {lugar_id} no encontrado")
        raise HTTPException(status_code=404, detail="Entidad no encontrada")
    return db_lugar

@app.delete("/lugares/{lugar_id}", status_code=status.HTTP_204_NO_CONTENT)
def borrar_lugar(lugar_id: int, db: Session = Depends(database.get_db)):
    logger.info(f"Intentando borrar lugar con ID: {lugar_id}")
    db_lugar = db.query(models.Lugar).filter(models.Lugar.id == lugar_id).first()
    if db_lugar is None:
        logger.warning(f"Error 404 en borrado: ID {lugar_id} inexistente")
        raise HTTPException(status_code=404, detail="Entidad no encontrada") # 
    
    db.delete(db_lugar)
    db.commit()
    logger.info(f"Lugar {lugar_id} eliminado correctamente")
    return None