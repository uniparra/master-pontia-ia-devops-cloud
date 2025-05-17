import logging
from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Optional

from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base


class User(BaseModel):
    username: str = Field(..., min_length=3, description="Nombre de usuario (mínimo 3 caracteres).")
    email: str = Field(..., description="Email del usuario")
    age: Optional[int] = Field(None, ge=0, description="Edad no negativa (opcional)")

    @field_validator("username")
    def username_with_vowels(cls, value):
        if not any(vowel in value for vowel in ["a","e","i","o","u"]):
            raise ValueError("You need vowels in your username")
        return value

    # Mode = after se usa para que la validación se realice después de validar los campos
    #indivduales
    @model_validator(mode="after")
    def long_usernameif_age_ge_50(cls, instance):
        if instance.age >= 50:
            if len(instance.username) < 20:
                raise ValueError("You must provide a username longer than 20 chars")
        return instance

logging.basicConfig(  # el nivel es una cota inferior, es decir si
    # lo ponemos a error nos dara error y critical
    level=logging.INFO,  # DEBYG, INFO, WARNING, ERROR, CRITICAL
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    # handler <-- para manejar los logs, escribirlos, enviarlos por mail etc.
    # filter <-- para filtrar logs
)

logger = logging.getLogger(__name__)

DATABASE_URL= "sqlite: ///./usuarios.db"

engine= create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base=declarative_base()

class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    age = Column(Integer, nullable=True)

app = FastAPI(
    title="Mi primera api",
    description="Una API de ejemplo",
    version="1.0.0"
)

# ## Endpoints API Fórmula 1
#
# ## Pilotos (Drivers)
# GET /drivers                           - Listar todos los pilotos
# GET /drivers/{driver_id}              - Obtener información de un piloto
# GET /drivers/{driver_id}/results      - Resultados de un piloto
# GET /drivers/{driver_id}/wins         - Carreras ganadas por el piloto
# GET /drivers/search?name=alonso       - Buscar piloto por nombre
#
# ## Equipos (Constructors)
# GET /constructors                             - Listar todos los equipos
# GET /constructors/{constructor_id}            - Info de un equipo
# GET /constructors/{constructor_id}/drivers    - Pilotos del equipo
# GET /constructors/{constructor_id}/wins       - Carreras ganadas por el equipo
#
# ## Carreras (Races)
# GET /races                             - Lista de todas las carreras
# GET /races/{race_id}                   - Detalles de una carrera
# GET /races/latest                      - Última carrera
# GET /races/year/{year}                 - Carreras de un año específico
# GET /races/{race_id}/results           - Resultados de la carrera
#
# ## Circuitos
# GET /circuits                          - Lista de circuitos
# GET /circuits/{circuit_id}            - Info de un circuito
# GET /circuits/{circuit_id}/races      - Carreras celebradas en el circuito
#
# ## Temporadas
# GET /seasons                           - Lista de temporadas
# GET /seasons/{year}                    - Resumen de la temporada
# GET /seasons/{year}/champion          - Campeón del año
# GET /seasons/{year}/standings         - Clasificación final
#
# ## Extras
# GET /standings/drivers?year=2023           - Clasificación de pilotos de un año
# GET /standings/constructors?year





@app.get("/hello")
def initial_greeting():
    logger.info("Recibida peticion saludo generico")
    return {"msg": "Hola mundo!!!"}


@app.get("/hello/{name}")
def custom_greeting(name: str):
    logger.info(f"Recibida peticion saludo personalizado para {name}")
    processed_name = name.capitalize()
    logger.debug(f"Nombre tras .capitalize(): {processed_name}")
    if processed_name == "Unai":
        logger.warning("Unai ha entrado a la web!")
    return {"msg": f"Hello, {processed_name}!!!"}

@app.post("/users/")
def create_user(user: User):
    logger.info(f"Refistro de usuario recibido: {user}")
    return {
        "msg": "Usuario registrado correctamente",
        "usuario" : user.username
    }