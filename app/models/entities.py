
from datetime import UTC, datetime

from sqlmodel import Field, SQLModel

from app.core.constants import (
    ESTADO_INICIAL_SOLICITUD,
    PRIORIDAD_PREDETERMINADA,
)


class Estudiante(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nombre: str = Field(max_length=100)
    apellido: str = Field(max_length=100)
    email: str = Field(max_length=150, unique=True, index=True)
    matricula: str = Field(max_length=30, unique=True)


class Area(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nombre: str = Field(max_length=100, unique=True)
    descripcion: str | None = Field(default=None, max_length=250)
    activa: bool = Field(default=True)


class Responsable(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nombre: str = Field(max_length=100)
    apellido: str = Field(max_length=100)
    email: str = Field(max_length=150, unique=True, index=True)
    area_id: int = Field(foreign_key="area.id")


class Solicitud(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    titulo: str = Field(max_length=150)
    descripcion: str
    tipo: str = Field(max_length=80)
    prioridad: str = Field(
        default=PRIORIDAD_PREDETERMINADA,
        max_length=20
    )
    estado: str = Field(
        default=ESTADO_INICIAL_SOLICITUD,
        max_length=30
    )

    fecha_creacion: datetime = Field(
        default_factory=lambda: datetime.now(UTC)
    )

    estudiante_id: int = Field(foreign_key="estudiante.id")
    area_id: int = Field(foreign_key="area.id")
    responsable_id: int | None = Field(
        default=None,
        foreign_key="responsable.id"
    )
