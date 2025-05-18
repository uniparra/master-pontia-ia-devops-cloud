import logging
from http.client import HTTPException

from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Optional

from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from fastapi import BackgroundTasks

# --- Pydantic model ---
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

DATABASE_URL= "sqlite:///./usuarios.db"

engine= create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base=declarative_base()

class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    age = Column(Integer, nullable=True)

Base.metadata.create_all(bind=engine)
app = FastAPI(
    title="Mi primera api",
    description="Una API de ejemplo",
    version="1.0.0"
)

def enviar_email_bienvenida(email:str):
    logger.info(f"Enviando email de bienvenida a {email}")
    # Simulamos el envío de un email
    import time
    time.sleep(10)
    logger.info(f"Email enviado a {email}")

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

# @app.post("/users/")
# def create_user(user: User):
#     logger.info(f"Refistro de usuario recibido: {user}")
#     return {
#         "msg": "Usuario registrado correctamente",
#         "usuario" : user.username
#     }

@app.post("/users/")
def create_user(user: User, background_tasks: BackgroundTasks):
    logger.info(f"Registro de usuario recibido: {user}")

    db = SessionLocal()
    existing = db.query(UserDB).filter(UserDB.email == user.email).first()
    if existing:
        db.close()
        raise HTTPException(status_code=400, detail="El mail ya está registrado")
    user_db = UserDB(username=user.username, email=user.email, age=user.age)
    db.add(user_db)
    db.commit()
    db.refresh(user_db)
    db.close()

    logger.info(f"Usuario guardado en DB: {user_db.username}")
    background_tasks.add_task(enviar_email_bienvenida, user.email)
    return {
        "msg":"Usuario registrado correctamente",
        "usuario":{
            "id":user_db.id,
            "username":user_db.username,
            "email":user_db.email,
            "age":user_db.age
        }
    }