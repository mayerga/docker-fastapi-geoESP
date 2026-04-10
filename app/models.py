from sqlalchemy import Column, Integer, String
from api.database import Base

class Entidad(Base):
    __tablename__ = "lugares"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    comunidad = Column(String, nullable=False)
    altitud = Column(Integer, nullable=False)


