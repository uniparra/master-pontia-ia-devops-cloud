import logging
from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator, model_validator

from sqlalchemy import Column, Integer, String, ForeignKey, create_engine, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

from fastapi import BackgroundTasks

import time

# --- Logging ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# --- DB Formula 1 ---
DATABASE_URL = "sqlite:///./formula1_4tables.sqlite"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

# --- SQLAlchemy models ---
class DriversTB(Base):
    __tablename__ = "drivers"

    driverId = Column(Integer, primary_key=True, index=True, autoincrement=True)
    driverRef = Column(String, unique=True, index=True)
    number = Column(Integer, nullable=True)
    code = Column(String)
    forename = Column(String)
    surname = Column(String)
    dob = Column(String)
    nationalty = Column(String)
    url = Column(String)

    results = relationship("ResultsTB", back_populates="driver")


class RacesTB(Base):
    __tablename__ = "races"

    raceId = Column(Integer, primary_key=True, index=True, autoincrement=True)
    year = Column(Integer)
    round = Column(Integer)
    circuitId = Column(Integer, ForeignKey("circuits.circuitId"), index=True)
    name = Column(String, index=True)
    date = Column(DateTime)
    time = Column(String)
    url = Column(String)

    results = relationship("ResultsTB", back_populates="race")
    circuit = relationship("CircuitsTB", back_populates="races")


class CircuitsTB(Base):
    __tablename__ = "circuits"

    circuitId = Column(Integer, primary_key=True, index=True, autoincrement=True)
    circuitRef = Column(String, unique=True, index=True)
    name = Column(String)
    location = Column(String)
    country = Column(String)
    lat = Column(String)
    long = Column(String)
    alt = Column(String)
    url = Column(String)

    races = relationship("RacesTB", back_populates="circuit")


class ResultsTB(Base):
    __tablename__ = "results"

    resultId = Column(Integer, primary_key=True, index=True, autoincrement=True)
    raceId = Column(Integer, ForeignKey("races.raceId"), index=True)
    driverId = Column(Integer, ForeignKey("drivers.driverId"), index=True)
    constructorId = Column(Integer, ForeignKey("constructors.constructorId"), index=True)
    number = Column(Integer)
    grid = Column(Integer)
    position = Column(Integer)
    positionText = Column(String)
    positionOrder = Column(Integer)
    points = Column(Integer)
    laps = Column(Integer)
    time = Column(String)
    milliseconds = Column(Integer)
    fastestLap = Column(Integer)
    rank = Column(Integer)
    fastestLapTime = Column(String)
    fastestLapSpeed = Column(String)
    statusId = Column(Integer, ForeignKey("status.statusId"), index=True)

    driver = relationship("DriversTB", back_populates="results")
    race = relationship("RacesTB", back_populates="results")



Base.metadata.create_all(bind=engine)


# --- Pydantic models ---
class Driver(BaseModel):
    driverId: Optional[int] = Field(None, description="ID del piloto")
    driverRef: str = Field(..., min_length=2, max_length=30, description="Referencia única del piloto")
    number: Optional[int] = Field(None, ge=1, le=99, description="Número del piloto (1-99)")
    code: Optional[str] = Field(None, min_length=2, max_length=5, description="Código del piloto")
    forename: str = Field(..., min_length=2, max_length=30, description="Nombre del piloto")
    surname: str = Field(..., min_length=2, max_length=30, description="Apellido del piloto")
    dob: str = Field(..., description="Fecha de nacimiento (YYYY-MM-DD)")
    nationalty: str = Field(..., min_length=2, max_length=30, description="Nacionalidad del piloto")
    url: Optional[str] = Field(None, description="URL de referencia")

    @field_validator("dob")
    def valid_dob(cls, value):
        import re
        if not re.match(r"\d{4}-\d{2}-\d{2}", value):
            raise ValueError("La fecha de nacimiento debe tener el formato YYYY-MM-DD")
        return value

class Race(BaseModel):
    raceId: Optional[int] = Field(None, description="ID de la carrera")
    year: int = Field(..., ge=1950, le=2100, description="Año de la carrera")
    round: int = Field(..., ge=1, description="Ronda de la carrera")
    circuitId: int = Field(..., description="ID del circuito")
    name: str = Field(..., min_length=3, max_length=50, description="Nombre de la carrera")
    date: Optional[str] = Field(None, description="Fecha de la carrera (YYYY-MM-DD)")
    time: Optional[str] = Field(None, description="Hora de la carrera (HH:MM:SS)")
    url: Optional[str] = Field(None, description="URL de referencia")

    @field_validator("date")
    def valid_date(cls, value):
        if value is not None:
            import re
            if not re.match(r"\d{4}-\d{2}-\d{2}", value):
                raise ValueError("La fecha debe tener el formato YYYY-MM-DD")
        return value

class Circuit(BaseModel):
    circuitId: Optional[int] = Field(None, description="ID del circuito")
    circuitRef: str = Field(..., min_length=2, max_length=30, description="Referencia única del circuito")
    name: str = Field(..., min_length=2, max_length=50, description="Nombre del circuito")
    location: str = Field(..., min_length=2, max_length=50, description="Ubicación del circuito")
    country: str = Field(..., min_length=2, max_length=50, description="País del circuito")
    lat: Optional[str] = Field(None, description="Latitud")
    long: Optional[str] = Field(None, description="Longitud")
    alt: Optional[str] = Field(None, description="Altitud")
    url: Optional[str] = Field(None, description="URL de referencia")

class Result(BaseModel):
    resultId: Optional[int] = Field(None, description="ID del resultado")
    raceId: int = Field(..., description="ID de la carrera")
    driverId: int = Field(..., description="ID del piloto")
    constructorId: int = Field(..., description="ID del constructor")
    number: Optional[int] = Field(None, ge=1, le=99, description="Número del piloto")
    grid: Optional[int] = Field(None, ge=1, description="Posición de salida")
    position: Optional[int] = Field(None, ge=1, description="Posición final")
    positionText: Optional[str] = Field(None, description="Texto de la posición")
    positionOrder: Optional[int] = Field(None, ge=1, description="Orden de la posición")
    points: Optional[int] = Field(None, ge=0, description="Puntos obtenidos")
    laps: Optional[int] = Field(None, ge=0, description="Vueltas completadas")
    time: Optional[str] = Field(None, description="Tiempo final")
    milliseconds: Optional[int] = Field(None, ge=0, description="Tiempo en milisegundos")
    fastestLap: Optional[int] = Field(None, ge=1, description="Vuelta más rápida")
    rank: Optional[int] = Field(None, ge=1, description="Ranking de la vuelta rápida")
    fastestLapTime: Optional[str] = Field(None, description="Tiempo de la vuelta rápida")
    fastestLapSpeed: Optional[str] = Field(None, description="Velocidad de la vuelta rápida")
    statusId: int = Field(..., description="ID del estado del resultado")

# --- Pydantic models ---
class Races(BaseModel):
    race_id: int = Field(..., description="Id de la carrera")
    name: str = Field(..., min_length=3, max_length=20, description="Nombre de la carrera (de 3 a 20 caracteres)")
    year: int = Field(None, description="Año de la carrera")
    winner_id: int = Field(..., description="Id del piloto ganador de la carrera")

    @field_validator("name")
    def racename(cls, value):
        if not any(vowel in value for vowel in ["a", "e", "i", "o", "u"]):
            raise ValueError("There must be vowels in the race name!")
        return value

    @field_validator("year")
    def valid_year(cls, value):
        y = int(time.strftime("%Y", time.gmtime()))
        if value > y:
            raise ValueError("The year of the race can't be higher than nowadays!!!")
        return value


class Pilots(BaseModel):
    pilot_id: int = Field(..., description="Id del piloto")
    name: str = Field(..., min_length=3, max_length=20, description="Nombre del piloto (de 3 a 20 caracteres)")
    vict: int = Field(..., description="Numero de victorias del piloto")
    active_years: int = Field(None, description="Años que ha estado en activo el piloto (opcional)")
    races_won: list[Races] = Field([], description="Lista de carreras ganadas por un piloto")

    @field_validator("name")
    def username_with_values(cls, value):
        if not any(vowel in value for vowel in ["a", "e", "i", "o", "u"]):
            raise ValueError("There must be vowels in the pilot name!")
        return value

    @field_validator("active_years")
    def active_pilot(cls, value):
        if value <= 0:
            raise ValueError("The pilot hasn't been active for at least one year")
        return value

    @model_validator(mode="after")
    def victory_validation(cls, instance):
        if instance.vict != len(instance.races_won):
            raise ValueError("It's not possible to have a discrepancy between the number of won races and victories")
        return instance

    # --- FastAPI setup ---


app = FastAPI(
    title="API para la práctica de clase sobre Formula 1",
    description="API de ejemplo",
    version="1.0.0"
)


#  Quiero preguntar si estos métodos al declarar sus respectivos ids con autoincrement es necesario pasarle algo al método como param
@app.post("/pilots/")
async def create_user(pilot: Pilots):
    # pilot_id = pilot.pilot_id
    pilot_name = pilot.name
    victories = pilot.vict
    active_years = pilot.active_years
    races_won = pilot.races_won
    return {
        "msg": "Información del piloto recibida correctamente",
        "PiloT name": pilot_name,
        "Victories": victories,
        "active_years": active_years,
        "races_won": races_won
    }


@app.post("/races/")
async def create_user(race: Races):
    # race_id = race.race_id
    name = race.name
    year = race.year
    winner_id = race.winner_id
    return {
        "msg": "Información de la carrera recibida correctamente",
        "Race name": name,
        "Year of the race": year,
        "Winner of the race": winner_id
    }


# método que va a devolver todas las carreras ganadas por un piloto
@app.get("/pilots/{pilot_name}/races")
def amount_of_won_races_by_pilot(pilot_name: str):
    logger.info(f"Petición de la lista de carreras del piloto {pilot_name}")
    db = SessionLocal()
    existing = db.query(DriversTB).filter(DriversTB.surname == pilot_name).first()
    if existing:
        db.close()
        logger.info(f"Envío del número de carreras ganadas por el piloto {pilot_name}")
        return {
            "msg": "Piloto encontrado",
            "races_won": f"{existing.pilot_name} ha ganado un total de {len(existing.races_won)} carreras",
            "races": existing.races_won
        }
    else:
        db.close()
        logger.warning(f"Envío del número de carreras ganadas por el piloto {pilot_name}")
        raise HTTPException(status_code=404, detail=f"El piloto {pilot_name} no esta registrado en la BBDD")


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
    # existing = db.query(PilotosTB).filter(PilotosTB.pilotos == pilotos.pilotos).first()
    # if existing:
    #     db.close()
    #     raise HTTPException(status_code=400, detail="El piloto ya está registrado")
    #
    # pilotos_db = PilotosTB(pilotosname=pilotos.pilotosname, victorias=pilotos.victorias, anosactivo=pilotos.anosactivo)
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