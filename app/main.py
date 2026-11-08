
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database.connection import create_db_and_tables

from app.routers.estudiantes import router as estudiantes_router
from app.routers.areas import router as areas_router
from app.routers.responsables import router as responsables_router
from app.routers.solicitudes import router as solicitudes_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(
    title="EduGestión",
    description="Sistema de Gestión de Solicitudes Académicas",
    version="1.0.0",
    lifespan=lifespan
)


app.include_router(estudiantes_router)
app.include_router(areas_router)
app.include_router(responsables_router)
app.include_router(solicitudes_router)


@app.get("/")
def inicio():
    return {
        "mensaje": "Bienvenido a EduGestión",
        "estado": "Sistema funcionando correctamente"
    }


@app.get("/health")
def verificar_estado():
    return {
        "estado": "activo"
    }
