from pydantic import BaseModel, EmailStr, Field


class ResponsableCreate(BaseModel):
    nombre: str = Field(min_length=2, max_length=100)
    apellido: str = Field(min_length=2, max_length=100)
    email: EmailStr
    area_id: int = Field(gt=0)


class ResponsableUpdate(BaseModel):
    nombre: str | None = Field(default=None, min_length=2, max_length=100)
    apellido: str | None = Field(default=None, min_length=2, max_length=100)
    email: EmailStr | None = None
    area_id: int | None = Field(default=None, gt=0)


class ResponsableResponse(BaseModel):
    id: int
    nombre: str
    apellido: str
    email: str
    area_id: int