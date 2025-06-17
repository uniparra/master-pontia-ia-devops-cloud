import logging
import os

from fastapi import FastAPI, HTTPException, Body
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from practicafinal.models import results, circuit, races
from practicafinal.models import Base


# --- Configuración de logging ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# --- Configuración de la base de datos de Fórmula 1 ---
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://test:test@localhost:5432/formula1")

# Creación del motor y la sesión de la base de datos
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# Creación de las tablas en la base de datos si no existen
Base.metadata.create_all(bind=engine)

# --- Configuración de la aplicación FastAPI ---
app = FastAPI(
    title="API para la práctica de clase sobre Formula 1",
    description="API de ejemplo",
    version="1.0.0"
)

# Endpoint para consultar el inventario de tablas y columnas en la base de datos
@app.get("/inventario/")
def inventariotablas():
    """
    Devuelve un diccionario con los nombres de las tablas y sus columnas.
    """
    logger.info("Acceso al endpoint de inventario de tablas")
    tabla_columnas = {
        table_name: [column.name for column in table.columns]
        for table_name, table in Base.metadata.tables.items()
    }
    return {
        "msg": "Bienvenido a la API de Formula 1",
        "tablas": tabla_columnas
    }

# Endpoint para obtener los identificadores y nombres de los circuitos
@app.get("/circuit_ids")
def circuits_id():
    """
    Devuelve una lista de diccionarios con el id y nombre de cada circuito.
    """
    db = SessionLocal()
    circuit_ids = db.query(circuit.CircuitsTB.circuitId, circuit.CircuitsTB.name).all()
    db.close()
    circuit_ids = [
        {"id_circuito": circuit_id[0],
         "nombre_circuito": circuit_id[1]
        } for circuit_id in circuit_ids]
    if not circuit_ids:
        raise HTTPException(status_code=404, detail="No circuit IDs found")
    return {
        "msg": "Circuit IDs",
        "circuit_ids": circuit_ids
    }

# Endpoint para consultar los últimos n ganadores en un circuito específico
@app.get("/last_n_winners_in_circuit/{circuit_id}/{n}")
def last_n_winners_circuit(circuit_id: int, n: int):
    """
    Devuelve los últimos n ganadores en un circuito dado.
    """
    db = SessionLocal()
    winners = (
        db.query(results.ResultsTB)
        .join(results.ResultsTB.race)
        .join(results.ResultsTB.driver)
        .filter(races.RacesTB.circuitId == circuit_id).filter(results.ResultsTB.position == "1")
        .order_by(races.RacesTB.date.desc())
        .limit(n)
        .all()
    )
    winners_json = [{
        "name": w.driver.forename,
        "surname": w.driver.surname,
        "race": w.race.name,
        "circuit": w.race.circuit.name,
        "time": w.time,
        "date": w.race.date,
    } for w in winners]
    db.close()
    if not winners_json:
        raise HTTPException(status_code=404, detail="No winners found for this circuit")
    return {
        "msg": f"Last {n} winners at circuit {circuit_id}",
        "winners": winners_json
    }



# Endpoint para crear un nuevo resultado de carrera
@app.post("/results/", response_model=results.Result)
def create_result(result: results.Result = Body(...)):
    """
    Crea un nuevo resultado de carrera en la base de datos.
    """
    db = SessionLocal()
    new_result = results.ResultsTB(
        raceId=result.raceId,
        driverId=result.driverId,
        constructorId=result.constructorId,
        number=result.number,
        grid=result.grid,
        position=result.position,
        positionText=result.positionText,
        positionOrder=result.positionOrder,
        points=result.points,
        laps=result.laps,
        time=result.time,
        milliseconds=result.milliseconds,
        fastestLap=result.fastestLap,
        rank=result.rank,
        fastestLapTime=result.fastestLapTime,
        fastestLapSpeed=result.fastestLapSpeed,
        statusId=result.statusId
    )
    try:
        db.add(new_result)
        db.commit()
        db.refresh(new_result)
    except Exception as e:
        db.rollback()
        logger.error(f"Error al insertar: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()
    return new_result

# Endpoint para eliminar un resultado de carrera por su ID
@app.delete("/results/{result_id}")
def delete_result(result_id: int):
    """
    Elimina un resultado de carrera de la base de datos por su identificador.
    """
    logger.info(f"Intentando eliminar resultado con ID: {result_id}")
    db = SessionLocal()
    db_result = db.query(results.ResultsTB).filter_by(resultId=result_id).first()
    if not db_result:
        db.close()
        raise HTTPException(status_code=404, detail="Resultado no encontrado")
    db.delete(db_result)
    db.commit()
    db.close()
    return {"msg": f"Resultado con ID {result_id} eliminado correctamente"}