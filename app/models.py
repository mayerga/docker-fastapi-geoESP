from sqlalchemy import Column, Integer, String
from app.database import Base

class Lugar(Base):
    __tablename__ = "lugares"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    comunidad = Column(String, nullable=False)
    altitud = Column(Integer, nullable=False)


