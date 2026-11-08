from pydantic import BaseModel, EmailStr, Field


class EstudianteCreate(BaseModel):
    nombre: str = Field(min_length=2, max_length=100)
    apellido: str = Field(min_length=2, max_length=100)
    email: EmailStr
    matricula: str = Field(min_length=3, max_length=30)


class EstudianteUpdate(BaseModel):
    nombre: str | None = Field(default=None, min_length=2, max_length=100)
    apellido: str | None = Field(default=None, min_length=2, max_length=100)
    email: EmailStr | None = None
    matricula: str | None = Field(default=None, min_length=3, max_length=30)


class EstudianteResponse(BaseModel):
    id: int
    nombre: str
    apellido: str
    email: str
    matricula: str