from .basemodel import *
from .drivers import DriversTB

class ResultsTB(Base):
    __tablename__ = "results"

    resultId = Column(Integer, primary_key=True, index=True, autoincrement=True)
    raceId = Column(Integer, ForeignKey("races.raceId"), index=True)
    driverId = Column(Integer, ForeignKey("drivers.driverId"), index=True)
    constructorId = Column(Integer, index=True)
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
    statusId = Column(Integer, index=True)

    driver = relationship("DriversTB", back_populates="results")
    race = relationship("RacesTB", back_populates="results")

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
