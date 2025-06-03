from .basemodel import *

class DriversTB(Base):
    __tablename__ = "drivers"

    driverId = Column(Integer, primary_key=True, index=True, autoincrement=True)
    driverRef = Column(String, unique=True, index=True)
    number = Column(Integer, nullable=True)
    code = Column(String)
    forename = Column(String)
    surname = Column(String)
    dob = Column(String)
    nationality = Column(String)
    url = Column(String)

    results = relationship("ResultsTB", back_populates="driver")


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