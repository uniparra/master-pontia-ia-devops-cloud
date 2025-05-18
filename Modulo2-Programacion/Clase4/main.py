import logging
from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator, model_validator

from sqlalchemy import Column, Integer, String, create_engine
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

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

class PilotosDB(Base):
    __tablename__ = "formulauno"

    pilotos = Column(String, primary_key=True, index=True)
    victorias = Column(Integer, unique=True, index=True)
    anosactivo = Column(String, nullable=True)

Base.metadata.create_all(bind=engine)

# --- Pydantic model ---
class Pilotos(BaseModel):
    pilotos: str = Field(..., min_length=3, description="Nombre de usuario (mínimo 3 caracteres)")
    victorias: int = Field(..., description="Email del usuario")
    anosactivo: str = Field(None, ge=0, description="Edad no negativa (opcional)")

    @field_validator("pilotos")
    def username_with_values(cls, value):
        if not any(vowel in value for vowel in ["a", "e", "i", "o", "u"]):
            raise ValueError("You need vowels in your username!")
        return value

    @model_validator(mode="after")
    def long_username_if_age_ge_50(cls, instance):
        if instance.victorias is not None and instance.victorias >= 5:
            if len(instance.pilotos) > 12:
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

@app.post("/pilotos/")
def create_user(pilotos: Pilotos):
    logger.info(f"📥 Registro de usuario recibido: {pilotos}")
    
    # db = SessionLocal()
    # existing = db.query(PilotosDB).filter(PilotosDB.pilotos == pilotos.pilotos).first()
    # if existing:
    #     db.close()
    #     raise HTTPException(status_code=400, detail="El piloto ya está registrado")
    #
    # pilotos_db = PilotosDB(pilotosname=pilotos.pilotosname, victorias=pilotos.victorias, anosactivo=pilotos.anosactivo)
    # db.add(pilotos_db)
    # db.commit()
    # db.refresh(pilotos_db)
    # db.close()
    # logger.info(f"✅ Piloto guardado: {pilotos_db.pilotosname}")
    # Tarea en segundo plano
    # background_tasks.add_task(enviar_email_bienvenida, pilotos.email)
    return {
        "msg": "Usuario registrado correctamente",
        # "pilotos": {
        #     "piloto": pilotos_db.pilotos,
        #     "victorias": pilotos_db.victorias,
        #     "anosactivo": pilotos_db.anosactivo
        # }
    }
