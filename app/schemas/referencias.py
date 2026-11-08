
from pydantic import BaseModel, Field


class SolicitudReferencias(BaseModel):
    estudiante_id: int = Field(gt=0)
    area_id: int = Field(gt=0)
    responsable_id: int | None = Field(default=None, gt=0)
