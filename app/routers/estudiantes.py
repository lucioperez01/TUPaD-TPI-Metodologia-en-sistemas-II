from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from app.core.exceptions import RecursoDuplicadoError, RecursoNoEncontradoError
from app.database.connection import get_session
from app.schemas.estudiante import (
    EstudianteCreate,
    EstudianteResponse,
    EstudianteUpdate,
)
from app.services import estudiante_service


router = APIRouter(
    prefix="/estudiantes",
    tags=["Estudiantes"]
)


@router.post(
    "/",
    response_model=EstudianteResponse,
    status_code=status.HTTP_201_CREATED
)
def crear_estudiante(
    datos: EstudianteCreate,
    session: Annotated[Session, Depends(get_session)]
):
    try:
        return estudiante_service.crear_estudiante(session, datos)
    except RecursoDuplicadoError as error:
        raise HTTPException(status_code=409, detail=str(error))
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))


@router.get("/", response_model=list[EstudianteResponse])
def obtener_estudiantes(
    session: Annotated[Session, Depends(get_session)]
):
    return estudiante_service.obtener_estudiantes(session)


@router.get("/{estudiante_id}", response_model=EstudianteResponse)
def obtener_estudiante(
    estudiante_id: int,
    session: Annotated[Session, Depends(get_session)]
):
    try:
        return estudiante_service.obtener_estudiante_por_id(
            session,
            estudiante_id
        )
    except RecursoNoEncontradoError as error:
        raise HTTPException(status_code=404, detail=str(error))


@router.put("/{estudiante_id}", response_model=EstudianteResponse)
def actualizar_estudiante(
    estudiante_id: int,
    datos: EstudianteUpdate,
    session: Annotated[Session, Depends(get_session)]
):
    try:
        return estudiante_service.actualizar_estudiante(
            session,
            estudiante_id,
            datos
        )
    except RecursoNoEncontradoError as error:
        raise HTTPException(status_code=404, detail=str(error))
    except RecursoDuplicadoError as error:
        raise HTTPException(status_code=409, detail=str(error))


@router.delete("/{estudiante_id}")
def eliminar_estudiante(
    estudiante_id: int,
    session: Annotated[Session, Depends(get_session)]
):
    try:
        return estudiante_service.eliminar_estudiante(
            session,
            estudiante_id
        )
    except RecursoNoEncontradoError as error:
        raise HTTPException(status_code=404, detail=str(error))