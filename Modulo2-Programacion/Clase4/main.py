import logging
from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator, model_validator

from sqlalchemy import Column, Integer, String, create_engine, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from fastapi import BackgroundTasks

# --- Logging ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# --- DB setup ---
DATABASE_URL = "sqlite:///./formulauno.db"

"""
* create_engine crea una instancia de conexión con la base de datos.
* connect_args={"check_same_thread"} es un parámetro específico de SQLite, 
  que permite que la conexión se comparta entre distintos hilos (FastAPI usa hilos 
  para atender peticiones y SQLite no lo permite por defecto).
"""
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

"""
* sessionmaker es una fábrica de sesiones: cada vez que haces SessionLocal(), 
  obtienes una nueva conexión/instancia de trabajo con la base de datos.
"""
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

"""
* Esto crea una clase base de la que heredan tus modelos.
* SQLAlchemy la necesita para saber qué clases representan tablas.
"""
Base = declarative_base()

class PilotosDB(Base):
    __tablename__ = "formulauno"

    pilotos = Column(String, primary_key=True, index=True)
    victorias = Column(Integer, unique=False, index=True)
    anosactivo = Column(String, nullable=True)

"""
* Base.metadata contiene información sobre todos los modelos que se han declarado (es decir, las clases que heredan de Base).
* .create_all() genera y ejecuta las instrucciones CREATE TABLE necesarias en la base de datos, siempre que no existan.
* bind=engine indica a qué base de datos debe conectarse para crear las tablas.
"""
Base.metadata.create_all(bind=engine)

# --- Pydantic model ---
class Pilotos(BaseModel):
    pilotos: str = Field(..., min_length=3, description="Nombre de piloto (mínimo 3 caracteres)")
    victorias: int = Field(..., description="Victorias del piloto")
    anosactivo: str = Field(None, description="Años activos del piloto")

    @field_validator("pilotos")
    def username_with_values(cls, value):
        if not any(vowel in value for vowel in ["a", "e", "i", "o", "u"]):
            raise ValueError("You need vowels in your username!")
        return value

    @model_validator(mode="after")
    def long_username_if_age_ge_50(cls, instance):
        if instance.victorias is not None and instance.victorias >= 5:
            if len(instance.pilotos) > 20:
                raise ValueError("You must provide a driver name with 12 chars or less")
        return instance

# --- FastAPI setup ---
app = FastAPI(
    title="Mi primera API con FastAPI",
    description="Una API de ejemplo con base de datos SQLite.",
    version="1.0.0"
)

@app.get("/hello")
def initial_greeting():
    logger.info("Recibida petición al saludo genérico")
    return {"msg": "Hola mundo!!!"}

#
# @app.get("/drivers")
# async def get_drivers():
#     logger.info("Acceso al endpoint de los Conductores")
#     return {"drivers": db.query("SELECT * FROM formulauno")}

@app.get("/hello/{name}")
def custom_greeting(name: str):
    logger.info(f"Recibida petición al saludo personalizado para {name}")
    processed_name = name.capitalize()
    if processed_name == "Pepe":
        logger.warning("Pepe ha entrado a la web!!")
    return {"msg": f"Hello, {processed_name}!!!"}

# def enviar_email_bienvenida(email: str):
#     logger.info(f"📧 Simulando envío de email a {email}...")
#     import time
#     time.sleep(10)  # Simular retardo para ver la asincronía
#     logger.info(f"✅ Email de bienvenida enviado a {email}")
@app.get("/pilotos/maxGanador")
def get_max_ganador():
    logger.info(f"Recibida petición para obtener el piloto con más victorias")
    db = SessionLocal()
    max_victorias = db.query(func.max(PilotosDB.victorias)).scalar()
    piloto = db.query(PilotosDB).filter(PilotosDB.victorias == max_victorias).all()
    piloto = db.query(PilotosDB).order_by(PilotosDB.victorias.desc()).all()  #<-- otra solución a esto? query(func.max(PilotosDB.victorias)).first()
    db.close()
    logger.info(f"se obtuvo con exito el piloto con más victorias")
    if not piloto:
        raise HTTPException(status_code=404, detail="Piloto no encontrado")

    return {
        "msg": "Piloto encontrado",
        "piloto": piloto.json()
    }


@app.get("/pilotos/{nombre_piloto}")
def get_user(nombre_piloto: str):
    logger.info(f"Recibida petición para obtener piloto con ID: {nombre_piloto}")
    nombreConEspacio = nombre_piloto.replace("_", " ")
    db = SessionLocal()
    piloto = db.query(PilotosDB).filter(PilotosDB.pilotos == nombreConEspacio).first()
    db.close()

    if not piloto:
        raise HTTPException(status_code=404, detail="Piloto no encontrado")

    return {
        "msg": "Piloto encontrado",
        "piloto": {
            "piloto": piloto.pilotos,
            "victorias": piloto.victorias,
            "anosactivo": piloto.anosactivo
        }
    }

@app.post("/pilotos/")
def create_user(pilotos: Pilotos):
    logger.info(f"📥 Registro de usuario recibido: {pilotos}")
    
    db = SessionLocal()
    existing = db.query(PilotosDB).filter(PilotosDB.pilotos == pilotos.pilotos).first()
    if existing:
        db.close()
        raise HTTPException(status_code=400, detail="El piloto ya está registrado")

    pilotos_db = PilotosDB(pilotos=pilotos.pilotos, victorias=pilotos.victorias, anosactivo=pilotos.anosactivo)
    db.add(pilotos_db)
    db.commit()
    db.refresh(pilotos_db)
    db.close()
    logger.info(f"✅ Piloto guardado: {pilotos_db.pilotos}")
    # Tarea en segundo plano
    # background_tasks.add_task(enviar_email_bienvenida, pilotos.email)
    return {
        "msg": "Piloto registrado correctamente",
        "pilotos": {
            "piloto": pilotos_db.pilotos,
            "victorias": pilotos_db.victorias,
            "anosactivo": pilotos_db.anosactivo
        }
    }
