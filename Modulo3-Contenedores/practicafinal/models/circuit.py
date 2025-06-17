from .basemodel import *

class CircuitsTB(Base):
    __tablename__ = "circuits"

    circuitId = Column(Integer, primary_key=True, index=True, autoincrement=True)
    circuitRef = Column(String, unique=True, index=True)
    name = Column(String)
    location = Column(String)
    country = Column(String)
    lat = Column(String)
    lng = Column(String)
    alt = Column(String)
    url = Column(String)

    races = relationship("RacesTB", back_populates="circuit")


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