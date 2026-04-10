from pydantic import BaseModel, Field

class Lugar(BaseModel):
    nombre: str = Field(..., example="Teide")
    comunidad: str = Field(..., example="Canarias")
    altitud: int = Field(..., description="Altitud en metros, debe ser un número entero")

class LugarCreate(LugarBase):
    pass

class Lugar(LugarBase):
    id: int

    # model_config = {"from_attributes": True}
