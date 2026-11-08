from pydantic import BaseModel, Field


class AreaCreate(BaseModel):
    nombre: str = Field(min_length=2, max_length=100)
    descripcion: str | None = Field(default=None, max_length=250)


class AreaUpdate(BaseModel):
    nombre: str | None = Field(default=None, min_length=2, max_length=100)
    descripcion: str | None = Field(default=None, max_length=250)
    activa: bool | None = None


class AreaResponse(BaseModel):
    id: int
    nombre: str
    descripcion: str | None
    activa: bool