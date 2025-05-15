import logging
from pydantic import BaseModel
from typing import Optional

from fastapi import FastAPI

class User(BaseModel):
    username: str
    email: str
    age: Optional[int]

logging.basicConfig(  # el nivel es una cota inferior, es decir si
    # lo ponemos a error nos dara error y critical
    level=logging.INFO,  # DEBYG, INFO, WARNING, ERROR, CRITICAL
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    # handler <-- para manejar los logs, escribirlos, enviarlos por mail etc.
    # filter <-- para filtrar logs
)

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Mi primera api",
    description="Una API de ejemplo",
    version="1.0.0"
)


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
    logger.ingo(f"Refistro de usuario recibido: {user}")
    return {
        "msg": "Usuario registrado correctamente",
        "usuario" : user.username
    }