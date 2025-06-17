from .basemodel import *
from sqlalchemy.orm import Session
from fastapi import HTTPException
from . import races, results

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
    @model_validator(mode="after")
    def validate_result_ids(result, db: Session):
        # Check raceId exists
        if not db.query(races.RacesTB).filter_by(raceId=result.raceId).first():
            raise HTTPException(status_code=400, detail="raceId does not exist")
        # Check driverId exists
        if not db.query(results.DriversTB).filter_by(driverId=result.driverId).first():
            raise HTTPException(status_code=400, detail="driverId does not exist")
        # Check constructorId exists
        if not db.query(results.ConstructorsTB).filter_by(constructorId=result.constructorId).first():
            raise HTTPException(status_code=400, detail="constructorId does not exist")
        # Check statusId exists
        if not db.query(results.StatusTB).filter_by(statusId=result.statusId).first():
            raise HTTPException(status_code=400, detail="statusId does not exist")
        # Check year is not before the latest year
        race = db.query(races.RacesTB).filter_by(raceId=result.raceId).first()
        latest_year = db.query(races.RacesTB).order_by(races.RacesTB.year.desc()).first().year
        if race.year < latest_year:
            raise HTTPException(status_code=400, detail="Race year is before the latest year in the database")
        return result