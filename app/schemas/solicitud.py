
from datetime import datetime

from pydantic import BaseModel, Field

from app.core.constants import PRIORIDAD_PREDETERMINADA


class SolicitudCreate(BaseModel):
    titulo: str = Field(min_length=3, max_length=150)
    descripcion: str = Field(min_length=5)
    tipo: str = Field(min_length=2, max_length=80)
    prioridad: str = Field(
        default=PRIORIDAD_PREDETERMINADA,
        max_length=20
    )

    estudiante_id: int = Field(gt=0)
    area_id: int = Field(gt=0)
    responsable_id: int | None = Field(default=None, gt=0)


class SolicitudUpdate(BaseModel):
    titulo: str | None = Field(default=None, min_length=3, max_length=150)
    descripcion: str | None = Field(default=None, min_length=5)
    tipo: str | None = Field(default=None, min_length=2, max_length=80)
    prioridad: str | None = Field(default=None, max_length=20)
    estado: str | None = Field(default=None, max_length=30)

    estudiante_id: int | None = Field(default=None, gt=0)
    area_id: int | None = Field(default=None, gt=0)
    responsable_id: int | None = Field(default=None, gt=0)


class SolicitudResponse(BaseModel):
    id: int
    titulo: str
    descripcion: str
    tipo: str
    prioridad: str
    estado: str
    fecha_creacion: datetime

    estudiante_id: int
    area_id: int
    responsable_id: int | None
